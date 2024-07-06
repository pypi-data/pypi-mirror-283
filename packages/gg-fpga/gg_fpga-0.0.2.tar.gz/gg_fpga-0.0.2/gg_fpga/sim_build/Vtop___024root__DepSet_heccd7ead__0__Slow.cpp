// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___eval_static__TOP(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    // Body
    Vtop___024root___eval_static__TOP(vlSelf);
}

VL_ATTR_COLD void Vtop___024root___eval_static__TOP(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static__TOP\n"); );
    // Init
    VlWide<4>/*127:0*/ __Vtemp_1;
    // Body
    vlSelf->app__DOT__security_id_triggers[0U] = 0xd75U;
    VL_CONST_W_4X(128,__Vtemp_1,0x00019c97,0x9f1a3400,0x00019c8b,0xfadec000);
    VL_ASSIGN_W(128,vlSelf->app__DOT__price_triggers
                [0U], __Vtemp_1);
    vlSelf->app__DOT__size_triggers[0U] = 0x100000001ULL;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_error = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__newpkt = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__pcapfinished = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__rg_available = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__swapped = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__toNanos = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__file = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__r = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__eof = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__i = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__pktSz = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__diskSz = 0U;
    vlSelf->app__DOT__pcap_parser__DOT__countIPG = 0U;
}

VL_ATTR_COLD void Vtop___024root___eval_initial__TOP(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    // Body
    Vtop___024root___eval_initial__TOP(vlSelf);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = vlSelf->clk;
    vlSelf->__Vtrigprevexpr_h32d5fd87__0 = ((IData)(vlSelf->clk) 
                                            & (IData)(vlSelf->rst));
    vlSelf->__Vtrigprevexpr___TOP__app__DOT__md_parser__DOT__out_valid__0 
        = vlSelf->app__DOT__md_parser__DOT__out_valid;
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelf->__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/app.sv", 37, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vtop___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelf->__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VstlTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___stl_sequent__TOP__0(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___stl_sequent__TOP__0\n"); );
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
    vlSelf->app__DOT__rst = vlSelf->rst;
    vlSelf->app__DOT__md_parser__DOT__out_security_id 
        = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x70U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_price = VL_SEL_QWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0xb0U, 0x40U);
    vlSelf->app__DOT__md_parser__DOT__out_size = VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x90U, 0x20U);
    vlSelf->app__DOT__md_parser__DOT__out_side = (3U 
                                                  & VL_SEL_IWII(240, vlSelf->app__DOT__md_parser__DOT__md_entry, 0x28U, 2U));
    vlSelf->app__DOT__md_parser__DOT__out_valid = vlSelf->app__DOT__md_parser__DOT__set_out_valid;
    vlSelf->app__DOT__clk = vlSelf->clk;
    vlSelf->app__DOT__fire = vlSelf->app__DOT__pv_triggerer__DOT__fire;
    vlSelf->app__DOT__available = vlSelf->app__DOT__pcap_parser__DOT__available;
    vlSelf->app__DOT__md_parser__DOT__rx = vlSelf->app__DOT__aso_out_data;
    vlSelf->app__DOT__md_parser__DOT__rx_valid = vlSelf->app__DOT__aso_out_valid;
    vlSelf->app__DOT__md_parser__DOT__rx_eop = vlSelf->app__DOT__aso_out_eop;
    vlSelf->app__DOT__pktcount = vlSelf->app__DOT__pcap_parser__DOT__pktcount;
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
    vlSelf->app__DOT__pv_triggerer__DOT__valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__md_parse_valid = vlSelf->app__DOT__md_parser__DOT__out_valid;
    vlSelf->app__DOT__pcap_parser__DOT__clk_out = vlSelf->app__DOT__clk;
    vlSelf->app__DOT__md_parser__DOT__clk = vlSelf->app__DOT__clk;
    vlSelf->app__DOT__pv_triggerer__DOT__clk = vlSelf->app__DOT__clk;
}

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    // Body
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        Vtop___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelf->__VstlTriggered.any();
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VicoTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VactTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge (clk & rst))\n");
    }
    if ((4ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 2 is active: @(posedge app.md_parser.out_valid)\n");
    }
    if ((8ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 3 is active: @(posedge app.md_parser.out_valid or posedge clk)\n");
    }
    if ((0x10ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 4 is active: @(posedge clk or posedge (clk & rst))\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__nba\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VnbaTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge (clk & rst))\n");
    }
    if ((4ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 2 is active: @(posedge app.md_parser.out_valid)\n");
    }
    if ((8ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 3 is active: @(posedge app.md_parser.out_valid or posedge clk)\n");
    }
    if ((0x10ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 4 is active: @(posedge clk or posedge (clk & rst))\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->rst = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__rst = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__fire_state[__Vi0] = 0;
    }
    vlSelf->app__DOT__paused = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__available = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pktcount = VL_RAND_RESET_I(8);
    vlSelf->app__DOT__pcapfinished = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__aso_out_data = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__aso_out_ready = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__aso_out_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__aso_out_sop = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__aso_out_empty = VL_RAND_RESET_I(3);
    vlSelf->app__DOT__aso_out_eop = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__aso_out_error = VL_RAND_RESET_I(6);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__security_id_triggers[__Vi0] = VL_RAND_RESET_I(32);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        VL_RAND_RESET_W(128, vlSelf->app__DOT__price_triggers[__Vi0]);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__size_triggers[__Vi0] = VL_RAND_RESET_Q(64);
    }
    vlSelf->app__DOT__security_id = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__price = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__size = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__side = VL_RAND_RESET_I(2);
    vlSelf->app__DOT__md_parse_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__fire = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__rst_trigger = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__pause = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__available = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_data = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_ready = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_sop = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_empty = VL_RAND_RESET_I(3);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_eop = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__aso_out_error = VL_RAND_RESET_I(6);
    vlSelf->app__DOT__pcap_parser__DOT__clk_out = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__pktcount = VL_RAND_RESET_I(8);
    vlSelf->app__DOT__pcap_parser__DOT__newpkt = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__pcapfinished = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__rg_available = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pcap_parser__DOT__rg_pktcount = VL_RAND_RESET_I(8);
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->app__DOT__pcap_parser__DOT__global_header[__Vi0] = VL_RAND_RESET_I(8);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->app__DOT__pcap_parser__DOT__packet_header[__Vi0] = VL_RAND_RESET_I(8);
    }
    vlSelf->app__DOT__pcap_parser__DOT__swapped = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__toNanos = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__file = 0;
    vlSelf->app__DOT__pcap_parser__DOT__r = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__eof = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__i = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__pktSz = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__diskSz = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pcap_parser__DOT__countIPG = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__md_parser__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__rst = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__rx = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__md_parser__DOT__rx_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__rx_eop = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__out_security_id = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__md_parser__DOT__out_price = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__md_parser__DOT__out_size = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__md_parser__DOT__out_side = VL_RAND_RESET_I(2);
    vlSelf->app__DOT__md_parser__DOT__out_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__packet_idx = VL_RAND_RESET_I(16);
    VL_RAND_RESET_W(272, vlSelf->app__DOT__md_parser__DOT__ip_header);
    vlSelf->app__DOT__md_parser__DOT__udp_header = VL_RAND_RESET_Q(64);
    VL_RAND_RESET_W(96, vlSelf->app__DOT__md_parser__DOT__packet_header);
    VL_RAND_RESET_W(80, vlSelf->app__DOT__md_parser__DOT__sbe_message_header);
    VL_RAND_RESET_W(72, vlSelf->app__DOT__md_parser__DOT__trade_summary);
    VL_RAND_RESET_W(240, vlSelf->app__DOT__md_parser__DOT__md_entry);
    VL_RAND_RESET_W(96, vlSelf->app__DOT__md_parser__DOT__order_entry);
    vlSelf->app__DOT__md_parser__DOT__set_out_valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__rx_rem = VL_RAND_RESET_I(16);
    vlSelf->app__DOT__md_parser__DOT__grp_idx = VL_RAND_RESET_I(16);
    vlSelf->app__DOT__md_parser__DOT__in_grp_idx = VL_RAND_RESET_I(16);
    vlSelf->app__DOT__md_parser__DOT__parse_md_group = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__parse_ord_grp_size = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__parse_order_group = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__md_parser__DOT__no_in_group = VL_RAND_RESET_I(8);
    vlSelf->app__DOT__pv_triggerer__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pv_triggerer__DOT__rst = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pv_triggerer__DOT__rst_trigger = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__pv_triggerer__DOT__security_id_triggers[__Vi0] = VL_RAND_RESET_I(32);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        VL_RAND_RESET_W(128, vlSelf->app__DOT__pv_triggerer__DOT__price_triggers[__Vi0]);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__pv_triggerer__DOT__size_triggers[__Vi0] = VL_RAND_RESET_Q(64);
    }
    vlSelf->app__DOT__pv_triggerer__DOT__security_id = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pv_triggerer__DOT__price = VL_RAND_RESET_Q(64);
    vlSelf->app__DOT__pv_triggerer__DOT__size = VL_RAND_RESET_I(32);
    vlSelf->app__DOT__pv_triggerer__DOT__aggressor_side = VL_RAND_RESET_I(2);
    vlSelf->app__DOT__pv_triggerer__DOT__valid = VL_RAND_RESET_I(1);
    vlSelf->app__DOT__pv_triggerer__DOT__fire = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->app__DOT__pv_triggerer__DOT__state[__Vi0] = 0;
    }
    vlSelf->app__DOT__pv_triggerer__DOT__set_trigger_fire = VL_RAND_RESET_I(1);
    vlSelf->__Vdlyvset__app__DOT__fire_state__v0 = 0;
    vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v0 = 0;
    vlSelf->__Vdlyvset__app__DOT__pv_triggerer__DOT__state__v1 = 0;
    vlSelf->__Vdlyvset__app__DOT__price_triggers__v0 = 0;
    vlSelf->__Vdlyvset__app__DOT__fire_state__v1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr_h32d5fd87__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__app__DOT__md_parser__DOT__out_valid__0 = VL_RAND_RESET_I(1);
}
