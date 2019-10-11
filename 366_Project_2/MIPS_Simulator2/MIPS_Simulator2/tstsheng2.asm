# ECE 366 Project 2 Test File B2
# For checking functionality of Custom MIPS instruction
# MFOLD

# Author: Sheng Chen
	
# Initialize values
    addi    $8, $0, 3
    addi    $9, $0, 3

# Control case consisting of the instructions MFOLD will replace
# 1
# Unsigned Multiply the two values
    multu   $8, $9

# Assign them to registers from hi and lo
    mfhi    $10
    mflo    $11

# XOR registers
    xor     $12, $10, $11

# Control case consisting of the instructions MFOLD will replace
# 2
# Unsigned Multiply the two values
    multu   $12, $9

# Assign them to registers from hi and lo
    mfhi    $10
    mflo    $11

# XOR registers
    xor     $12, $10, $11

# Control case consisting of the instructions MFOLD will replace
# 3
# Unsigned Multiply the two values
    multu   $12, $9

# Assign them to registers from hi and lo
    mfhi    $10
    mflo    $11

# XOR registers
    xor     $12, $10, $11

# Control case consisting of the instructions MFOLD will replace
# 4
# Unsigned Multiply the two values
    multu   $12, $9

# Assign them to registers from hi and lo
    mfhi    $10
    mflo    $11

# XOR registers
    xor     $12, $10, $11

# Control case consisting of the instructions MFOLD will replace
# 5
# Unsigned Multiply the two values
    multu   $12, $9

# Assign them to registers from hi and lo
    mfhi    $10
    mflo    $11

# XOR registers
    xor     $12, $10, $11

# Final two folds to reduce 32-bit register 12 to 8-bits
  	andi	$21, $12, 0xffff
	srl	    $22, $12, 16
	xor	    $12, $21, $22			# C = A5[31:16] ^ A5[15:0]
	andi	$21, $12, 0xff
	srl	    $22, $12, 8
	xor	    $12, $21, $22			# C = C[15:8] ^ C[7:0]

# CUSTOM INSTRUCTION
# Perform custom instruction on initial values
#    mfold   $13, $8, $9

# Compare results between control case and custom instruction
# Flag positive register 14 if answers differ
    addi    $14, $0, 0
    beq     $13, $12, negative
    addi    $14, $0, 1
negative:
    addi    $14, $14, 0