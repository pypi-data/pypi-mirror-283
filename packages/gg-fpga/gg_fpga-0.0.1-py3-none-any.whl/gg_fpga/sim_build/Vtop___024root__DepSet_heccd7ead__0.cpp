// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_INLINE_OPT void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    // Body
    vlSelf->app__DOT__pcap_parser__DOT__pause = vlSelf->app__DOT__paused;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_ready 
        = vlSelf->app__DOT__aso_out_ready;
    vlSelf->app__DOT__pv_triggerer__DOT__rst_trigger 
        = vlSelf->app__DOT__rst_trigger;
    vlSelf->app__DOT__pv_triggerer__DOT__security_id_triggers[0U] 
        = vlSelf->app__DOT__security_id_triggers[0U];
    VL_ASSIGN_W(128,vlSelf->app__DOT__pv_triggerer__DOT__price_triggers
                [0U], vlSelf->app__DOT__price_triggers
                [0U]);
    vlSelf->app__DOT__pv_triggerer__DOT__size_triggers[0U] 
        = vlSelf->app__DOT__size_triggers[0U];
    vlSelf->app__DOT__aso_out_sop = vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop;
    vlSelf->app__DOT__aso_out_empty = vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty;
    vlSelf->app__DOT__aso_out_error = vlSelf->app__DOT__pcap_parser__DOT__aso_out_error;
    vlSelf->app__DOT__pcapfinished = vlSelf->app__DOT__pcap_parser__DOT__pcapfinished;
    vlSelf->app__DOT__pv_triggerer__DOT__fire = vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire;
    vlSelf->app__DOT__pcap_parser__DOT__available = vlSelf->app__DOT__pcap_parser__DOT__rg_available;
    vlSelf->app__DOT__aso_out_data = vlSelf->app__DOT__pcap_parser__DOT__aso_out_data;
    vlSelf->app__DOT__aso_out_valid = vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid;
    vlSelf->app__DOT__aso_out_eop = vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop;
    vlSelf->app__DOT__pcap_parser__DOT__pktcount = vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount;
    vlSelf->app__DOT__md_parser__DOT__out_valid = vlSelf->app__DOT__md_parser__DOT__set_out_valid;
    vlSelf->app__DOT__rst = vlSelf->rst;
    vlSelf->app__DOT__md_parser__DOT__out_security_id 
        = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x70U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_price = VL_SEL_QWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0xb0U, 0x40U);
    vlSelf->app__DOT__md_parser__DOT__out_size = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x90U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_side = (3U 
                                                  & VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x28U, 2U));
    vlSelf->app__DOT__clk = vlSelf->clk;
    vlSelf->app__DOT__fire = vlSelf->app__DOT__pv_triggerer__DOT__fire;
    vlSelf->app__DOT__available = vlSelf->app__DOT__pcap_parser__DOT__available;
    vlSelf->app__DOT__md_parser__DOT__rx = vlSelf->app__DOT__aso_out_data;
    vlSelf->app__DOT__md_parser__DOT__rx_valid = vlSelf->app__DOT__aso_out_valid;
    vlSelf->app__DOT__md_parser__DOT__rx_eop = vlSelf->app__DOT__aso_out_eop;
    vlSelf->app__DOT__pktcount = vlSelf->app__DOT__pcap_parser__DOT__pktcount;
    vlSelf->app__DOT__pv_triggerer__DOT__valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__md_parse_valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__md_parser__DOT__rst = vlSelf->app__DOT__rst;
    vlSelf->app__DOT__pv_triggerer__DOT__rst = vlSelf->app__DOT__rst;
    vlSelf->app__DOT__pv_triggerer__DOT__security_id 
        = vlSelf->app__DOT__md_parser__DOT__out_security_id;
    vlSelf->app__DOT__security_id = vlSelf->app__DOT__md_parser__DOT__out_security_id;
    vlSelf->app__DOT__pv_triggerer__DOT__price = vlSelf->app__DOT__md_parser__DOT__out_price;
    vlSelf->app__DOT__price = vlSelf->app__DOT__md_parser__DOT__out_price;
    vlSelf->app__DOT__pv_triggerer__DOT__size = vlSelf->app__DOT__md_parser__DOT__out_size;
    vlSelf->app__DOT__size = vlSelf->app__DOT__md_parser__DOT__out_size;
    vlSelf->app__DOT__pv_triggerer__DOT__aggressor_side 
        = vlSelf->app__DOT__md_parser__DOT__out_side;
    vlSelf->app__DOT__side = vlSelf->app__DOT__md_parser__DOT__out_side;
    vlSelf->app__DOT__pcap_parser__DOT__clk_out = vlSelf->app__DOT__clk;
    vlSelf->app__DOT__md_parser__DOT__clk = vlSelf->app__DOT__clk;
    vlSelf->app__DOT__pv_triggerer__DOT__clk = vlSelf->app__DOT__clk;
}

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    // Body
    if ((1ULL & vlSelf->__VicoTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelf->__VicoTriggered.any();
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_act(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_act\n"); );
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    // Body
    vlSelf->__Vdlyvset__app__DOT__fire_state__v0 = 0U;
    vlSelf->__Vdlyvset__app__DOT__fire_state__v1 = 0U;
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__1(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__1\n"); );
    // Body
    vlSelf->__Vdlyvset__app__DOT__price_triggers__v0 = 0U;
}

extern const VlWide<8>/*255:0*/ Vtop__ConstPool__CONST_h9e67c271_0;
extern const VlWide<9>/*287:0*/ Vtop__ConstPool__CONST_hc5471b50_0;
extern const VlWide<8>/*255:0*/ Vtop__ConstPool__CONST_h7f3586b3_0;

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__2(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__2\n"); );
    // Init
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__0__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__0__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__0__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__0__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__0__size;
    __Vfunc_reverse_bytes__0__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__1__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__1__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__1__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__1__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__1__size;
    __Vfunc_reverse_bytes__1__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__2__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__2__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__2__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__2__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__2__size;
    __Vfunc_reverse_bytes__2__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__3__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__3__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__3__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__3__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__3__size;
    __Vfunc_reverse_bytes__3__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__4__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__4__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__4__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__4__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__4__size;
    __Vfunc_reverse_bytes__4__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__5__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__5__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__5__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__5__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__5__size;
    __Vfunc_reverse_bytes__5__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__6__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__6__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__6__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__6__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__6__size;
    __Vfunc_reverse_bytes__6__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__7__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__7__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__7__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__7__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__7__size;
    __Vfunc_reverse_bytes__7__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__8__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__8__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__8__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__8__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__8__size;
    __Vfunc_reverse_bytes__8__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__9__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__9__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__9__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__9__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__9__size;
    __Vfunc_reverse_bytes__9__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__10__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__10__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__10__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__10__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__10__size;
    __Vfunc_reverse_bytes__10__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__11__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__11__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__11__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__11__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__11__size;
    __Vfunc_reverse_bytes__11__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__12__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__12__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__12__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__12__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__12__size;
    __Vfunc_reverse_bytes__12__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__13__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__13__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__13__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__13__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__13__size;
    __Vfunc_reverse_bytes__13__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__14__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__14__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__14__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__14__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__14__size;
    __Vfunc_reverse_bytes__14__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i = 0;
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__15__Vfuncout;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__15__Vfuncout);
    VlWide<8>/*255:0*/ __Vfunc_reverse_bytes__15__data;
    VL_ZERO_W(256, __Vfunc_reverse_bytes__15__data);
    CData/*7:0*/ __Vfunc_reverse_bytes__15__size;
    __Vfunc_reverse_bytes__15__size = 0;
    IData/*31:0*/ __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i;
    __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i = 0;
    IData/*31:0*/ __Vdly__app__DOT__pcap_parser__DOT__diskSz;
    __Vdly__app__DOT__pcap_parser__DOT__diskSz = 0;
    CData/*0:0*/ __Vdly__app__DOT__pcap_parser__DOT__newpkt;
    __Vdly__app__DOT__pcap_parser__DOT__newpkt = 0;
    IData/*31:0*/ __Vdly__app__DOT__pcap_parser__DOT__countIPG;
    __Vdly__app__DOT__pcap_parser__DOT__countIPG = 0;
    CData/*0:0*/ __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop;
    __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop = 0;
    CData/*2:0*/ __Vdly__app__DOT__pcap_parser__DOT__aso_out_empty;
    __Vdly__app__DOT__pcap_parser__DOT__aso_out_empty = 0;
    SData/*15:0*/ __Vdly__app__DOT__md_parser__DOT__packet_idx;
    __Vdly__app__DOT__md_parser__DOT__packet_idx = 0;
    VlWide<3>/*79:0*/ __Vdly__app__DOT__md_parser__DOT__sbe_message_header;
    VL_ZERO_W(80, __Vdly__app__DOT__md_parser__DOT__sbe_message_header);
    SData/*15:0*/ __Vdly__app__DOT__md_parser__DOT__rx_rem;
    __Vdly__app__DOT__md_parser__DOT__rx_rem = 0;
    SData/*15:0*/ __Vdly__app__DOT__md_parser__DOT__grp_idx;
    __Vdly__app__DOT__md_parser__DOT__grp_idx = 0;
    SData/*15:0*/ __Vdly__app__DOT__md_parser__DOT__in_grp_idx;
    __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0;
    CData/*0:0*/ __Vdly__app__DOT__md_parser__DOT__parse_md_group;
    __Vdly__app__DOT__md_parser__DOT__parse_md_group = 0;
    CData/*0:0*/ __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size;
    __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size = 0;
    CData/*0:0*/ __Vdly__app__DOT__md_parser__DOT__parse_order_group;
    __Vdly__app__DOT__md_parser__DOT__parse_order_group = 0;
    CData/*7:0*/ __Vdly__app__DOT__md_parser__DOT__no_in_group;
    __Vdly__app__DOT__md_parser__DOT__no_in_group = 0;
    // Body
    __Vdly__app__DOT__pcap_parser__DOT__countIPG = vlSelf->app__DOT__pcap_parser__DOT__countIPG;
    __Vdly__app__DOT__pcap_parser__DOT__newpkt = vlSelf->app__DOT__pcap_parser__DOT__newpkt;
    __Vdly__app__DOT__pcap_parser__DOT__diskSz = vlSelf->app__DOT__pcap_parser__DOT__diskSz;
    __Vdly__app__DOT__pcap_parser__DOT__aso_out_empty 
        = vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty;
    __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop 
        = vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop;
    __Vdly__app__DOT__md_parser__DOT__no_in_group = vlSelf->app__DOT__md_parser__DOT__no_in_group;
    __Vdly__app__DOT__md_parser__DOT__parse_order_group 
        = vlSelf->app__DOT__md_parser__DOT__parse_order_group;
    __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size 
        = vlSelf->app__DOT__md_parser__DOT__parse_ord_grp_size;
    __Vdly__app__DOT__md_parser__DOT__parse_md_group 
        = vlSelf->app__DOT__md_parser__DOT__parse_md_group;
    __Vdly__app__DOT__md_parser__DOT__in_grp_idx = vlSelf->app__DOT__md_parser__DOT__in_grp_idx;
    __Vdly__app__DOT__md_parser__DOT__grp_idx = vlSelf->app__DOT__md_parser__DOT__grp_idx;
    __Vdly__app__DOT__md_parser__DOT__rx_rem = vlSelf->app__DOT__md_parser__DOT__rx_rem;
    VL_ASSIGN_W(80,__Vdly__app__DOT__md_parser__DOT__sbe_message_header, vlSelf->app__DOT__md_parser__DOT__sbe_message_header);
    __Vdly__app__DOT__md_parser__DOT__packet_idx = vlSelf->app__DOT__md_parser__DOT__packet_idx;
    vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v0 = 0U;
    vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v1 = 0U;
    if ((1U & ((~ (IData)(vlSelf->rst)) | (~ (IData)(vlSelf->app__DOT__rst_trigger))))) {
        vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v0 = 1U;
    } else if (((~ vlSelf->app__DOT__pv_triggerer__DOT__state
                 [0U]) & (IData)(vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire))) {
        vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v1 = 1U;
    }
    if ((((0U == vlSelf->app__DOT__pcap_parser__DOT__eof) 
          & (0U == vlSelf->app__DOT__pcap_parser__DOT__diskSz)) 
         & (0U == vlSelf->app__DOT__pcap_parser__DOT__countIPG))) {
        vlSelf->app__DOT__pcap_parser__DOT__r = VL_FREAD_I(8
                                                           ,0
                                                           ,16
                                                           , &(vlSelf->app__DOT__pcap_parser__DOT__packet_header)
                                                           , vlSelf->app__DOT__pcap_parser__DOT__file
                                                           , 0
                                                           , 16);
        vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount 
            = (0xffU & ((IData)(1U) + (IData)(vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount)));
        if ((1U == vlSelf->app__DOT__pcap_parser__DOT__swapped)) {
            vlSelf->app__DOT__pcap_parser__DOT__pktSz 
                = VL_CONCAT_III(32,8,24, vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                [0xbU], VL_CONCAT_III(24,8,16, 
                                                      vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                      [0xaU], 
                                                      VL_CONCAT_III(16,8,8, 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [9U], 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [8U])));
            __Vdly__app__DOT__pcap_parser__DOT__diskSz 
                = VL_CONCAT_III(32,8,24, vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                [0xfU], VL_CONCAT_III(24,8,16, 
                                                      vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                      [0xeU], 
                                                      VL_CONCAT_III(16,8,8, 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [0xdU], 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [0xcU])));
        } else {
            vlSelf->app__DOT__pcap_parser__DOT__pktSz 
                = VL_CONCAT_III(32,8,24, vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                [8U], VL_CONCAT_III(24,8,16, 
                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                    [9U], 
                                                    VL_CONCAT_III(16,8,8, 
                                                                  vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                  [0xaU], 
                                                                  vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                  [0xbU])));
            __Vdly__app__DOT__pcap_parser__DOT__diskSz 
                = VL_CONCAT_III(32,8,24, vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                [0xcU], VL_CONCAT_III(24,8,16, 
                                                      vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                      [0xdU], 
                                                      VL_CONCAT_III(16,8,8, 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [0xeU], 
                                                                    vlSelf->app__DOT__pcap_parser__DOT__packet_header
                                                                    [0xfU])));
        }
        vlSelf->app__DOT__pcap_parser__DOT__rg_available = 1U;
        __Vdly__app__DOT__pcap_parser__DOT__newpkt = 1U;
        __Vdly__app__DOT__pcap_parser__DOT__countIPG = 4U;
        __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_data = 0x7070707fb555555ULL;
    } else if (VL_LTS_III(32, 0U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)) {
        if (vlSelf->app__DOT__paused) {
            vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 0U;
        } else {
            __Vdly__app__DOT__pcap_parser__DOT__diskSz 
                = (VL_LTS_III(32, 7U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                    ? (vlSelf->app__DOT__pcap_parser__DOT__diskSz 
                       - (IData)(8U)) : 0U);
            vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop 
                = vlSelf->app__DOT__pcap_parser__DOT__newpkt;
            __Vdly__app__DOT__pcap_parser__DOT__aso_out_empty 
                = (7U & VL_SEL_IIII(32, (VL_LTS_III(32, 8U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                          ? 0U : ((IData)(8U) 
                                                  - vlSelf->app__DOT__pcap_parser__DOT__diskSz)), 0U, 3U));
            __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop 
                = VL_GTES_III(32, 8U, vlSelf->app__DOT__pcap_parser__DOT__diskSz);
            __Vdly__app__DOT__pcap_parser__DOT__newpkt = 0U;
            VL_ASSIGNSEL_QI(64,8,0U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 0U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,8U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 1U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x10U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 2U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x18U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 3U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x20U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 4U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x28U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 5U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x30U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 6U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            VL_ASSIGNSEL_QI(64,8,0x38U, vlSelf->app__DOT__pcap_parser__DOT__aso_out_data, 
                            (0xffU & VL_SEL_IIII(32, 
                                                 (VL_LTS_III(32, 7U, vlSelf->app__DOT__pcap_parser__DOT__diskSz)
                                                   ? 
                                                  (vlSelf->app__DOT__pcap_parser__DOT__file ? fgetc(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : -1)
                                                   : 0U), 0U, 8U)));
            vlSelf->app__DOT__pcap_parser__DOT__eof 
                = (vlSelf->app__DOT__pcap_parser__DOT__file ? feof(VL_CVT_I_FP(vlSelf->app__DOT__pcap_parser__DOT__file)) : true);
            if (((0U != vlSelf->app__DOT__pcap_parser__DOT__eof) 
                 | (1U == vlSelf->app__DOT__pcap_parser__DOT__diskSz))) {
                vlSelf->app__DOT__pcap_parser__DOT__rg_available = 0U;
            } else {
                vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 1U;
            }
        }
    } else if (VL_LTS_III(32, 0U, vlSelf->app__DOT__pcap_parser__DOT__countIPG)) {
        __Vdly__app__DOT__pcap_parser__DOT__countIPG 
            = (vlSelf->app__DOT__pcap_parser__DOT__countIPG 
               - (IData)(1U));
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_data 
            = (((0U == (IData)(vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty)) 
                & (IData)(vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop))
                ? 0xfd00000000000000ULL : 0ULL);
        __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop = 0U;
    } else if ((0U != vlSelf->app__DOT__pcap_parser__DOT__eof)) {
        vlSelf->app__DOT__pcap_parser__DOT__pcapfinished = 1U;
        __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__aso_out_data = 0ULL;
    }
    if (vlSelf->rst) {
        if (vlSelf->app__DOT__aso_out_valid) {
            __Vdly__app__DOT__md_parser__DOT__packet_idx 
                = (0xffffU & ((IData)(1U) + (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx)));
            if (((((((((0U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx)) 
                       | (1U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                      | (2U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                     | (3U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                    | (4U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                   | (5U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                  | (6U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) 
                 | (7U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx)))) {
                if ((0U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WQ(272,48,0xe0U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffffffffffULL 
                                     & VL_SEL_QWII(256, 
                                                   ([&]() {
                                        __Vfunc_reverse_bytes__0__size = 6U;
                                        VL_EXTEND_WQ(256,48, __Vfunc_reverse_bytes__0__data, 
                                                     (0xffffffffffffULL 
                                                      & VL_SEL_QQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x30U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__0__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__0__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__0__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__0__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__0__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__0__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__0__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__0__Vfuncout), 0U, 0x30U)));
                    VL_ASSIGNSEL_WI(272,16,0xd0U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__1__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__1__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__1__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__1__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__1__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__1__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__1__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__1__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__1__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__1__Vfuncout), 0U, 0x10U)));
                } else if ((1U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WI(272,32,0xb0U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    VL_SEL_IWII(256, 
                                                ([&]() {
                                    __Vfunc_reverse_bytes__2__size = 4U;
                                    VL_EXTEND_WI(256,32, __Vfunc_reverse_bytes__2__data, 
                                                 VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x20U));
                                    VL_ASSIGN_W(256,__Vfunc_reverse_bytes__2__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                    __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i = 0U;
                                    while ((__Vfunc_reverse_bytes__2__unnamedblk1__DOT__i 
                                            < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__2__size)))) {
                                        VL_ASSIGNSEL_WI(256,8,
                                                        (0xffU 
                                                         & VL_SEL_IIII(32, 
                                                                       VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__2__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__2__Vfuncout, 
                                                        (0xffU 
                                                         & VL_SEL_IWII(256, __Vfunc_reverse_bytes__2__data, 
                                                                       (0xffU 
                                                                        & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                        __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i 
                                            = ((IData)(1U) 
                                               + __Vfunc_reverse_bytes__2__unnamedblk1__DOT__i);
                                    }
                                }(), __Vfunc_reverse_bytes__2__Vfuncout), 0U, 0x20U));
                    VL_ASSIGNSEL_WI(272,16,0xa0U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__3__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__3__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x20U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__3__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__3__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__3__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__3__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__3__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__3__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__3__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__3__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(272,16,0x90U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__4__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__4__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__4__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__4__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__4__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__4__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__4__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__4__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__4__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__4__Vfuncout), 0U, 0x10U)));
                } else if ((2U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WI(272,16,0x80U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__5__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__5__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__5__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__5__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__5__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__5__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__5__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__5__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__5__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__5__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(272,16,0x70U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__6__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__6__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__6__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__6__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__6__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__6__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__6__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__6__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__6__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__6__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(272,16,0x60U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__7__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__7__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x20U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__7__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__7__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__7__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__7__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__7__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__7__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__7__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__7__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(272,16,0x50U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    VL_CONCAT_III(16,8,8, 
                                                  (0xffU 
                                                   & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 8U)), 
                                                  (0xffU 
                                                   & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x38U, 8U))));
                } else if ((3U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WI(272,16,0x40U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__8__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__8__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__8__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__8__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__8__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__8__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__8__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__8__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__8__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__8__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(272,32,0x20U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    VL_SEL_IWII(256, 
                                                ([&]() {
                                    __Vfunc_reverse_bytes__9__size = 4U;
                                    VL_EXTEND_WI(256,32, __Vfunc_reverse_bytes__9__data, 
                                                 VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x20U));
                                    VL_ASSIGN_W(256,__Vfunc_reverse_bytes__9__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                    __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i = 0U;
                                    while ((__Vfunc_reverse_bytes__9__unnamedblk1__DOT__i 
                                            < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__9__size)))) {
                                        VL_ASSIGNSEL_WI(256,8,
                                                        (0xffU 
                                                         & VL_SEL_IIII(32, 
                                                                       VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__9__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__9__Vfuncout, 
                                                        (0xffU 
                                                         & VL_SEL_IWII(256, __Vfunc_reverse_bytes__9__data, 
                                                                       (0xffU 
                                                                        & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                        __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i 
                                            = ((IData)(1U) 
                                               + __Vfunc_reverse_bytes__9__unnamedblk1__DOT__i);
                                    }
                                }(), __Vfunc_reverse_bytes__9__Vfuncout), 0U, 0x20U));
                    VL_ASSIGNSEL_WI(272,17,0xfU, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0x1ffffU & VL_SEL_IWII(256, 
                                                            ([&]() {
                                        __Vfunc_reverse_bytes__10__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__10__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__10__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__10__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__10__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__10__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__10__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__10__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__10__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__10__Vfuncout), 0U, 0x11U)));
                } else if ((4U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WI(272,16,0U, vlSelf->app__DOT__md_parser__DOT__ip_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__11__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__11__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__11__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__11__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__11__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__11__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__11__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__11__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__11__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__11__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_QI(64,16,0x30U, vlSelf->app__DOT__md_parser__DOT__udp_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__12__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__12__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__12__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__12__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__12__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__12__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__12__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__12__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__12__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__12__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_QI(64,16,0x20U, vlSelf->app__DOT__md_parser__DOT__udp_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__13__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__13__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x20U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__13__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__13__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__13__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__13__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__13__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__13__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__13__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__13__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_QI(64,16,0x10U, vlSelf->app__DOT__md_parser__DOT__udp_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__14__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__14__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__14__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__14__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__14__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__14__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__14__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__14__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__14__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__14__Vfuncout), 0U, 0x10U)));
                } else if ((5U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_QI(64,16,0U, vlSelf->app__DOT__md_parser__DOT__udp_header, 
                                    (0xffffU & VL_SEL_IWII(256, 
                                                           ([&]() {
                                        __Vfunc_reverse_bytes__15__size = 2U;
                                        VL_EXTEND_WI(256,16, __Vfunc_reverse_bytes__15__data, 
                                                     (0xffffU 
                                                      & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)));
                                        VL_ASSIGN_W(256,__Vfunc_reverse_bytes__15__Vfuncout, Vtop__ConstPool__CONST_h9e67c271_0);
                                        __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i = 0U;
                                        while ((__Vfunc_reverse_bytes__15__unnamedblk1__DOT__i 
                                                < VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__15__size)))) {
                                            VL_ASSIGNSEL_WI(256,8,
                                                            (0xffU 
                                                             & VL_SEL_IIII(32, 
                                                                           VL_SHIFTL_III(32,32,32, 
                                                                                ((VL_EXTEND_II(32,8, (IData)(__Vfunc_reverse_bytes__15__size)) 
                                                                                - (IData)(1U)) 
                                                                                - __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i), 3U), 0U, 8U)), __Vfunc_reverse_bytes__15__Vfuncout, 
                                                            (0xffU 
                                                             & VL_SEL_IWII(256, __Vfunc_reverse_bytes__15__data, 
                                                                           (0xffU 
                                                                            & VL_SEL_IIII(32, 
                                                                                VL_MULS_III(32, (IData)(8U), __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i), 0U, 8U)), 8U)));
                                            __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i 
                                                = ((IData)(1U) 
                                                   + __Vfunc_reverse_bytes__15__unnamedblk1__DOT__i);
                                        }
                                    }(), __Vfunc_reverse_bytes__15__Vfuncout), 0U, 0x10U)));
                    VL_ASSIGNSEL_WI(96,32,0x40U, vlSelf->app__DOT__md_parser__DOT__packet_header, 
                                    VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x20U));
                    VL_ASSIGNSEL_WI(96,16,0U, vlSelf->app__DOT__md_parser__DOT__packet_header, 
                                    (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                } else if ((6U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WQ(96,48,0x10U, vlSelf->app__DOT__md_parser__DOT__packet_header, 
                                    (0xffffffffffffULL 
                                     & VL_SEL_QQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x30U)));
                    VL_ASSIGNSEL_WI(80,16,0x40U, __Vdly__app__DOT__md_parser__DOT__sbe_message_header, 
                                    (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                } else {
                    VL_ASSIGNSEL_WQ(80,48,0x10U, __Vdly__app__DOT__md_parser__DOT__sbe_message_header, 
                                    VL_CONCAT_QII(48,32,16, 
                                                  VL_CONCAT_III(32,16,16, 
                                                                (0xffffU 
                                                                 & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)), 
                                                                (0xffffU 
                                                                 & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x10U))), 
                                                  (0xffffU 
                                                   & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x20U, 0x10U))));
                    VL_ASSIGNSEL_WI(80,16,0U, __Vdly__app__DOT__md_parser__DOT__sbe_message_header, 
                                    (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U)));
                }
            }
            if (vlSelf->app__DOT__aso_out_eop) {
                __Vdly__app__DOT__md_parser__DOT__rx_rem = 0U;
                __Vdly__app__DOT__md_parser__DOT__packet_idx = 0U;
                __Vdly__app__DOT__md_parser__DOT__grp_idx = 0U;
                __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
                __Vdly__app__DOT__md_parser__DOT__parse_md_group = 0U;
                __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size = 0U;
                __Vdly__app__DOT__md_parser__DOT__parse_order_group = 0U;
            }
            if ((0x30U == (0xffffU & VL_SEL_IWII(80, vlSelf->app__DOT__md_parser__DOT__sbe_message_header, 0x20U, 0x10U)))) {
                if ((8U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WQ(72,64,8U, vlSelf->app__DOT__md_parser__DOT__trade_summary, vlSelf->app__DOT__aso_out_data);
                } else if ((9U == (IData)(vlSelf->app__DOT__md_parser__DOT__packet_idx))) {
                    VL_ASSIGNSEL_WI(72,8,0U, vlSelf->app__DOT__md_parser__DOT__trade_summary, 
                                    (0xffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 8U)));
                    __Vdly__app__DOT__md_parser__DOT__no_in_group 
                        = (0xffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x28U, 8U));
                    __Vdly__app__DOT__md_parser__DOT__rx_rem 
                        = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                    __Vdly__app__DOT__md_parser__DOT__grp_idx = 0U;
                    __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
                    __Vdly__app__DOT__md_parser__DOT__parse_md_group = 1U;
                }
                if (vlSelf->app__DOT__md_parser__DOT__parse_md_group) {
                    __Vdly__app__DOT__md_parser__DOT__in_grp_idx 
                        = (0xffffU & ((IData)(1U) + (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx)));
                    if ((0U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        vlSelf->app__DOT__md_parser__DOT__set_out_valid = 0U;
                        VL_ASSIGNSEL_WQ(240,64,0xb0U, vlSelf->app__DOT__md_parser__DOT__md_entry, 
                                        VL_CONCAT_QQI(64,48,16, 
                                                      (0xffffffffffffULL 
                                                       & VL_SEL_QQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x30U)), (IData)(vlSelf->app__DOT__md_parser__DOT__rx_rem)));
                        __Vdly__app__DOT__md_parser__DOT__rx_rem 
                            = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                    } else if ((1U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        VL_ASSIGNSEL_WQ(240,64,0x70U, vlSelf->app__DOT__md_parser__DOT__md_entry, 
                                        VL_CONCAT_QII(64,32,32, 
                                                      VL_CONCAT_III(32,16,16, 
                                                                    (0xffffU 
                                                                     & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)), (IData)(vlSelf->app__DOT__md_parser__DOT__rx_rem)), 
                                                      VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x20U)));
                        __Vdly__app__DOT__md_parser__DOT__rx_rem 
                            = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                    } else if ((2U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        VL_ASSIGNSEL_WI(240,32,0x50U, vlSelf->app__DOT__md_parser__DOT__md_entry, 
                                        VL_CONCAT_III(32,16,16, 
                                                      (0xffffU 
                                                       & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)), (IData)(vlSelf->app__DOT__md_parser__DOT__rx_rem)));
                        vlSelf->app__DOT__md_parser__DOT__set_out_valid = 1U;
                        VL_ASSIGNSEL_WQ(240,48,0x20U, vlSelf->app__DOT__md_parser__DOT__md_entry, 
                                        VL_CONCAT_QII(48,32,16, 
                                                      VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x10U, 0x20U), 
                                                      VL_CONCAT_III(16,8,8, 
                                                                    (0xffU 
                                                                     & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 8U)), 
                                                                    (0xffU 
                                                                     & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x38U, 8U)))));
                    } else if ((3U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        VL_ASSIGNSEL_WI(240,32,0U, vlSelf->app__DOT__md_parser__DOT__md_entry, 
                                        VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x20U));
                        __Vdly__app__DOT__md_parser__DOT__rx_rem 
                            = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                        if ((((IData)(1U) + VL_EXTEND_II(32,16, (IData)(vlSelf->app__DOT__md_parser__DOT__grp_idx))) 
                             < VL_EXTEND_II(32,8, (IData)(vlSelf->app__DOT__md_parser__DOT__no_in_group)))) {
                            __Vdly__app__DOT__md_parser__DOT__grp_idx 
                                = (0xffffU & ((IData)(1U) 
                                              + (IData)(vlSelf->app__DOT__md_parser__DOT__grp_idx)));
                            __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
                        } else {
                            __Vdly__app__DOT__md_parser__DOT__parse_md_group = 0U;
                            __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size = 1U;
                        }
                    }
                }
                if (vlSelf->app__DOT__md_parser__DOT__parse_ord_grp_size) {
                    __Vdly__app__DOT__md_parser__DOT__no_in_group 
                        = (0xffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x28U, 8U));
                    __Vdly__app__DOT__md_parser__DOT__rx_rem 
                        = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                    __Vdly__app__DOT__md_parser__DOT__grp_idx = 0U;
                    __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
                    __Vdly__app__DOT__md_parser__DOT__parse_order_group = 1U;
                    __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size = 0U;
                    VL_CONST_W_1X(96,vlSelf->app__DOT__md_parser__DOT__order_entry,0x00000000);
                }
                if (vlSelf->app__DOT__md_parser__DOT__parse_order_group) {
                    __Vdly__app__DOT__md_parser__DOT__in_grp_idx 
                        = (0xffffU & ((IData)(1U) + (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx)));
                    if ((0U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        VL_ASSIGNSEL_WQ(96,64,0x20U, vlSelf->app__DOT__md_parser__DOT__order_entry, 
                                        VL_CONCAT_QQI(64,48,16, 
                                                      (0xffffffffffffULL 
                                                       & VL_SEL_QQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x30U)), (IData)(vlSelf->app__DOT__md_parser__DOT__rx_rem)));
                        __Vdly__app__DOT__md_parser__DOT__rx_rem 
                            = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                    } else if ((1U == (IData)(vlSelf->app__DOT__md_parser__DOT__in_grp_idx))) {
                        VL_ASSIGNSEL_WI(96,32,0U, vlSelf->app__DOT__md_parser__DOT__order_entry, 
                                        VL_CONCAT_III(32,16,16, 
                                                      (0xffffU 
                                                       & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0U, 0x10U)), (IData)(vlSelf->app__DOT__md_parser__DOT__rx_rem)));
                        if ((((IData)(1U) + VL_EXTEND_II(32,16, (IData)(vlSelf->app__DOT__md_parser__DOT__grp_idx))) 
                             < VL_EXTEND_II(32,8, (IData)(vlSelf->app__DOT__md_parser__DOT__no_in_group)))) {
                            __Vdly__app__DOT__md_parser__DOT__grp_idx 
                                = (0xffffU & ((IData)(1U) 
                                              + (IData)(vlSelf->app__DOT__md_parser__DOT__grp_idx)));
                            __Vdly__app__DOT__md_parser__DOT__rx_rem 
                                = (0xffffU & VL_SEL_IQII(64, vlSelf->app__DOT__aso_out_data, 0x30U, 0x10U));
                            __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
                        } else {
                            __Vdly__app__DOT__md_parser__DOT__parse_order_group = 0U;
                            __Vdly__app__DOT__md_parser__DOT__packet_idx = 0U;
                        }
                    }
                }
            }
        }
    } else {
        __Vdly__app__DOT__md_parser__DOT__grp_idx = 0U;
        __Vdly__app__DOT__md_parser__DOT__in_grp_idx = 0U;
        __Vdly__app__DOT__md_parser__DOT__parse_md_group = 0U;
        __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size = 0U;
        __Vdly__app__DOT__md_parser__DOT__parse_order_group = 0U;
        VL_ASSIGN_W(272,vlSelf->app__DOT__md_parser__DOT__ip_header, Vtop__ConstPool__CONST_hc5471b50_0);
        vlSelf->app__DOT__md_parser__DOT__udp_header = 0ULL;
        VL_CONST_W_1X(96,vlSelf->app__DOT__md_parser__DOT__packet_header,0x00000000);
        VL_CONST_W_1X(80,__Vdly__app__DOT__md_parser__DOT__sbe_message_header,0x00000000);
        VL_CONST_W_1X(72,vlSelf->app__DOT__md_parser__DOT__trade_summary,0x00000000);
        VL_ASSIGN_W(240,vlSelf->app__DOT__md_parser__DOT__md_entry, Vtop__ConstPool__CONST_h7f3586b3_0);
        VL_CONST_W_1X(96,vlSelf->app__DOT__md_parser__DOT__order_entry,0x00000000);
        __Vdly__app__DOT__md_parser__DOT__packet_idx = 0U;
        vlSelf->app__DOT__md_parser__DOT__set_out_valid = 0U;
    }
    vlSelf->app__DOT__pcap_parser__DOT__diskSz = __Vdly__app__DOT__pcap_parser__DOT__diskSz;
    vlSelf->app__DOT__pcap_parser__DOT__newpkt = __Vdly__app__DOT__pcap_parser__DOT__newpkt;
    vlSelf->app__DOT__pcap_parser__DOT__countIPG = __Vdly__app__DOT__pcap_parser__DOT__countIPG;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty 
        = __Vdly__app__DOT__pcap_parser__DOT__aso_out_empty;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop 
        = __Vdly__app__DOT__pcap_parser__DOT__aso_out_eop;
    vlSelf->app__DOT__md_parser__DOT__packet_idx = __Vdly__app__DOT__md_parser__DOT__packet_idx;
    VL_ASSIGN_W(80,vlSelf->app__DOT__md_parser__DOT__sbe_message_header, __Vdly__app__DOT__md_parser__DOT__sbe_message_header);
    vlSelf->app__DOT__md_parser__DOT__rx_rem = __Vdly__app__DOT__md_parser__DOT__rx_rem;
    vlSelf->app__DOT__md_parser__DOT__grp_idx = __Vdly__app__DOT__md_parser__DOT__grp_idx;
    vlSelf->app__DOT__md_parser__DOT__in_grp_idx = __Vdly__app__DOT__md_parser__DOT__in_grp_idx;
    vlSelf->app__DOT__md_parser__DOT__parse_md_group 
        = __Vdly__app__DOT__md_parser__DOT__parse_md_group;
    vlSelf->app__DOT__md_parser__DOT__parse_ord_grp_size 
        = __Vdly__app__DOT__md_parser__DOT__parse_ord_grp_size;
    vlSelf->app__DOT__md_parser__DOT__parse_order_group 
        = __Vdly__app__DOT__md_parser__DOT__parse_order_group;
    vlSelf->app__DOT__md_parser__DOT__no_in_group = __Vdly__app__DOT__md_parser__DOT__no_in_group;
    vlSelf->app__DOT__aso_out_sop = vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop;
    vlSelf->app__DOT__aso_out_empty = vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty;
    vlSelf->app__DOT__pcapfinished = vlSelf->app__DOT__pcap_parser__DOT__pcapfinished;
    vlSelf->app__DOT__pcap_parser__DOT__pktcount = vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount;
    vlSelf->app__DOT__pcap_parser__DOT__available = vlSelf->app__DOT__pcap_parser__DOT__rg_available;
    vlSelf->app__DOT__aso_out_eop = vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop;
    vlSelf->app__DOT__aso_out_valid = vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid;
    vlSelf->app__DOT__aso_out_data = vlSelf->app__DOT__pcap_parser__DOT__aso_out_data;
    if ((1U & (~ (IData)(vlSelf->rst)))) {
        vlSelf->app__DOT__paused = 0U;
    }
    vlSelf->app__DOT__md_parser__DOT__out_valid = vlSelf->app__DOT__md_parser__DOT__set_out_valid;
    vlSelf->app__DOT__pktcount = vlSelf->app__DOT__pcap_parser__DOT__pktcount;
    vlSelf->app__DOT__available = vlSelf->app__DOT__pcap_parser__DOT__available;
    vlSelf->app__DOT__md_parser__DOT__rx_eop = vlSelf->app__DOT__aso_out_eop;
    vlSelf->app__DOT__md_parser__DOT__rx_valid = vlSelf->app__DOT__aso_out_valid;
    vlSelf->app__DOT__md_parser__DOT__rx = vlSelf->app__DOT__aso_out_data;
    vlSelf->app__DOT__pv_triggerer__DOT__valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__md_parse_valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__pcap_parser__DOT__pause = vlSelf->app__DOT__paused;
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__4(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__4\n"); );
    // Body
    if ((1U & ((~ (IData)(vlSelf->rst)) | (~ (IData)(vlSelf->app__DOT__rst_trigger))))) {
        vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire = 0U;
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__5(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__5\n"); );
    // Body
    if (((((IData)(vlSelf->rst) & (IData)(vlSelf->app__DOT__rst_trigger)) 
          & (~ vlSelf->app__DOT__pv_triggerer__DOT__state
             [0U])) & (vlSelf->app__DOT__md_parser__DOT__out_security_id 
                       == vlSelf->app__DOT__security_id_triggers
                       [0U]))) {
        if ((1U == (IData)(vlSelf->app__DOT__md_parser__DOT__out_side))) {
            if (((vlSelf->app__DOT__md_parser__DOT__out_price 
                  >= VL_SEL_QWII(128, vlSelf->app__DOT__price_triggers
                                 [0U], 0x40U, 0x40U)) 
                 & (vlSelf->app__DOT__md_parser__DOT__out_size 
                    >= VL_SEL_IQII(64, vlSelf->app__DOT__size_triggers
                                   [0U], 0x20U, 0x20U)))) {
                vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire = 1U;
            }
        } else if ((2U == (IData)(vlSelf->app__DOT__md_parser__DOT__out_side))) {
            if (((vlSelf->app__DOT__md_parser__DOT__out_price 
                  <= VL_SEL_QWII(128, vlSelf->app__DOT__price_triggers
                                 [0U], 0U, 0x40U)) 
                 & (vlSelf->app__DOT__md_parser__DOT__out_size 
                    >= VL_SEL_IQII(64, vlSelf->app__DOT__size_triggers
                                   [0U], 0U, 0x20U)))) {
                vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire = 1U;
            }
        }
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__6(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__6\n"); );
    // Body
    if (vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v0) {
        vlSelf->app__DOT__pv_triggerer__DOT__state[0U] = 0U;
    }
    if (vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v1) {
        vlSelf->app__DOT__pv_triggerer__DOT__state[0U] = 1U;
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__9(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__9\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->rst)))) {
        vlSelf->app__DOT__rst_trigger = 1U;
    }
    if (vlSelf->app__DOT__fire_state[0U]) {
        if (vlSelf->app__DOT__fire_state[0U]) {
            vlSelf->app__DOT__rst_trigger = 1U;
            vlSelf->__Vdlyvset__app__DOT__fire_state__v0 = 1U;
        }
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__10(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__10\n"); );
    // Init
    CData/*6:0*/ __Vdlyvlsb__app__DOT__price_triggers__v0;
    __Vdlyvlsb__app__DOT__price_triggers__v0 = 0;
    QData/*63:0*/ __Vdlyvval__app__DOT__price_triggers__v0;
    __Vdlyvval__app__DOT__price_triggers__v0 = 0;
    CData/*6:0*/ __Vdlyvlsb__app__DOT__price_triggers__v1;
    __Vdlyvlsb__app__DOT__price_triggers__v1 = 0;
    QData/*63:0*/ __Vdlyvval__app__DOT__price_triggers__v1;
    __Vdlyvval__app__DOT__price_triggers__v1 = 0;
    // Body
    if (VL_UNLIKELY(((IData)(vlSelf->app__DOT__pv_triggerer__DOT__fire) 
                     & (~ vlSelf->app__DOT__fire_state
                        [0U])))) {
        VL_WRITEF("fire: i: 0 security_id: %0# price: %0# size: %0# side: %0#\n",
                  32,vlSelf->app__DOT__md_parser__DOT__out_security_id,
                  64,vlSelf->app__DOT__md_parser__DOT__out_price,
                  32,vlSelf->app__DOT__md_parser__DOT__out_size,
                  2,(IData)(vlSelf->app__DOT__md_parser__DOT__out_side));
        __Vdlyvval__app__DOT__price_triggers__v0 = 
            (0x5d21dba00ULL + vlSelf->app__DOT__md_parser__DOT__out_price);
        vlSelf->__Vdlyvset__app__DOT__price_triggers__v0 = 1U;
        __Vdlyvlsb__app__DOT__price_triggers__v0 = 0x40U;
        vlSelf->app__DOT__rst_trigger = 0U;
        vlSelf->__Vdlyvset__app__DOT__fire_state__v1 = 1U;
        __Vdlyvval__app__DOT__price_triggers__v1 = 
            (vlSelf->app__DOT__md_parser__DOT__out_price 
             - 0x5d21dba00ULL);
        __Vdlyvlsb__app__DOT__price_triggers__v1 = 0U;
    }
    if (vlSelf->__Vdlyvset__app__DOT__price_triggers__v0) {
        VL_ASSIGNSEL_WQ(128,64,(IData)(__Vdlyvlsb__app__DOT__price_triggers__v0), 
                        vlSelf->app__DOT__price_triggers
                        [0U], __Vdlyvval__app__DOT__price_triggers__v0);
    }
    if (vlSelf->__Vdlyvset__app__DOT__fire_state__v1) {
        VL_ASSIGNSEL_WQ(128,64,(IData)(__Vdlyvlsb__app__DOT__price_triggers__v1), 
                        vlSelf->app__DOT__price_triggers
                        [0U], __Vdlyvval__app__DOT__price_triggers__v1);
    }
    VL_ASSIGN_W(128,vlSelf->app__DOT__pv_triggerer__DOT__price_triggers
                [0U], vlSelf->app__DOT__price_triggers
                [0U]);
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__11(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__11\n"); );
    // Body
    vlSelf->app__DOT__pv_triggerer__DOT__fire = vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire;
    vlSelf->app__DOT__fire = vlSelf->app__DOT__pv_triggerer__DOT__fire;
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__12(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__12\n"); );
    // Body
    if (vlSelf->__Vdlyvset__app__DOT__fire_state__v0) {
        vlSelf->app__DOT__fire_state[0U] = 0U;
    }
    if (vlSelf->__Vdlyvset__app__DOT__fire_state__v1) {
        vlSelf->app__DOT__fire_state[0U] = 1U;
    }
    vlSelf->app__DOT__pv_triggerer__DOT__rst_trigger 
        = vlSelf->app__DOT__rst_trigger;
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__13(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__13\n"); );
    // Body
    vlSelf->app__DOT__md_parser__DOT__out_security_id 
        = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x70U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_price = VL_SEL_QWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0xb0U, 0x40U);
    vlSelf->app__DOT__md_parser__DOT__out_size = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x90U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_side = (3U 
                                                  & VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x28U, 2U));
    vlSelf->app__DOT__pv_triggerer__DOT__security_id 
        = vlSelf->app__DOT__md_parser__DOT__out_security_id;
    vlSelf->app__DOT__security_id = vlSelf->app__DOT__md_parser__DOT__out_security_id;
    vlSelf->app__DOT__pv_triggerer__DOT__price = vlSelf->app__DOT__md_parser__DOT__out_price;
    vlSelf->app__DOT__price = vlSelf->app__DOT__md_parser__DOT__out_price;
    vlSelf->app__DOT__pv_triggerer__DOT__size = vlSelf->app__DOT__md_parser__DOT__out_size;
    vlSelf->app__DOT__size = vlSelf->app__DOT__md_parser__DOT__out_size;
    vlSelf->app__DOT__pv_triggerer__DOT__aggressor_side 
        = vlSelf->app__DOT__md_parser__DOT__out_side;
    vlSelf->app__DOT__side = vlSelf->app__DOT__md_parser__DOT__out_side;
}

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    // Body
    if ((0x10ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__1(vlSelf);
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__2(vlSelf);
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__4(vlSelf);
    }
    if ((4ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__5(vlSelf);
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__6(vlSelf);
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__9(vlSelf);
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__10(vlSelf);
    }
    if ((8ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__11(vlSelf);
    }
    if ((0x10ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__12(vlSelf);
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__13(vlSelf);
    }
}

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    // Init
    VlTriggerVec<5> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelf->__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelf->__VactTriggered, vlSelf->__VnbaTriggered);
        vlSelf->__VnbaTriggered.thisOr(vlSelf->__VactTriggered);
        Vtop___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelf->__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        vlSelf->__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelf->__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY((0x64U < __VicoIterCount))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/app.sv", 37, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vtop___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelf->__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/app.sv", 37, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelf->__VactIterCount = 0U;
        vlSelf->__VactContinue = 1U;
        while (vlSelf->__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelf->__VactIterCount))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/app.sv", 37, "", "Active region did not converge.");
            }
            vlSelf->__VactIterCount = ((IData)(1U) 
                                       + vlSelf->__VactIterCount);
            vlSelf->__VactContinue = 0U;
            if (Vtop___024root___eval_phase__act(vlSelf)) {
                vlSelf->__VactContinue = 1U;
            }
        }
        if (Vtop___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((vlSelf->clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelf->rst & 0xfeU))) {
        Verilated::overWidthError("rst");}
}
#endif  // VL_DEBUG
