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

import gg_fpga::*;


module app #(
	parameter DURATION = 10000,
	parameter SECURITY_ID = 32'd3445,
	parameter TRIGGER_MODE = gg_fpga::STATIC,
	parameter HITTING_MODE = gg_fpga::AUTO_HIT_WIDTH,
	parameter PCAP_PATH = "../../../resources/cme/pcaps/dc3-glbx-a-20230716T220000.pcap",
	parameter PRICE_LO = 64'd453600000000000,
	parameter PRICE_HI = 64'd453650000000000,
	parameter SIZE_LO = 32'd1,
	parameter SIZE_HI = 32'd1
) (
	input clk,
	input rst
);

	// localparam CLK_EDGE_FREQ = 10;
	localparam NUM_INSTRUMENTS = 1;
	localparam HIT_WIDTH = ((PRICE_HI + PRICE_LO) / 2) - PRICE_LO;

	typedef enum bit {
		ARMED = 0,
		REARM = 1
	} fire_state_t;

	fire_state_t fire_state[NUM_INSTRUMENTS-1:0];

	logic paused;

	wire available;
	wire [7:0] pktcount;
	wire pcapfinished;

	wire [63:0] aso_out_data;
    wire        aso_out_ready;
    wire        aso_out_valid;
    wire        aso_out_sop;
    wire [2:0]  aso_out_empty;
    wire        aso_out_eop;
    wire [5:0]  aso_out_error;


	// for now using 1 (ES)
	logic [31:0] security_id_triggers[NUM_INSTRUMENTS-1:0] = {SECURITY_ID};
	// Price9 + display factor = 0.01
	logic [64*2-1:0] price_triggers [NUM_INSTRUMENTS-1:0] 	   = {{PRICE_HI, PRICE_LO}};
	logic [32*2-1:0] size_triggers [NUM_INSTRUMENTS-1:0] 	   = {{SIZE_HI, SIZE_LO}};

	wire [31:0] 	security_id;
	wire [63:0] 	price;
	wire [31:0] 	size;
	wire [1:0]		side;
	wire 			md_parse_valid;
	
	wire [NUM_INSTRUMENTS-1:0]	fire;

	logic [NUM_INSTRUMENTS-1:0]	rst_trigger;

	pcapparser_10gbmac #(
		.pcap_filename(PCAP_PATH),
		.ipg(4)
	) pcap_parser (
		.clk_out		(clk),
		.pause			(paused),
		.available		(available),
		.pktcount		(pktcount),
		.pcapfinished	(pcapfinished),
		.aso_out_data	(aso_out_data),
		.aso_out_ready	(aso_out_ready),
		.aso_out_valid	(aso_out_valid),
		.aso_out_sop	(aso_out_sop),
		.aso_out_empty	(aso_out_empty),
		.aso_out_eop	(aso_out_eop),
		.aso_out_error	(aso_out_error)
	);

	cme_md_parser md_parser (
		.clk 				(clk),
		.rst 				(rst),
		.rx 				(aso_out_data),
		.rx_valid 			(aso_out_valid),
		.rx_eop 			(aso_out_eop),
		.out_security_id 	(security_id),
		.out_price 			(price),
		.out_size 			(size),
		.out_side 			(side),
		.out_valid 			(md_parse_valid)
	);

	triggerer #(
		.MAX_INSTRUMENTS(1)
	) pv_triggerer (
		.clk 					(clk),
		.rst					(rst),
		.rst_trigger			(rst_trigger),
		.security_id_triggers 	(security_id_triggers),
		.price_triggers 		(price_triggers),
		.size_triggers 			(size_triggers),
		.security_id 			(security_id),
		.price 					(price),
		.size 					(size),
		.aggressor_side 		(side),
		.valid 					(md_parse_valid),
		.fire 					(fire)
	);

	initial begin 
		fire_state = '{default:ARMED};
		paused = 1; 
	end

	always @ (posedge clk) begin 
		if (!rst) begin 
			rst_trigger <= ~0;
			paused <= 0;
		end
	end

	genvar i;
	generate
		for (i = 0; i < NUM_INSTRUMENTS; ++i) begin
			always @ (posedge clk) begin
				case (fire_state[i])
				ARMED:
				begin	
				end
				REARM:
				begin 
					rst_trigger[i] <= 1'b1;
					fire_state[i] <= ARMED;	
				end
				endcase
			end	

			always @ (posedge clk && rst) begin 
				// $display("f parse out: security_id: %0d price: %0d size: %0d side: %0d",
				// 	     security_id,
				// 	     price,
				// 	     size,
				// 	     side);
				
				if (fire[i] != 0 && fire_state[i] == ARMED) begin 
					$display("fire: i: %0d security_id: %0d price: %0d size: %0d side: %0d",
							i,
							security_id,
							price,
							size,
							side);
					
					if (HITTING_MODE == gg_fpga::AUTO_HIT_WIDTH) begin 
						price_triggers[i][64+:64] 	<= price + HIT_WIDTH;
						price_triggers[i][0+:64] 	<= price - HIT_WIDTH;
					end
					
					//
					rst_trigger[i] 	<= 0;
					fire_state[i] 	<= REARM;
				end
			end
		end
	endgenerate 
 
endmodule

