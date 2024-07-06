import os
from pathlib import Path

import cocotb
from cocotb.runner import get_runner


def run():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "verilator")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [
        proj_path + "functions.sv",
        proj_path + "modes.sv",
        proj_path + "cme_md_parser.sv",
        proj_path + "pcapparser_10gbmac.sv",
        proj_path + "triggerer.sv",
        proj_path + "app.sv"
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

    runner.test(hdl_toplevel="app", test_module="md_run,") 
