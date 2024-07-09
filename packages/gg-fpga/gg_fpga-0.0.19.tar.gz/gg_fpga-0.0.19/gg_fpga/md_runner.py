# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#  # This Source Code Form is subject to the terms of the Mozilla Public
#  # License, v. 2.0. If a copy of the MPL was not distributed with this
#  # file, You can obtain one at https://mozilla.org/MPL/2.0/.

# <!-- This Source Code Form is subject to the terms of the Mozilla Public
#    - License, v. 2.0. If a copy of the MPL was not distributed with this
#    - file, You can obtain one at https://mozilla.org/MPL/2.0/. -->

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random
import struct
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

import xlwt 

import cocotb
from cocotb.handle import SimHandleBase, ModifiableObject
from cocotb.clock import Clock
from cocotb.triggers import Timer, Edge, RisingEdge, First
from cocotb.simulator import get_sim_time

CLK_PERIOD = 10
TIME_UNITS = "ns"
SIM_PERIOD_DIV = 1000000


@dataclass
class FPGAParseHandler:
    """Class to track dut md parsing signals and output"""

    clk: ModifiableObject
    security_id: ModifiableObject
    price: ModifiableObject 
    size: ModifiableObject
    side: ModifiableObject
    md_parse_valid: ModifiableObject
    fire: ModifiableObject
    prev_md_valid: bool = False
    count: int = 0 
    time: int = 0

    def __init__(self, dut: SimHandleBase) -> None:
        self.clk = dut.clk
        self.security_id = dut.security_id
        self.price = dut.price 
        self.size = dut.size
        self.side = dut.side
        self.md_parse_valid = dut.md_parse_valid
        self.fire = dut.fire
        # liskov
        self.count = 0 
        self.time = 0
    
    def update_time(self) -> None:
        lo, hi = get_sim_time()
        t = int(int(hi) << 32 | int(lo))
        self.time = int(t / SIM_PERIOD_DIV)

    async def get_next_parse(self) -> bool:
        await First(RisingEdge(self.md_parse_valid), RisingEdge(self.fire))
        if (self.md_parse_valid.value):
            self.update_time()
            self.count += 1
            return True 
        else:
            return False

class FPGAParseLogger(FPGAParseHandler):
    """Class to write FPGA parse output to excel file (base: FPGAParseHandler)"""
    
    def __init__(self, dut: SimHandleBase, price_div: int, active_id: int) -> None:
        super().__init__(dut)
        self.price_div = price_div
        self.active_id = active_id

    async def start(self) -> None:
        while True:
            if await self.get_next_parse():
                if int(self.security_id.value) == self.active_id:
                    print(f"summary: id: {int(self.security_id.value): 8d} price: {float(self.price.value.integer)/self.price_div: 6f} size: {int(self.size.value): 4d} agg_side: {int(self.side.value): 1d} fired: {bool(self.fire.value): 1b}")                
                else:
                    print(f"summary: id: {int(self.security_id.value): 8d} price(raw): {self.price.value.integer: 10d} size: {int(self.size.value): 4d} agg_side: {int(self.side.value): 1d} fired: {bool(self.fire.value): 1b}")                

class FPGAParseExcelWriter(FPGAParseHandler):
    """Class to write FPGA parse output to excel file (base: FPGAParseHandler)"""
    
    def __init__(self, dut: SimHandleBase, filename: str, price_div: int, active_id: int) -> None:
        super().__init__(dut)
        self.filename = filename
        self.price_div = price_div
        self.active_id = active_id
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet("md_parse_out")
        self.wb.save(self.filename)
        self.active_count = 0

    async def start(self) -> None:
        while True:
            if await self.get_next_parse() and int(self.security_id.value) == self.active_id:
                self.active_count += 1
                self.ws.write(self.active_count, 0, self.time)
                self.ws.write(self.active_count, 1, int(self.security_id.value))
                self.ws.write(self.active_count, 2, float(self.price.value) / self.price_div)
                self.ws.write(self.active_count, 3, int(self.size.value))
                self.ws.write(self.active_count, 4, int(self.side.value))
                self.ws.write(self.active_count, 5, int(self.fire.value))
                self.wb.save(self.filename)  

                print(f"summary: id: {int(self.security_id.value): 8d} price: {int(int(self.price.value)/self.price_div): 6f} size: {int(self.size.value): 4d} agg_side: {int(self.side.value): 1d} fired: {bool(self.fire.value): 1b}")                


class FPGAParsePlotter(FPGAParseHandler):
    def __init__(self, dut: SimHandleBase, filename: str, price_div: int, active_id: int) -> None:
        super().__init__(dut)
        self.filename = filename
        # not ideal
        self.price_div = price_div / 100
        self.active_id = active_id
        self.price_triggers = dut.price_triggers
        self.times = []
        self.prices = []
        self.sizes = []
        self.sides = []
        self.fires = []
        self.price_his = []
        self.price_los = []
        self.fig = plt.figure()
        self.ax = plt.axes()
        # self.graph = self.ax.plot(self.times, self.prices, "gs", self.times, self.sizes, "y-", self.times, self.sides, "C0*", self.times, self.fires, "r--")
        self.graph = self.ax.plot(self.times, self.prices, self.times, self.fires, self.times, self.price_his, self.times, self.price_los)
        for l in self.graph:
            l.set(antialiased=False, visible=True, linewidth=0)
        l1, l2, l3, l4 = self.graph
        l1.set(color="green", marker="s", markersize=2)
        l2.set(color="red", marker="+", markersize=5)
        l3.set(color="blue", marker=".", markersize=2)
        l4.set(color="orange", marker=".", markersize=2)
        # l2.set(color="red", linewidth=0.01)
        # l3.set(color="purple", linewidth=0.01)
        # l4.set(color="yellow", linewidth=0.01)
        # self.ax.set_title("FPGA Parse: times vs (price | size | side | fire)")
        self.ax.set_title("FPGA Parse: x: time || y: price | fire | hi triggers | lo triggers")

    async def get_next_parse(self) -> bool:
        await First(RisingEdge(self.md_parse_valid), RisingEdge(self.fire))
        self.update_time()
        self.count += 1
        return True 
        # else: 
        #     return False

    def update_plt(self) -> None:
        self.graph[0].set_data(self.times, self.prices)
        self.graph[1].set_data(self.times, self.fires)
        self.graph[2].set_data(self.times, self.price_his)
        self.graph[3].set_data(self.times, self.price_los)

    async def start(self) -> None:
        while True:
            if await self.get_next_parse():
                if self.md_parse_valid.value and int(self.security_id.value) == self.active_id:
                    self.times.append(self.time)
                    self.prices.append(self.scale_price_sig(self.price))
                    self.sizes.append(int(self.size.value))
                    self.sides.append(int(self.side.value))
                    self.fires.append(int(self.fire.value) * self.scale_price_sig(self.price))
                    
                    if len(self.price_his):
                        self.price_his.append(self.price_his[-1])
                        self.price_los.append(self.price_los[-1])
                    else:
                        self.price_his.append(self.prices[-1])
                        self.price_los.append(self.prices[-1])
                
                    self.update_plt()

                    print(f"summary: id: {int(self.security_id.value): 8d} price: {float(self.price.value.integer)/self.price_div: 10f} size: {int(self.size.value): 4d} agg_side: {int(self.side.value): 1d} fired: {bool(self.fire.value): 1b}")
                # price_triggers Edge
                elif len(self.prices): 
                    # put back in get_next_parse
                    self.update_time()
                    self.count += 1
                    # put back in get_next_parse
                    self.times.append(self.time)
                    self.prices.append(self.prices[-1])
                    self.sizes.append(self.sizes[-1])
                    self.sides.append(self.sides[-1])
                    self.fires.append(self.fires[-1]) 

                    hi_trig = int(self.price_triggers[0].value.integer >> 64)
                    lo_trig = int(self.price_triggers[0].value.integer & 0x0000000000000000ffffffffffffffff)
                    
                    self.price_his.append(self.scale_price(hi_trig))
                    self.price_los.append(self.scale_price(lo_trig))

                    self.update_plt()
                
    def save(self) -> None:
        if len(self.times):
            plt.xlim(0, self.times[-1]+100)
            max_p = max(self.prices)
            min_p = min(self.prices)
            plt.ylim(int(min_p * 0.9998), int(max_p*1.0002))
            self.fig.savefig(self.filename)
        else:
            print("no summaries recorded not saving file")
    
    def scale_price_sig(self, price: ModifiableObject) -> int:
        return self.scale_price(int(price.value))

    def scale_price(self, price: int) -> int:
        return int(float(price) / self.price_div)
    

# reset copied from cocotb docs
async def reset_dut(reset_n: ModifiableObject, duration_ns: int) -> None:
    reset_n.value = 0
    await Timer(duration_ns, units="ns")
    reset_n.value = 1
    reset_n._log.debug("Reset complete")

@cocotb.test()
async def test_with_handler(dut: SimHandleBase) -> None:
    random.seed(1)

    parse_mode = cocotb.plusargs["parse_mode"]
    duration_str = cocotb.plusargs["duration"]
    filename = cocotb.plusargs["filename"]
    price_div_str = cocotb.plusargs["price_div"]
    active_id_str = cocotb.plusargs["active_id"]

    duration = int(duration_str)
    price_div = int(price_div_str)
    active_id = int(active_id_str)

    if parse_mode == "l":
        handler = FPGAParseLogger(dut, price_div, active_id)
    elif parse_mode == "e":
        if not filename:
            raise ValueError("filename not set but needed for write to excel file mode; please set file to write to")
        handler = FPGAParseExcelWriter(dut, filename, price_div, active_id)
    elif parse_mode == "p":
        if not filename:
            raise ValueError("filename not set but needed for write plt img mode; please set file to write img to")
        handler = FPGAParsePlotter(dut, filename, price_div, active_id)
    else:
        raise ValueError("invalid parse_mode: use 'l' for logging; or 'e' for excel; or 'p' for plot")
    
    clk = cocotb.start_soon(Clock(dut.clk, CLK_PERIOD, "ns").start())
    cocotb.start_soon(reset_dut(dut.rst, 100))
    run_task = cocotb.start_soon(handler.start())

    await Timer(duration, units="ns")
    if parse_mode == "p":
        handler.save()
    clk.kill()
    run_task.kill()
