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

import os
from pathlib import Path

from cocotb.runner import get_runner


def to_sv_trigger_mode(mode: str):
    if mode != "h":
        raise ValueError("invalid trigger mode or not implemented: only mode == 'h' valid")
    else:
        return 2

def run(
    security_id: int = 3445,
    parse_mode: str = "l",
    duration: int = 1000000,
    filename: str = "",
    trigger_mode: str = "h",
    price_div: int = pow(10, 11),
):
    """
        Args:
        
        security_id: int (Optional)
            id to trigger on in incoming trade summaries
            (default is 3445 for cme ES)
        
        parse_mode: str (Optional)
            output handling mode: 
                "l" is log mode: (parsed summary values are just printed to console; no writing)
                "x" is excel write mode: 
                    (time, price, size, aggressor side, trigger fire are written to excel file for each new summary)
                "p" is plot mode:
                    (price, fire, hi price trigger, lo price trigger are plotted vs time using basic plt)
        
        duration: int (Optional)
            sim time duration (in ns) of run
            (default is 1000000: note: clk is set at 10ns period)

        filename: str (Optional/Required)
            filename to write to: Required for parse_mode x (excel) or p (plt)
            (for excel use .xls suffix; for plt use .jpg or .png suffix)

        trigger_mode: str (Optional / Not implemented)
            triggering mode ("h": HIT_WIDTH_SHIFT, (not implemented: STATIC, BOUNCE_BACK))
        
        price_div: int (Optional)
            factor to divide msg price by to get real human readable price
            (defaulted to 1e9 for cme ES (Price9 and display factor 0.01))
    """

    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "verilator")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [
        proj_path / "functions.sv",
        proj_path / "gg_fpga.sv",
        proj_path / "cme_md_parser.sv",
        proj_path / "pcapparser_10gbmac.sv",
        proj_path / "triggerer.sv",
        proj_path / "app.sv"
    ]   

    runner = get_runner(sim)
    
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=[],
        hdl_toplevel="app",
        build_args=["-Wno-lint", "-fno-expand", "-Wno-multidriven"],
        parameters={
            "SECURITY_ID": security_id,
            "TRIGGER_MODE": to_sv_trigger_mode(trigger_mode)
        },
        defines={"-w": 1},
        always=False,
        verbose=True
    )

    runner.test(
        hdl_toplevel="app", 
        test_module="md_runner", 
        plusargs=[
            f"+parse_mode={parse_mode}",
            f"+duration={str(duration)}",
            f"+filename={filename}",
            f"+price_div={str(price_div)}",
            f"+active_id={str(security_id)}"
        ]
    ) 
