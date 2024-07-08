import argparse
from model import Model
from pathlib import Path
import shutil
import sys
import torch


class HelpfulParser(argparse.ArgumentParser):
  def error(self, message):
    self.print_help(sys.stderr)
    sys.exit(1)


def main():
  parser = HelpfulParser(
      description="You can finetuna model but you can't finetuna fish")
  subparsers = parser.add_subparsers(
      title="Subcommands", dest="command", metavar="")

  new_parser = subparsers.add_parser(
      "new", help="Create a new fine-tuned model")
  new_parser.add_argument(
      "config", action="store", type=Path,
      help="Path to fine-tuning config (YAML) file")
  new_parser.add_argument(
      "modeldir", action="store", type=Path,
      help="Path to output the fine-tuned model")

  continue_parser = subparsers.add_parser(
      "continue", help="Continues fine-tuning from a checkpoint")
  continue_parser.add_argument(
      "modeldir", action="store", type=Path,
      help="Path to the fine-tuned model")

  eval_parser = subparsers.add_parser(
      "eval", help="Evaluates performance of a fine-tuned model")
  eval_parser.add_argument(
      "modeldir", action="store", type=Path,
      help="Path to the fine-tuned model")

  args = parser.parse_args()
  if args.command == "new":
    args.modeldir.mkdir(parents=True)
    config_path = args.modeldir / "config.yaml"
    shutil.copy(args.config, config_path)
    model = Model(config_path)
    model.Initialize()
    model.Train()
  elif args.command == "continue":
    config_path = args.modeldir / "config.yaml"
    model = Model(config_path)
    model.Train()
  elif args.command == "eval":
    config_path = args.modeldir / "config.yaml"
    model = Model(config_path)
    model.Eval()
  else:
    parser.print_help(sys.stderr)
    sys.exit(1)
  sys.exit(0)

if __name__ == "__main__":
  main()
