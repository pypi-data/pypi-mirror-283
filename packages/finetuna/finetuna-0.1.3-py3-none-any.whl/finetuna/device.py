import psutil
import torch


class Device:
  def __init__(self):
    pass

  def GetTotalMemory(self) -> int:
    pass

  def GetAllocatedMemory(self) -> int:
    pass

  def GetTorchDevice(self) -> object:
    return self._device

  def Upload(self, object):
    return object.to(self.GetTorchDevice())


class MpsDevice(Device):
  def __init__(self):
    assert torch.backends.mps.is_available()
    self._device = torch.device('mps')

  def GetTotalMemory(self) -> int:
    return psutil.virtual_memory().total

  def GetAllocatedMemory(self) -> int:
    return torch.mps.current_allocated_memory()

class CudaDevice(Device):
  def __init__(self):
    assert torch.cuda.is_available()
    self._device = torch.device('cuda')

  def GetTotalMemory(self) -> int:
    free, total = torch.cuda.mem_get_info()
    return total

  def GetAllocatedMemory(self) -> int:
    return torch.cuda.memory_allocated()


def CpuDevice(Device):
  def __init__(self):
    self._device = torch.device('cpu')

  def GetTotalMemory(self) -> int:
    return psutil.virtual_memory().total

  def GetAllocatedMemory(self) -> int:
    # Not really.
    return psutil.virtual_memory().used


def GetDefaultDevice() -> Device:
  if torch.cuda.is_available():
    return CudaDevice()
  if torch.backends.mps.is_available():
    return MpsDevice()
  return CpuDevice()
