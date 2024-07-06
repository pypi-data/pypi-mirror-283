// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop__Syms.h"
#include "Vtop___024root.h"

extern const VlWide<15>/*479:0*/ Vtop__ConstPool__CONST_h361d3684_0;

VL_ATTR_COLD void Vtop___024root___eval_initial__TOP(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial__TOP\n"); );
    // Body
    vlSelf->app__DOT__fire_state[0U] = 0U;
    vlSelf->app__DOT__paused = 1U;
    vlSelf->app__DOT__pcap_parser__DOT__file = VL_FOPEN_NN(
                                                           VL_CVT_PACK_STR_NW(15, Vtop__ConstPool__CONST_h361d3684_0)
                                                           , 
                                                           std::string{"rb"});
    ;
    if (VL_UNLIKELY((0U == vlSelf->app__DOT__pcap_parser__DOT__file))) {
        VL_WRITEF("can't read pcap input ../../../resources/cme/pcaps/dc3-glbx-a-20230716T220000.pcap\n");
        VL_FINISH_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/pcapparser_10gbmac.sv", 90, "");
    }
    VL_WRITEF("PCAP: %Napp.pcap_parser reading from ../../../resources/cme/pcaps/dc3-glbx-a-20230716T220000.pcap\n",
              vlSymsp->name());
    vlSelf->app__DOT__pcap_parser__DOT__r = VL_FREAD_I(8
                                                       ,0
                                                       ,24
                                                       , &(vlSelf->app__DOT__pcap_parser__DOT__global_header)
                                                       , vlSelf->app__DOT__pcap_parser__DOT__file
                                                       , 0
                                                       , 24);
    if (VL_UNLIKELY((((0xd4U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                       [0U]) & (0xc3U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                                [1U])) & (0xb2U == 
                                          vlSelf->app__DOT__pcap_parser__DOT__global_header
                                          [2U])))) {
        VL_WRITEF(" pcap endian: swapped, ms\n");
        vlSelf->app__DOT__pcap_parser__DOT__swapped = 1U;
        vlSelf->app__DOT__pcap_parser__DOT__toNanos = 0xf4240U;
    } else if (VL_UNLIKELY((((0xa1U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                              [0U]) & (0xb2U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                                       [1U])) & (0xc3U 
                                                 == 
                                                 vlSelf->app__DOT__pcap_parser__DOT__global_header
                                                 [2U])))) {
        VL_WRITEF(" pcap endian: native, ms\n");
        vlSelf->app__DOT__pcap_parser__DOT__swapped = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__toNanos = 0xf4240U;
    } else if (VL_UNLIKELY((((0x4dU == vlSelf->app__DOT__pcap_parser__DOT__global_header
                              [0U]) & (0x3cU == vlSelf->app__DOT__pcap_parser__DOT__global_header
                                       [1U])) & (0xb2U 
                                                 == 
                                                 vlSelf->app__DOT__pcap_parser__DOT__global_header
                                                 [2U])))) {
        VL_WRITEF(" pcap endian: swapped, nanos\n");
        vlSelf->app__DOT__pcap_parser__DOT__swapped = 1U;
        vlSelf->app__DOT__pcap_parser__DOT__toNanos = 1U;
    } else if (VL_LIKELY((((0xa1U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                            [0U]) & (0xb2U == vlSelf->app__DOT__pcap_parser__DOT__global_header
                                     [1U])) & (0x3cU 
                                               == vlSelf->app__DOT__pcap_parser__DOT__global_header
                                               [2U])))) {
        VL_WRITEF(" pcap endian: native, nanos\n");
        vlSelf->app__DOT__pcap_parser__DOT__swapped = 0U;
        vlSelf->app__DOT__pcap_parser__DOT__toNanos = 1U;
    } else {
        VL_WRITEF(" pcap endian: unrecognised format %02x%02x%02x%02x\n",
                  8,vlSelf->app__DOT__pcap_parser__DOT__global_header
                  [0U],8,vlSelf->app__DOT__pcap_parser__DOT__global_header
                  [1U],8,vlSelf->app__DOT__pcap_parser__DOT__global_header
                  [2U],8,vlSelf->app__DOT__pcap_parser__DOT__global_header
                  [3U]);
        VL_FINISH_MT("/mnt/c/Users/ggggg/Documents/docs/libs/gg.fpga.py.gg/gg_fpga/pcapparser_10gbmac.sv", 119, "");
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers__stl\n"); );
    // Body
    vlSelf->__VstlTriggered.set(0U, (IData)(vlSelf->__VstlFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__stl(vlSelf);
    }
#endif
}
