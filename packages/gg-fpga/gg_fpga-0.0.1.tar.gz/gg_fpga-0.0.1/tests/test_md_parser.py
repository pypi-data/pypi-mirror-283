import os
from pathlib import Path
import random
from typing import Any, Dict, List
from collections.abc import Callable

import numpy as np

import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ReadOnly

CLK_EDGE_FREQ = 10


class PriceTracker:
    def __init__(self, dut: SimHandleBase):
        self.security_id = dut.security_id
        self.price = dut.price 
        self.size = dut.size
        self.side = dut.side
        self.md_parse_valid = dut.md_parse_valid
    
    async def start(self, stop_token: Callable[[], bool] = lambda: False) -> None:
        while (not stop_token()):
            await RisingEdge(self.md_parse_valid)
            print("next parse summary: security_id: %8d price: %6d size: %4d aggressor_side: %1d" % (
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
async def test(dut):
    random.seed(1)

    price_tracker = PriceTracker(dut)
        
    clk = cocotb.start_soon(Clock(dut.clk, 1, "ns").start())
    cocotb.start_soon(reset_dut(dut.rst, 100))
    track_task = cocotb.start_soon(price_tracker.start())

    await Timer(100000, units="ns")
    clk.kill()
    track_task.kill()
