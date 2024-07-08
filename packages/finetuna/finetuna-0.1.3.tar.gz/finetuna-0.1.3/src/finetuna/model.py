from datasets import load_dataset
from device import GetDefaultDevice
import evaluate
from hashlib import sha256
from itertools import islice
import json
import numpy as np
from pathlib import Path
from timeit import default_timer as timer
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_scheduler
import yaml


def _HashDict(d: dict):
  return sha256(json.dumps(d, sort_keys=True).encode("utf-8")).hexdigest()


def _LoadBaseModel(name: str, model_type: str, source: str, meta: dict):
  print("Fetching base model...")
  if source == "hf_transformers":
    if model_type == "sequence_classifier":
      return AutoModelForSequenceClassification.from_pretrained(
          name, num_labels=meta["num_labels"])


class Optimizer:
  def __init__(self, optimizer, scheduler):
    self._optimizer = optimizer
    self._scheduler = scheduler

  def Step(self):
    self._optimizer.step()
    self._scheduler.step()
    self._optimizer.zero_grad()

  def ToStateDict(self):
    return {
      "optimizer": self._optimizer.state_dict(),
      "scheduler": self._scheduler.state_dict(),
    }

  def LoadStateDict(self, state_dict):
    self._optimizer.load_state_dict(state_dict["optimizer"])
    self._scheduler.load_state_dict(state_dict["scheduler"])


class OptimizerTemplate:
  def __init__(self, cls, lr, scheduler):
    self._cls = cls
    self._lr = lr
    self._scheduler_name = scheduler

  def CreateOptimizer(self, params, num_steps):
    optimizer = self._cls(params, lr=self._lr)
    scheduler = get_scheduler(
        name=self._scheduler_name, optimizer=optimizer,
        num_warmup_steps=0, num_training_steps=num_steps)
    return Optimizer(optimizer, scheduler)


def _LoadOptimizerTemplate(config: dict):
  cls = None
  if config["type"] == "adamw":
    cls = AdamW
  lr = float(config.get("lr", "5e-5"))
  return OptimizerTemplate(cls, lr, config.get("scheduler", "linear"))


def _LoadDataset(name: str, model_name: str):
  print(f"Loading dataset \"{name}\"...")
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  def _Tokenize(data):
    return tokenizer(data["text"], padding="max_length", truncation=True)
  dataset = load_dataset(name)
  dataset = dataset.map(_Tokenize, batched=True)
  dataset = dataset.remove_columns(["text"])
  dataset = dataset.rename_column("label", "labels")
  dataset.set_format("torch")
  return dataset


class TrainingSet:
  def __init__(self, data, num_epochs, optimizer):
    self._data = data
    self._num_epochs = num_epochs
    self._optimizer = optimizer
    self._epoch = 0
    self._batch = 0

  def SetHash(self, hash):
    self._hash = hash

  def SetOptimizerHash(self, hash):
    self._optimizer_hash = hash

  def SetEpoch(self, epoch):
    self._epoch = epoch

  def SetBatch(self, batch):
    self._batch = batch

  def IsDone(self):
    return (self._epoch == self._num_epochs and self._batch == len(self._data))

  def ToStateDict(self):
    return {
      "hash": self._hash,
      "optimizer_hash": self._optimizer_hash,
      "epoch": self._epoch,
      "batch": self._batch,
      "optimizer": self._optimizer.ToStateDict(),
    }

  def InitOptimizer(self, state_dict):
    self._optimizer.LoadStateDict(state_dict)

  def Train(self, model, device, save=None):
    if self.IsDone():
      return

    epochs_left = self._num_epochs - self._epoch
    batches_skipped = self._batch
    num_steps_left = epochs_left * len(self._data) - batches_skipped
    progress = tqdm(range(num_steps_left))
    last_save_time = timer()
    for epoch in range(self._epoch, self._num_epochs):
      self._epoch = epoch
      self._batch = batches_skipped
      for batch in islice(self._data, batches_skipped, None):
        batch = {k: device.Upload(v) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        self._optimizer.Step()
        progress.update(1)
        self._batch += 1

        time_since_last_save = timer() - last_save_time
        if save and time_since_last_save > 120:
          save()
          time_since_last_save = timer()
      batches_skipped = 0
    self._epoch = self._num_epochs
    if save:
      save()

class Model:
  def __init__(self, config_path: Path):
    self._root_path = config_path.parent
    with open(config_path, "r") as config_file:
      config = yaml.safe_load(config_file)

    base_model = config["base_model"]
    self._base_model_config = base_model
    self._base_model = _LoadBaseModel(base_model["name"], base_model["type"],
                                      base_model["source"], base_model["meta"])

    self._optimizers = {}
    optimizer_hashes = {}
    self._optimizer_templates = {}
    for k, v in config["optimizers"].items():
      self._optimizer_templates[k] = _LoadOptimizerTemplate(v)
      optimizer_hashes[k] = _HashDict(v)

    base_sig = _HashDict(base_model)
    try:
      status = torch.load(self.GetStatusPath())
    except FileNotFoundError:
      status = {}

    train_configs = config.get("train", [])
    self._datasets = {}
    self._training_sets = []
    for set_config in train_configs:
      shuffle_seed = set_config.get("shuffle_seed")
      limit = set_config.get("limit")
      dataset = self.GetDataset(set_config.get("dataset"))
      data = dataset[set_config.get("datakey")]
      if shuffle_seed is not None:
        data = data.shuffle(seed=shuffle_seed)
      if limit is not None:
        data = data.select(range(limit))
      num_epochs = set_config.get("num_epochs", 1)
      optimizer_name = set_config.get("optimizer_name", "default")
      batch_size = set_config.get("batch_size", 1)
      loader = DataLoader(data, batch_size=batch_size)
      optimizer = self._optimizer_templates[optimizer_name].CreateOptimizer(
          self._base_model.parameters(), num_epochs * len(loader))
      training_set = TrainingSet(loader, num_epochs, optimizer)
      training_set.SetHash(_HashDict(set_config))
      training_set.SetOptimizerHash(optimizer_hashes[optimizer_name])
      self._training_sets.append(training_set)

    train_status = status.get("train", [])
    self._next_training_set = 0
    if status.get("base_sig") != base_sig:
      self._epoch = 0
      self._next_batch = 0
    else:
      for i in range(len(train_status)):
        state = train_status[i]
        if (i >= len(train_configs) or
            state.get("hash") != _HashDict(train_configs[i]) or
            state.get("optimizer_hash") !=
                optimizer_hashes[train_configs[i].get("optimizer")]):
          break
        epoch = state.get("epoch", 0)
        batch = state.get("batch", 0)
        training_set = self._training_sets[i]
        training_set.SetEpoch(epoch)
        training_set.SetBatch(batch)
        if training_set.IsDone():
          self._next_training_set = i + 1
        else:
          self._next_training_set = i
          training_set.InitOptimizer(state.get("optimizer"))

    self._evals = []
    for set_config in config.get("eval", []):
      shuffle_seed = set_config.get("shuffle_seed")
      limit = set_config.get("limit")
      dataset = self.GetDataset(set_config.get("dataset"))
      data = dataset[set_config.get("datakey")]
      if shuffle_seed is not None:
        data = data.shuffle(seed=shuffle_seed)
      if limit is not None:
        data = data.select(range(limit))
      batch_size = set_config.get("batch_size", 1)
      self._evals.append(DataLoader(data, batch_size=batch_size))

  def IsFullyTrained(self):
    return self._next_training_set >= len(self._training_sets)

  def GetStatusPath(self):
    return self._root_path / "status.pt"

  def GetDataset(self, name: str):
    if name not in self._datasets:
      self._datasets[name] = _LoadDataset(name, self._base_model_config["name"])
    return self._datasets.get(name)

  def Initialize(self):
    self.Save()

  def Save(self):
    status = {
      "base_sig": _HashDict(self._base_model_config),
      "train": [ts.ToStateDict() for ts in self._training_sets],
      "model": self._base_model.state_dict(),
    }
    torch.save(status, self.GetStatusPath())

  def Train(self):
    device = GetDefaultDevice()
    device.Upload(self._base_model)
    self._base_model.train()
    for i, training_set in enumerate(self._training_sets):
      training_set = self._training_sets[i]
      print(f"Training set {i + 1}/{len(self._training_sets)}...")
      training_set.Train(
          self._base_model, device, save=lambda: self.Save())

  def Eval(self):
    device = GetDefaultDevice()
    device.Upload(self._base_model)
    self._base_model.eval()
    metric = evaluate.load("accuracy")
    for i, data in enumerate(self._evals):
      print(f"Eval set {i + 1}/{len(self._evals)}...")
      for batch in data:
        batch = {k: device.Upload(v) for k, v in batch.items()}
        with torch.no_grad():
          outputs = self._base_model(**batch)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)
        metric.add_batch(predictions=predictions, references=batch["labels"])
    print(f"Accuracy: {metric.compute()['accuracy'] * 100}%")

