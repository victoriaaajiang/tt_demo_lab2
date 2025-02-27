/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_third (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // All output pins must be assigned. If not used, assign to 0.
    // assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in

    assign uio_out = 0;
    assign uio_oe  = 0;

    //Refer ui_in as the A input from the report
    //Refer uio_in as the B input from the report
    //Refer uo_out as the C output from the report

    //first multiplexer in the diagram, assigning first four bits of the output
    mux_two_one first(ui_in[0], uio_in[0], ui_in[0], uo_out[0]);
    mux_two_one second(ui_in[1], uio_in[1], ui_in[0], uo_out[1]);
    mux_two_one third(ui_in[2], uio_in[2], ui_in[0], uo_out[2]);
    mux_two_one fourth(ui_in[3], uio_in[3], ui_in[0], uo_out[3]);

    mux_two_one fifth(uo_out[0], uio_in[4], ui_in[1], uo_out[4]);//add assertion
    mux_two_one sixth(uo_out[1], uio_in[5], ui_in[1], uo_out[5]);
    mux_two_one seventh(uo_out[2], uio_in[6], ui_in[1], uo_out[6]);
    mux_two_one eighth(uo_out[3], uio_in[7], ui_in[1], uo_out[7]);

    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0, uio_out, uio_oe};

endmodule

//This function modifies the 2 to 1 multiplexer by comparing the input signal to each bit of the inputs. 
module mux_two_one(a, b, a_7, o);
    input a, b, a_7;
    output o;

    assign o = a_7 ? b : a
endmodule
