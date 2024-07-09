# gg-fpga
FPGA / Python simulation and output focused on exchange binary  
protocol parsing and specifics of byte layout for msg types.  
Uses SystemVerilog and Python and currently supports interfacing  
with excel and matplotlib.pyplot.  

### Note:
Currently set up to only work easily on Linux platforms.  

In addition to dependencies in pyproject, also requires:   
  - iverilog  

And, for simulation:  
- verilator (only easily installable for Linux systems)  

(can use other simulators as well: set in module 'run' as different default or set in env as SIM=\<your simulator choice\>)
