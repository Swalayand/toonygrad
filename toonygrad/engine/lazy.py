from __future__ import annotations
from typing import cast, Tuple, Dict
from toonygrad.ops import UOp, UOps
from toonygrad.shape.symbolic import sint
from toonygrad.shape.shapetracker import ShapeTracker
from toonygrad.device import Buffer
from toonygrad.helpers import all_same, unwrap, prod

buffers: Dict[LazyBuffer, Buffer] = {}

class LazyBuffer(UOp):
  buffer_num = -1

  @property
  def buffer(self) -> Buffer:
    assert self.op == UOps.BUFFER
    if (ret:=buffers.get(self, None)) is not None: return ret
    ret = buffers[self] = Buffer(self.arg[0], self.size, self.dtype)
    return ret

  def copy_to_device(self, device):
    return UOp(UOps.COPY, self.dtype, (self,), device)

  @staticmethod
  def metaop(op, shape, dtype, device, arg=None, src=None):
    print(op, shape, dtype, device, arg, src)
    LazyBuffer.buffer_num += 1
    return LazyBuffer(UOps.BUFFER, dtype, (ShapeTracker.from_shape(shape).to_uop(),), (device, LazyBuffer.buffer_num))