import os
from pathlib import Path
import random
from typing import Any, Dict, List
from collections.abc import Callable

import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ReadOnly
# from cocotb.runner import get_runner

CLK_EDGE_FREQ = 10
  

class MDRunner:
  def __init__(self, dut):
    self.security_id = dut.security_id
    self.price = dut.price 
    self.size = dut.size
    self.side = dut.side
    self.md_parse_valid = dut.md_parse_valid
    self.count = 0

  async def start(self, stop_token = lambda: False) -> None:
    while (not stop_token()):
      await RisingEdge(self.md_parse_valid)

    #   if (self.count % 100 == 0):
    #     input("something")
    #   self.count += 1

      print("next parse summary: security_id: %8d price: %6d size: %4d aggressor_side: %1d" % 
            (
              int(self.security_id.value),
              int(self.price.value), 
              int(self.size.value), 
              int(self.side.value)
            )) 
      
  

# reset copied from cocotb docs
async def reset_dut(reset_n, duration_ns):
  reset_n.value = 0
  await Timer(duration_ns, units="ns")
  reset_n.value = 1
  reset_n._log.debug("Reset complete")


@cocotb.test()
async def test_with_handler(dut):
  random.seed(1)

  # maybe change name to MDUpdateRelayer
  runner = MDRunner(dut)

  cocotb.start_soon(Clock(dut.clk, 1, "ns").start())
  cocotb.start_soon(reset_dut(dut.rst, 100))
  cocotb.start_soon(runner.start())

  await Timer(100000, units="ns")
