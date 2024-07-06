// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop__Syms.h"
#include "Vtop___024root.h"

// Parameter definitions for Vtop___024root
constexpr CData/*0:0*/ Vtop___024root::app__DOT__TRIGGER_MODE;
constexpr CData/*1:0*/ Vtop___024root::app__DOT__HITTING_MODE;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__DURATION;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__SECURITY_ID;
constexpr VlWide<15>/*479:0*/ Vtop___024root::app__DOT__PCAP_PATH;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__SIZE_LO;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__SIZE_HI;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__NUM_INSTRUMENTS;
constexpr VlWide<15>/*479:0*/ Vtop___024root::app__DOT__pcap_parser__DOT__pcap_filename;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__pcap_parser__DOT__ipg;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__MDIncrementalRefreshTradeSummaryID;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__ipv4_header_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__udp_header_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__packet_header_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__sbe_message_header_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__trade_summary_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__trade_summary_pad;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__md_entry_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__md_entry_pad;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__order_entry_len;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__md_parser__DOT__order_entry_pad;
constexpr IData/*31:0*/ Vtop___024root::app__DOT__pv_triggerer__DOT__MAX_INSTRUMENTS;
constexpr QData/*63:0*/ Vtop___024root::app__DOT__PRICE_LO;
constexpr QData/*63:0*/ Vtop___024root::app__DOT__PRICE_HI;
constexpr QData/*63:0*/ Vtop___024root::app__DOT__HIT_WIDTH;
constexpr double Vtop___024root::app__DOT__pv_triggerer__DOT__HIT_WIDTH;


void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf);

Vtop___024root::Vtop___024root(Vtop__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vtop___024root___ctor_var_reset(this);
}

void Vtop___024root::__Vconfigure(bool first) {
    if (false && first) {}  // Prevent unused
}

Vtop___024root::~Vtop___024root() {
}
