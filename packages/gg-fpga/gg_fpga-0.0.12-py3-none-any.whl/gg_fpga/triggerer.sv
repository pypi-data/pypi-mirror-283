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


module triggerer #(
    parameter MAX_INSTRUMENTS = 8
) (
    input                               clk,
    input                               rst,
    input logic[MAX_INSTRUMENTS-1:0]    rst_trigger,

    input logic[31:0]                   security_id_triggers[MAX_INSTRUMENTS-1:0],
    // keeping this raw for now to make simulation easier (move to packed structs)
    input logic[64*2-1:0]               price_triggers[MAX_INSTRUMENTS-1:0],
    input logic[32*2-1:0]               size_triggers[MAX_INSTRUMENTS-1:0],
    
    input logic[31:0]                   security_id,
    input logic[63:0]                   price,
    // note wont work with summary_long (65)
    input logic[31:0]                   size,
    input logic[1:0]                    aggressor_side,
    input                               valid,
    
    output logic[MAX_INSTRUMENTS-1:0]   fires    
);

    typedef enum bit {
        ARMED = 0,
        FIRED = 1
    } state_t;

    state_t state [0:MAX_INSTRUMENTS-1];

    logic[MAX_INSTRUMENTS-1:0] set_trigger_fires;
    assign fires = set_trigger_fires;

    genvar i;
    generate 
        for (i = 0; i < MAX_INSTRUMENTS; ++i) begin 
            // keep clk to separate rst and state from fire logic
            always @ (posedge clk) begin 
                if (!rst || !rst_trigger[i]) begin 
                    set_trigger_fires[i] <= 0;
                    state[i] <= ARMED;
                end else if (state[i] == ARMED && set_trigger_fires[i]) begin 
                    state[i] <= FIRED;
                end
            end 

            always @ (posedge valid) begin 
                if (rst && rst_trigger[i] && state[i] == ARMED && security_id == security_id_triggers[i]) begin 
                    case (aggressor_side)
                    1:
                    begin
                        // [ Price64, Price64 ]
                        // 0: sell aggressor price limit (lo)
                        // 1: buy aggressor price limit (hi)
                        if (price >= price_triggers[i][64+:64] && size >= size_triggers[i][32+:32]) begin 
                            set_trigger_fires[i] <= 1;
                        end
                    end 
                    2:
                    begin 
                        if (price <= price_triggers[i][0+:64] && size >= size_triggers[i][0+:32]) begin
                            set_trigger_fires[i] <= 1;
                        end
                    end
                    endcase
                end                 
            end 
        end
    endgenerate

endmodule