import os
import random
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def test_runner():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "verilator")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [
        proj_path / "../gg_fpga/functions.sv",
        proj_path / "../gg_fpga/modes.sv",
        proj_path / "../gg_fpga/cme_md_parser.sv",
        proj_path / "../gg_fpga/pcapparser_10gbmac.sv",
        proj_path / "../gg_fpga/triggerer.sv",
        proj_path / "../gg_fpga/app.sv"
    ]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=[],
        hdl_toplevel="app",
        build_args=["-Wno-lint", "-fno-expand", "-Wno-multidriven"],
        defines={"-w": 1},
        always=False,
        verbose=True
    )

    runner.test(hdl_toplevel="app", test_module="test_md_parser,")

if __name__ == "__main__":
    test_runner()
