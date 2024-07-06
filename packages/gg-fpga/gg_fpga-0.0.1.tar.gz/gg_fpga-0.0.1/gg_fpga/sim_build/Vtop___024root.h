// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(rst,0,0);
        CData/*0:0*/ app__DOT__md_parser__DOT__out_valid;
        CData/*0:0*/ app__DOT__clk;
        CData/*0:0*/ app__DOT__rst;
        CData/*0:0*/ app__DOT__paused;
        CData/*0:0*/ app__DOT__available;
        CData/*7:0*/ app__DOT__pktcount;
        CData/*0:0*/ app__DOT__pcapfinished;
        CData/*0:0*/ app__DOT__aso_out_ready;
        CData/*0:0*/ app__DOT__aso_out_valid;
        CData/*0:0*/ app__DOT__aso_out_sop;
        CData/*2:0*/ app__DOT__aso_out_empty;
        CData/*0:0*/ app__DOT__aso_out_eop;
        CData/*5:0*/ app__DOT__aso_out_error;
        CData/*1:0*/ app__DOT__side;
        CData/*0:0*/ app__DOT__md_parse_valid;
        CData/*0:0*/ app__DOT__fire;
        CData/*0:0*/ app__DOT__rst_trigger;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__pause;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__available;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__aso_out_ready;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__aso_out_valid;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__aso_out_sop;
        CData/*2:0*/ app__DOT__pcap_parser__DOT__aso_out_empty;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__aso_out_eop;
        CData/*5:0*/ app__DOT__pcap_parser__DOT__aso_out_error;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__clk_out;
        CData/*7:0*/ app__DOT__pcap_parser__DOT__pktcount;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__newpkt;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__pcapfinished;
        CData/*0:0*/ app__DOT__pcap_parser__DOT__rg_available;
        CData/*7:0*/ app__DOT__pcap_parser__DOT__rg_pktcount;
        CData/*0:0*/ app__DOT__md_parser__DOT__clk;
        CData/*0:0*/ app__DOT__md_parser__DOT__rst;
        CData/*0:0*/ app__DOT__md_parser__DOT__rx_valid;
        CData/*0:0*/ app__DOT__md_parser__DOT__rx_eop;
        CData/*1:0*/ app__DOT__md_parser__DOT__out_side;
        CData/*0:0*/ app__DOT__md_parser__DOT__set_out_valid;
        CData/*0:0*/ app__DOT__md_parser__DOT__parse_md_group;
        CData/*0:0*/ app__DOT__md_parser__DOT__parse_ord_grp_size;
        CData/*0:0*/ app__DOT__md_parser__DOT__parse_order_group;
        CData/*7:0*/ app__DOT__md_parser__DOT__no_in_group;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__clk;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__rst;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__rst_trigger;
        CData/*1:0*/ app__DOT__pv_triggerer__DOT__aggressor_side;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__valid;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__fire;
        CData/*0:0*/ app__DOT__pv_triggerer__DOT__set_trigger_fire;
        CData/*0:0*/ __Vdlyvset__app__DOT__fire_state__v0;
        CData/*0:0*/ __Vdlyvset__app__DOT__pv_triggerer__DOT__state__v0;
        CData/*0:0*/ __Vdlyvset__app__DOT__pv_triggerer__DOT__state__v1;
        CData/*0:0*/ __Vdlyvset__app__DOT__price_triggers__v0;
        CData/*0:0*/ __Vdlyvset__app__DOT__fire_state__v1;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VicoFirstIteration;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
        CData/*0:0*/ __Vtrigprevexpr_h32d5fd87__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__app__DOT__md_parser__DOT__out_valid__0;
        CData/*0:0*/ __VactContinue;
        SData/*15:0*/ app__DOT__md_parser__DOT__packet_idx;
        SData/*15:0*/ app__DOT__md_parser__DOT__rx_rem;
        SData/*15:0*/ app__DOT__md_parser__DOT__grp_idx;
    };
    struct {
        SData/*15:0*/ app__DOT__md_parser__DOT__in_grp_idx;
        IData/*31:0*/ app__DOT__security_id;
        IData/*31:0*/ app__DOT__size;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__swapped;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__toNanos;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__file;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__r;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__eof;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__i;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__pktSz;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__diskSz;
        IData/*31:0*/ app__DOT__pcap_parser__DOT__countIPG;
        IData/*31:0*/ app__DOT__md_parser__DOT__out_security_id;
        IData/*31:0*/ app__DOT__md_parser__DOT__out_size;
        IData/*31:0*/ app__DOT__pv_triggerer__DOT__security_id;
        IData/*31:0*/ app__DOT__pv_triggerer__DOT__size;
        IData/*31:0*/ __VactIterCount;
        QData/*63:0*/ app__DOT__aso_out_data;
        QData/*63:0*/ app__DOT__price;
        QData/*63:0*/ app__DOT__pcap_parser__DOT__aso_out_data;
        QData/*63:0*/ app__DOT__md_parser__DOT__rx;
        QData/*63:0*/ app__DOT__md_parser__DOT__out_price;
        VlWide<9>/*271:0*/ app__DOT__md_parser__DOT__ip_header;
        QData/*63:0*/ app__DOT__md_parser__DOT__udp_header;
        VlWide<3>/*95:0*/ app__DOT__md_parser__DOT__packet_header;
        VlWide<3>/*79:0*/ app__DOT__md_parser__DOT__sbe_message_header;
        VlWide<3>/*71:0*/ app__DOT__md_parser__DOT__trade_summary;
        VlWide<8>/*239:0*/ app__DOT__md_parser__DOT__md_entry;
        VlWide<3>/*95:0*/ app__DOT__md_parser__DOT__order_entry;
        QData/*63:0*/ app__DOT__pv_triggerer__DOT__price;
        VlUnpacked<CData/*0:0*/, 1> app__DOT__fire_state;
        VlUnpacked<IData/*31:0*/, 1> app__DOT__security_id_triggers;
        VlUnpacked<VlWide<4>/*127:0*/, 1> app__DOT__price_triggers;
        VlUnpacked<QData/*63:0*/, 1> app__DOT__size_triggers;
        VlUnpacked<CData/*7:0*/, 24> app__DOT__pcap_parser__DOT__global_header;
        VlUnpacked<CData/*7:0*/, 16> app__DOT__pcap_parser__DOT__packet_header;
        VlUnpacked<IData/*31:0*/, 1> app__DOT__pv_triggerer__DOT__security_id_triggers;
        VlUnpacked<VlWide<4>/*127:0*/, 1> app__DOT__pv_triggerer__DOT__price_triggers;
        VlUnpacked<QData/*63:0*/, 1> app__DOT__pv_triggerer__DOT__size_triggers;
        VlUnpacked<CData/*0:0*/, 1> app__DOT__pv_triggerer__DOT__state;
    };
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<5> __VactTriggered;
    VlTriggerVec<5> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // PARAMETERS
    static constexpr CData/*0:0*/ app__DOT__TRIGGER_MODE = 0U;
    static constexpr CData/*1:0*/ app__DOT__HITTING_MODE = 1U;
    static constexpr IData/*31:0*/ app__DOT__DURATION = 0x00002710U;
    static constexpr IData/*31:0*/ app__DOT__SECURITY_ID = 0x00000d75U;
    static constexpr VlWide<15>/*479:0*/ app__DOT__PCAP_PATH = {{
        0x70636170, 0x3030302e, 0x54323230, 0x30373136,
        0x32303233, 0x782d612d, 0x2d676c62, 0x2f646333,
        0x63617073, 0x6d652f70, 0x65732f63, 0x6f757263,
        0x2f726573, 0x2e2f2e2e, 0x2e2e2f2e
    }};
    static constexpr IData/*31:0*/ app__DOT__SIZE_LO = 1U;
    static constexpr IData/*31:0*/ app__DOT__SIZE_HI = 1U;
    static constexpr IData/*31:0*/ app__DOT__NUM_INSTRUMENTS = 1U;
    static constexpr VlWide<15>/*479:0*/ app__DOT__pcap_parser__DOT__pcap_filename = {{
        0x70636170, 0x3030302e, 0x54323230, 0x30373136,
        0x32303233, 0x782d612d, 0x2d676c62, 0x2f646333,
        0x63617073, 0x6d652f70, 0x65732f63, 0x6f757263,
        0x2f726573, 0x2e2f2e2e, 0x2e2e2f2e
    }};
    static constexpr IData/*31:0*/ app__DOT__pcap_parser__DOT__ipg = 4U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__MDIncrementalRefreshTradeSummaryID = 0x00000030U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__ipv4_header_len = 0x00000110U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__udp_header_len = 0x00000040U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__packet_header_len = 0x00000060U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__sbe_message_header_len = 0x00000050U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__trade_summary_len = 0x00000048U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__trade_summary_pad = 0x00000010U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__md_entry_len = 0x000000f8U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__md_entry_pad = 0x00000010U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__order_entry_len = 0x00000060U;
    static constexpr IData/*31:0*/ app__DOT__md_parser__DOT__order_entry_pad = 0x00000020U;
    static constexpr IData/*31:0*/ app__DOT__pv_triggerer__DOT__MAX_INSTRUMENTS = 1U;
    static constexpr QData/*63:0*/ app__DOT__PRICE_LO = 0x00019c8bfadec000ULL;
    static constexpr QData/*63:0*/ app__DOT__PRICE_HI = 0x00019c979f1a3400ULL;
    static constexpr QData/*63:0*/ app__DOT__HIT_WIDTH = 0x00000005d21dba00ULL;
    static constexpr double app__DOT__pv_triggerer__DOT__HIT_WIDTH = 5.00000000000000024e-05;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
