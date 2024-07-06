// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"
#include "Vtop___024unit.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_app);
    __Vhier.remove(&__Vscope_app, &__Vscope_app__md_parser);
    __Vhier.remove(&__Vscope_app, &__Vscope_app__pcap_parser);
    __Vhier.remove(&__Vscope_app, &__Vscope_app__pv_triggerer);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_app.configure(this, name(), "app", "app", -9, VerilatedScope::SCOPE_MODULE);
    __Vscope_app__md_parser.configure(this, name(), "app.md_parser", "md_parser", -9, VerilatedScope::SCOPE_MODULE);
    __Vscope_app__pcap_parser.configure(this, name(), "app.pcap_parser", "pcap_parser", -9, VerilatedScope::SCOPE_MODULE);
    __Vscope_app__pv_triggerer.configure(this, name(), "app.pv_triggerer", "pv_triggerer", -9, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_app);
    __Vhier.add(&__Vscope_app, &__Vscope_app__md_parser);
    __Vhier.add(&__Vscope_app, &__Vscope_app__pcap_parser);
    __Vhier.add(&__Vscope_app, &__Vscope_app__pv_triggerer);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0);
        __Vscope_TOP.varInsert(__Vfinal,"rst", &(TOP.rst), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"DURATION", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__DURATION))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"HITTING_MODE", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__HITTING_MODE))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,1,0);
        __Vscope_app.varInsert(__Vfinal,"HIT_WIDTH", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__HIT_WIDTH))), true, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app.varInsert(__Vfinal,"NUM_INSTRUMENTS", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__NUM_INSTRUMENTS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"PCAP_PATH", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__PCAP_PATH))), true, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,479,0);
        __Vscope_app.varInsert(__Vfinal,"PRICE_HI", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__PRICE_HI))), true, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app.varInsert(__Vfinal,"PRICE_LO", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__PRICE_LO))), true, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app.varInsert(__Vfinal,"SECURITY_ID", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__SECURITY_ID))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"SIZE_HI", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__SIZE_HI))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"SIZE_LO", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__SIZE_LO))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"TRIGGER_MODE", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__TRIGGER_MODE))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_data", &(TOP.app__DOT__aso_out_data), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_empty", &(TOP.app__DOT__aso_out_empty), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,2,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_eop", &(TOP.app__DOT__aso_out_eop), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_error", &(TOP.app__DOT__aso_out_error), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,5,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_ready", &(TOP.app__DOT__aso_out_ready), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_sop", &(TOP.app__DOT__aso_out_sop), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"aso_out_valid", &(TOP.app__DOT__aso_out_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"available", &(TOP.app__DOT__available), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"clk", &(TOP.app__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"fire", &(TOP.app__DOT__fire), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"fire_state", &(TOP.app__DOT__fire_state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,1 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"md_parse_valid", &(TOP.app__DOT__md_parse_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"paused", &(TOP.app__DOT__paused), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"pcapfinished", &(TOP.app__DOT__pcapfinished), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"pktcount", &(TOP.app__DOT__pktcount), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,7,0);
        __Vscope_app.varInsert(__Vfinal,"price", &(TOP.app__DOT__price), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app.varInsert(__Vfinal,"price_triggers", &(TOP.app__DOT__price_triggers), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,2 ,127,0 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"rst", &(TOP.app__DOT__rst), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app.varInsert(__Vfinal,"rst_trigger", &(TOP.app__DOT__rst_trigger), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"security_id", &(TOP.app__DOT__security_id), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"security_id_triggers", &(TOP.app__DOT__security_id_triggers), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,2 ,31,0 ,0,0);
        __Vscope_app.varInsert(__Vfinal,"side", &(TOP.app__DOT__side), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,1,0);
        __Vscope_app.varInsert(__Vfinal,"size", &(TOP.app__DOT__size), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app.varInsert(__Vfinal,"size_triggers", &(TOP.app__DOT__size_triggers), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,2 ,63,0 ,0,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"MDIncrementalRefreshTradeSummaryID", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__MDIncrementalRefreshTradeSummaryID))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"clk", &(TOP.app__DOT__md_parser__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"grp_idx", &(TOP.app__DOT__md_parser__DOT__grp_idx), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,1 ,15,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"in_grp_idx", &(TOP.app__DOT__md_parser__DOT__in_grp_idx), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,1 ,15,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"ip_header", &(TOP.app__DOT__md_parser__DOT__ip_header), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,271,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"ipv4_header_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__ipv4_header_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"md_entry", &(TOP.app__DOT__md_parser__DOT__md_entry), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,239,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"md_entry_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__md_entry_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"md_entry_pad", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__md_entry_pad))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"no_in_group", &(TOP.app__DOT__md_parser__DOT__no_in_group), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,7,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"order_entry", &(TOP.app__DOT__md_parser__DOT__order_entry), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,95,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"order_entry_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__order_entry_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"order_entry_pad", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__order_entry_pad))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"out_price", &(TOP.app__DOT__md_parser__DOT__out_price), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"out_security_id", &(TOP.app__DOT__md_parser__DOT__out_security_id), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"out_side", &(TOP.app__DOT__md_parser__DOT__out_side), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,1,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"out_size", &(TOP.app__DOT__md_parser__DOT__out_size), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"out_valid", &(TOP.app__DOT__md_parser__DOT__out_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"packet_header", &(TOP.app__DOT__md_parser__DOT__packet_header), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,95,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"packet_header_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__packet_header_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"packet_idx", &(TOP.app__DOT__md_parser__DOT__packet_idx), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,1 ,15,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"parse_md_group", &(TOP.app__DOT__md_parser__DOT__parse_md_group), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"parse_ord_grp_size", &(TOP.app__DOT__md_parser__DOT__parse_ord_grp_size), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"parse_order_group", &(TOP.app__DOT__md_parser__DOT__parse_order_group), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"rst", &(TOP.app__DOT__md_parser__DOT__rst), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"rx", &(TOP.app__DOT__md_parser__DOT__rx), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"rx_eop", &(TOP.app__DOT__md_parser__DOT__rx_eop), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"rx_rem", &(TOP.app__DOT__md_parser__DOT__rx_rem), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,1 ,15,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"rx_valid", &(TOP.app__DOT__md_parser__DOT__rx_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"sbe_message_header", &(TOP.app__DOT__md_parser__DOT__sbe_message_header), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,79,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"sbe_message_header_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__sbe_message_header_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"set_out_valid", &(TOP.app__DOT__md_parser__DOT__set_out_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"trade_summary", &(TOP.app__DOT__md_parser__DOT__trade_summary), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,71,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"trade_summary_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__trade_summary_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"trade_summary_pad", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__trade_summary_pad))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"udp_header", &(TOP.app__DOT__md_parser__DOT__udp_header), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app__md_parser.varInsert(__Vfinal,"udp_header_len", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__md_parser__DOT__udp_header_len))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_data", &(TOP.app__DOT__pcap_parser__DOT__aso_out_data), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_empty", &(TOP.app__DOT__pcap_parser__DOT__aso_out_empty), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,2,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_eop", &(TOP.app__DOT__pcap_parser__DOT__aso_out_eop), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_error", &(TOP.app__DOT__pcap_parser__DOT__aso_out_error), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,5,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_ready", &(TOP.app__DOT__pcap_parser__DOT__aso_out_ready), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_sop", &(TOP.app__DOT__pcap_parser__DOT__aso_out_sop), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"aso_out_valid", &(TOP.app__DOT__pcap_parser__DOT__aso_out_valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"available", &(TOP.app__DOT__pcap_parser__DOT__available), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"clk_out", &(TOP.app__DOT__pcap_parser__DOT__clk_out), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"countIPG", &(TOP.app__DOT__pcap_parser__DOT__countIPG), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"diskSz", &(TOP.app__DOT__pcap_parser__DOT__diskSz), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"eof", &(TOP.app__DOT__pcap_parser__DOT__eof), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"file", &(TOP.app__DOT__pcap_parser__DOT__file), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"global_header", &(TOP.app__DOT__pcap_parser__DOT__global_header), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,2 ,7,0 ,0,23);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"i", &(TOP.app__DOT__pcap_parser__DOT__i), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"ipg", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__pcap_parser__DOT__ipg))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"newpkt", &(TOP.app__DOT__pcap_parser__DOT__newpkt), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"packet_header", &(TOP.app__DOT__pcap_parser__DOT__packet_header), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,2 ,7,0 ,0,15);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"pause", &(TOP.app__DOT__pcap_parser__DOT__pause), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"pcap_filename", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__pcap_parser__DOT__pcap_filename))), true, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,1 ,479,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"pcapfinished", &(TOP.app__DOT__pcap_parser__DOT__pcapfinished), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"pktSz", &(TOP.app__DOT__pcap_parser__DOT__pktSz), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"pktcount", &(TOP.app__DOT__pcap_parser__DOT__pktcount), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,7,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"r", &(TOP.app__DOT__pcap_parser__DOT__r), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"rg_available", &(TOP.app__DOT__pcap_parser__DOT__rg_available), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"rg_pktcount", &(TOP.app__DOT__pcap_parser__DOT__rg_pktcount), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,7,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"swapped", &(TOP.app__DOT__pcap_parser__DOT__swapped), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pcap_parser.varInsert(__Vfinal,"toNanos", &(TOP.app__DOT__pcap_parser__DOT__toNanos), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"HIT_WIDTH", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__pv_triggerer__DOT__HIT_WIDTH))), true, VLVT_REAL,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"MAX_INSTRUMENTS", const_cast<void*>(static_cast<const void*>(&(TOP.app__DOT__pv_triggerer__DOT__MAX_INSTRUMENTS))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"aggressor_side", &(TOP.app__DOT__pv_triggerer__DOT__aggressor_side), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,1,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"clk", &(TOP.app__DOT__pv_triggerer__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"fire", &(TOP.app__DOT__pv_triggerer__DOT__fire), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"price", &(TOP.app__DOT__pv_triggerer__DOT__price), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,1 ,63,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"price_triggers", &(TOP.app__DOT__pv_triggerer__DOT__price_triggers), false, VLVT_WDATA,VLVD_NODIR|VLVF_PUB_RW,2 ,127,0 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"rst", &(TOP.app__DOT__pv_triggerer__DOT__rst), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"rst_trigger", &(TOP.app__DOT__pv_triggerer__DOT__rst_trigger), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"security_id", &(TOP.app__DOT__pv_triggerer__DOT__security_id), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"security_id_triggers", &(TOP.app__DOT__pv_triggerer__DOT__security_id_triggers), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,2 ,31,0 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"set_trigger_fire", &(TOP.app__DOT__pv_triggerer__DOT__set_trigger_fire), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"size", &(TOP.app__DOT__pv_triggerer__DOT__size), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,31,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"size_triggers", &(TOP.app__DOT__pv_triggerer__DOT__size_triggers), false, VLVT_UINT64,VLVD_NODIR|VLVF_PUB_RW,2 ,63,0 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"state", &(TOP.app__DOT__pv_triggerer__DOT__state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,1 ,0,0);
        __Vscope_app__pv_triggerer.varInsert(__Vfinal,"valid", &(TOP.app__DOT__pv_triggerer__DOT__valid), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
    }
}
