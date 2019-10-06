# ECE 366 Project 2 Test File B
# For checking functionality of MIPS instructions
# XOR, ANDI, SRL, and ORI

# Author: Sheng Chen
	
# ANDI test
    andi $8, $0, 0     # set register 8 to 0

# ORI test
    ori $9, $0, -1     # set register 9 to -1

# SRL test
    srl $10, $9, 1	   # set register 10 to $9 >> 1 = ((2^31)-1)

# XOR test
    xor $11, $10, $9	# set register 11 to $10 XOR $9 = -(2^31)