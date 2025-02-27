# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 3
    dut.uio_in.value = 131

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 131

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
        # Test all combinations of ui_in and uio_in across 256 possible values
    max_val = 255  # Maximum sum value allowed
    a_vals = [i for i in range(max_val)]  # ui_in can range from 0 to 255
    b_vals = [j for j in range(max_val)]  # uio_in can also range from 0 to 255

    for i in range(len(a_vals)):
        for j in range(len(b_vals)):
            # Set the input values
            dut.ui_in.value = a_vals[i]
            dut.uio_in.value = b_vals[j]

            # Wait for one or more clock cycles to see the output values
            await ClockCycles(dut.clk, 20)  # Allow enough time for the DUT to process

            # Log the output and check the assertion
            dut._log.info(f"Test case ui_in={a_vals[i]}, uio_in={b_vals[j]} -> uo_out={dut.uo_out.value}")

            # Expected output logic (assuming sum modulo 256, replace as per DUT logic)
            # expected_uo_out = (a_vals[i] + b_vals[j]) % 256
            #Converting A and B into binary values
            # binary_a = bin(a)[2:]
            # binary_b = bin(b)[2:]
            binary_a = format(a_vals[i], '08b')  # '08b' means 8-bit binary
            binary_b = format(b_vals[j], '08b')
            dut._log.info(f"a in binary: {binary_a}, b in binary: {binary_b}")  # Output: 0b1101

            #Extract the 8th and 7th bit of the binary number as select lines
            select_line_one = int(binary_a[7]) #Get 1st bit for multiplexer
            select_line_two = int(binary_a[6]) #Get 2nd bit
            dut._log.info(f"select lines, first one: {select_line_one}, and second one: {select_line_two}")

            output_arr = []
            #Add the first 4 bits of the output
            for k in range(4):
                temporary = 0
                #If the select line is 0, take the bit number of A
                if select_line_one == 0:
                    temporary = binary_a[-(k + 1)]
                    output_arr.append(temporary)
                #If the select line is 0, take the bit number of B
                elif select_line_one == 1:
                    temporary = binary_b[-(k + 1)]
                    output_arr.append(temporary)
                else:
                    print("Error in select line value")
                    continue
            reversed_arr_pt_1 = output_arr[::-1]
            # print(reversed_arr_pt_1)
                
            #Add the last 4 bits of the output
            count = 0
            for v in range(4, 8):
                temporary = 0
                #If the select line is 0, take the bit number of A
                if select_line_two == 0:
                    temporary = reversed_arr_pt_1[-(count + 1)]
                    output_arr.append(temporary)
                    count += 1
                #If the select line is 0, take the bit number of B
                elif select_line_two == 1:
                    temporary = binary_b[7 - v]
                    output_arr.append(temporary)
                else:
                    # print("Error in select line value")
                    continue
                
            #Check if the expected output has 8 bits
            reversed_arr = output_arr[::-1]
            # print("The expected binary output is: ", reversed_arr)

            # Convert list to a binary string and then to decimal
            decimal_number = int("".join(map(str, reversed_arr)), 2)

            print("In decimal, it is: ", decimal_number)  # Output: 11


            # Assert the output matches the expected value
            assert int(dut.uo_out.value) == decimal_number, (
                f"Test failed for ui_in={a_vals[i]}, uio_in={b_vals[j]}. Expected {decimal_number}, "
                f"but got {dut.uo_out.value}")
            
            # Optionally log the test case result if the assertion passed
            dut._log.info(f"Test passed for ui_in={a_vals[i]}, uio_in={b_vals[j]} with uo_out={dut.uo_out.value}")
