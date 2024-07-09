/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// # This Source Code Form is subject to the terms of the Mozilla Public
// # License, v. 2.0. If a copy of the MPL was not distributed with this
// # file, You can obtain one at https://mozilla.org/MPL/2.0/.

// <!-- This Source Code Form is subject to the terms of the Mozilla Public
//    - License, v. 2.0. If a copy of the MPL was not distributed with this
//    - file, You can obtain one at https://mozilla.org/MPL/2.0/. -->

// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

`timescale 1ns/1ps
`define NULL 0

import fn::*;


module cme_md_parser (
    input              clk,
    input              rst,
    input logic[63:0]  rx,
    input              rx_valid,
    input              rx_eop,

    output logic[31:0] out_security_id,
    output logic[63:0] out_price,
    output logic[31:0] out_size,
    output logic[1:0]  out_side,
    output             out_valid
  );

    localparam MDIncrementalRefreshTradeSummaryID = 48;

    typedef struct packed {
        logic [47:0]  dst_ip;
        logic [47:0]  src_ip;
        logic [15:0]  protocol_type;
        logic [15:0]  flags;
        logic [15:0]  length;
        logic [15:0]  id;
        logic [15:0]  fragment;
        logic [7:0]   ttl;
        logic [7:0]   protocol;
        logic [15:0]  checksum; 
        logic [31:0]  src_addr;
        logic [31:0]  dst_addr;
    } ipv4_header_t;

    localparam ipv4_header_len = 272; // 34 bytes

    typedef struct packed {
        logic [15:0]  src_port;
        logic [15:0]  dst_port;
        logic [15:0]  length;
        logic [15:0]  checksum;
    } udp_header_t;

    localparam udp_header_len = 64;

    typedef struct packed {
        logic [31:0] pkt_seq_num;
        logic [63:0] sending_time;
    } packet_header_t;

    localparam packet_header_len = 96; // 12 bytes

    typedef struct packed {
        logic [15:0] msg_size;
        logic [15:0] block_length;
        logic [15:0] template_id;
        logic [15:0] schema_id;
        logic [15:0] version;
    } sbe_message_header_t;

    localparam sbe_message_header_len = 80; // 10 bytes

    typedef struct packed {
        logic [63:0] transact_time;
        logic [7:0] match_event_indicator;
    } trade_summary_t;

    localparam trade_summary_len = 72; // 9 bytes
    localparam trade_summary_pad = 16; // 2 byte pad

    typedef struct packed {
        logic [63:0] md_entry_px;
        logic [31:0] md_entry_size;
        logic [31:0] security_id;
        logic [31:0] rpt_seq;
        logic [31:0] number_of_orders;
        logic [7:0] agressor_side;
        logic [7:0] md_update_action;
        logic [31:0] md_trade_entry_id;
    } md_entry_t;

    localparam md_entry_len = 248; // 30 bytes
    localparam md_entry_pad = 16; // 2 byte pad 

    typedef struct packed {
        logic [63:0] order_id;
        logic [31:0] last_qty;
    } order_entry_t;

    localparam order_entry_len = 96; // 12 bytes
    localparam order_entry_pad = 32; // 4 byte pad

    logic [15:0] packet_idx;

    ipv4_header_t ip_header;
    udp_header_t udp_header;
    
    packet_header_t packet_header;
    sbe_message_header_t sbe_message_header;

    trade_summary_t trade_summary;
    md_entry_t md_entry;
    order_entry_t order_entry;
    logic set_out_valid;

    logic [15:0] rx_rem;

    logic [15:0] grp_idx;
    logic [15:0] in_grp_idx;

    logic parse_md_group;
    logic parse_ord_grp_size;
    logic parse_order_group;

    logic [7:0] no_in_group;

    assign out_security_id  = md_entry.security_id;
    assign out_price        = md_entry.md_entry_px;
    assign out_size         = md_entry.md_entry_size;
    // for now ignore no_aggressor
    assign out_side         = md_entry.agressor_side[1:0];
    assign out_valid        = set_out_valid; 

    always @ (posedge clk) begin
    if(!rst) begin
        ip_header           <= 'b0;
        udp_header          <= 'b0;
        
        packet_header       <= 'b0;
        sbe_message_header  <= 'b0;
        
        trade_summary       <= 'b0;
        md_entry            <= 'b0;
        order_entry         <= 'b0;

        packet_idx          <= 'b0;
        grp_idx             <= 'b0;
        in_grp_idx          <= 'b0;

        parse_md_group      <= 0;
        parse_ord_grp_size  <= 0;
        parse_order_group   <= 0;

        set_out_valid       <= 0;      
    end else if (rx_valid) begin
        packet_idx <= packet_idx + 1;
        case (packet_idx)
        0:
        begin
            ip_header.dst_ip            <= fn::reverse_bytes(rx[0+:8*6], 6);
            ip_header.src_ip[47:32]     <= fn::reverse_bytes(rx[63:48], 2);
        end 
        1:
        begin 
            ip_header.src_ip[31:0]      <= fn::reverse_bytes(rx[31:0], 4);
            ip_header.protocol_type     <= fn::reverse_bytes(rx[47:32], 2);
            ip_header.flags             <= fn::reverse_bytes(rx[63:48], 2);
        end
        2:
        begin 
            ip_header.length            <= fn::reverse_bytes(rx[15:0], 2);
            ip_header.id                <= fn::reverse_bytes(rx[31:16], 2);
            ip_header.fragment          <= fn::reverse_bytes(rx[47:32], 2);
            ip_header.ttl               <= rx[55:48];
            ip_header.protocol          <= rx[63:56];
        end
        3:
        begin
            ip_header.checksum          <= fn::reverse_bytes(rx[15:0], 2);
            ip_header.src_addr          <= fn::reverse_bytes(rx[47:16], 4);
            ip_header.dst_addr[31:15]   <= fn::reverse_bytes(rx[63:48], 2);
        end 
        4:
        begin
            ip_header.dst_addr[15:0]    <= fn::reverse_bytes(rx[15:0], 2);
            udp_header.src_port         <= fn::reverse_bytes(rx[31:16], 2);
            udp_header.dst_port         <= fn::reverse_bytes(rx[47:32], 2);
            udp_header.length           <= fn::reverse_bytes(rx[63:48], 2);
        end 
        5:
        begin 
            // $display("done parsing ip and udp hdrs dst_ip: %0d src_ip: %0d src_addr: %0d dst_addr: %0d src_port: %0d dst_port: %0d length: %0d", 
            //          ip_header.dst_ip, 
            //          ip_header.src_ip,
            //          ip_header.src_addr,
            //          ip_header.dst_addr,
            //          udp_header.src_port,
            //          udp_header.dst_port,
            //          udp_header.length);
                                    
            udp_header.checksum              <= fn::reverse_bytes(rx[15:0], 2);
            packet_header.pkt_seq_num        <= rx[47:16];
            packet_header.sending_time[15:0] <= rx[63:48];
        end
        6:
        begin 
            packet_header.sending_time[63:16] <= rx[47:0];
            sbe_message_header.msg_size[15:0] <= rx[63:48];
        end 
        7:
        begin
            sbe_message_header.block_length   <= rx[15:0];
            sbe_message_header.template_id    <= rx[31:16];
            sbe_message_header.schema_id      <= rx[47:32];
            sbe_message_header.version        <= rx[63:48];
        end
        8:
        begin
            // $display("done parsing packet and sbe headers pkt_seq_num: %0d send_tm: %0t msg_size: %0d block_len: %0d template_id: %0d schema_id: %0d version: %0d", 
            //           packet_header.pkt_seq_num, 
            //           packet_header.sending_time,
            //           sbe_message_header.msg_size,
            //           sbe_message_header.block_length,
            //           sbe_message_header.template_id,
            //           sbe_message_header.schema_id,
            //           sbe_message_header.version);
        end
        endcase
        if(rx_eop) begin
        rx_rem                <= 'b0;
        
        packet_idx            <= 'b0;
        grp_idx               <= 0;
        in_grp_idx            <= 0;
        
        // packet_header         <= 'b0;
        // sbe_message_header    <= 'b0;
        // trade_summary         <= 'b0;
        // md_entry              <= 'b0;
        // order_entry           <= 'b0;
        
        parse_md_group        <= 0;
        parse_ord_grp_size    <= 0;
        parse_order_group     <= 0;
        end
        if(sbe_message_header.template_id == MDIncrementalRefreshTradeSummaryID) begin
        case (packet_idx)
            8:
            begin
            trade_summary.transact_time         <= rx;
            end
            9:
            begin
            // 2 bytes padding in TradeSummary48
            // + 2 bytes for block len
            trade_summary.match_event_indicator <= rx[7:0];
            
            // assumes no_in_grp always > 0: could add check
            no_in_group                         <= rx[47:40];
            rx_rem                              <= rx[63:48];

            grp_idx        <= 'b0;
            in_grp_idx     <= 'b0;
            parse_md_group <= 'b1;
            end   
        endcase
        if(parse_md_group) begin
            in_grp_idx <= in_grp_idx + 1;
            // 1 cycle per fields in price | (size and security_id) | aggressor_side | md_trade_entry_id
            case (in_grp_idx)
            0:
            begin
                set_out_valid                    <= 0;

                md_entry.md_entry_px[15:0]       <= rx_rem;
                md_entry.md_entry_px[63:16]      <= rx[47:0];
                rx_rem                           <= rx[63:48];
            end 
            1:
            begin
                md_entry.md_entry_size[15:0]     <= rx_rem;
                md_entry.md_entry_size[31:16]    <= rx[15:0];
                md_entry.security_id             <= rx[47:16];
                rx_rem                           <= rx[63:48];
            end 
            2:
            begin
                md_entry.rpt_seq[15:0]           <= rx_rem;
                md_entry.rpt_seq[31:16]          <= rx[15:0];
                md_entry.number_of_orders        <= rx[47:16];
                md_entry.agressor_side           <= rx[55:48];
                md_entry.md_update_action        <= rx[63:56];

                // for now don't include trade_entry_id or other
                set_out_valid                    <= 1; 
            end
            3:
            begin 
                md_entry.md_trade_entry_id       <= rx[31:0];
                // skip 2 for group padding
                rx_rem                           <= rx[63:48];
                if (grp_idx + 1 < no_in_group) begin 
                in_grp_idx           <= 'b0;
                grp_idx              <= grp_idx + 1;
                end
                else 
                begin 
                parse_md_group        <= 0;
                parse_ord_grp_size    <= 1;
                end
            end 
            endcase
        end
        if(parse_ord_grp_size) begin
            // order_grp_size.block_length <= rx_rem;
            // skip 5 inter block len <--> group size pad  
            no_in_group                         <= rx[47:40];
            rx_rem                              <= rx[63:48];

            grp_idx             <= 0;
            in_grp_idx          <= 0;
            parse_order_group   <= 1;

            parse_ord_grp_size  <= 0;

            // can move so not done before each read
            order_entry         <= 'b0;
        end 
        if(parse_order_group) begin
            in_grp_idx <= in_grp_idx + 1;
            case (in_grp_idx)
            0:
            begin
                order_entry.order_id[15:0]        <= rx_rem;
                order_entry.order_id[63:16]       <= rx[47:0];
                rx_rem                            <= rx[63:48];
            end 
            1:
            begin
                order_entry.last_qty[15:0]        <= rx_rem;
                order_entry.last_qty[31:16]       <= rx[15:0];
                
                if (grp_idx + 1 < no_in_group) begin
                // 4 byte padding (8 + 4 -> 16 group len rather than 12) 
                rx_rem                          <= rx[63:48];

                grp_idx           <= grp_idx + 1;
                in_grp_idx        <= 0;
                end else begin 
                parse_order_group <= 0;
                packet_idx        <= 'b0;
                end
            end 
            endcase
        end 
        end else begin
        // $display("template ID no match: id: %0d", sbe_message_header.template_id); 
        end  
    end
    end

endmodule
