TOPLEVEL_LANG ?= verilog

SIM = verilator

EXTRA_ARGS += -Wno-lint

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../src:$(PYTHONPATH)

TOPLEVEL = md_reader
MODULE   = test_md_reader

VERILOG_SOURCES += $(PWD)/build_params.sv
VERILOG_SOURCES += $(PWD)/ethernet.sv
VERILOG_SOURCES += $(PWD)/register_map.sv
VERILOG_SOURCES += $(PWD)/utils.sv
VERILOG_SOURCES += $(PWD)/x10.sv
VERILOG_SOURCES += $(PWD)/fix_binary.sv
VERILOG_SOURCES += $(PWD)/md_reader.sv

include $(shell cocotb-config --makefiles)/Makefile.sim
