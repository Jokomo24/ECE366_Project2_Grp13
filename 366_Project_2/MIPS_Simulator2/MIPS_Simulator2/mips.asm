# ECE 366 Project 1
#
# Author: Joe Komosa
#

	lui	$8, 0xfa19			# Initialize B
	ori	$8, $8, 0xe366
	
#
# Part A
# Registers
# | $10 = A val | $11 = loVal | $12 = hiVal | 
# | $13 = A_i * B val | $14 = 5 count | $21 = temp1 | 
# | $22 = temp2 | $23 = current address |
#

	addi	$10, $0, 0			# Initialize A / counter to 0
	addi	$23, $0, 0x2020			# Initialize address to 0x2020
	
continue:
	addi	$10, $10, 1			# A++
	multu	$10, $8				# A * B 
	addi	$14, $0, 5			# Initialize 5 count
	beq	$14, $14, first_pass		# Skip on first pass
mul_fold:
	multu	$13, $8
first_pass:
	mflo	$11					
	mfhi	$12
	xor	$13, $11, $12			# Lo ^ Hi --> $13
	addi	$14, $14, -1			# Count - 1
	bne	$14, $0, mul_fold

	andi	$21, $13, 0xffff		# Last 2 folding operations
	srl	$22, $13, 16
	xor	$13, $21, $22			# C = A5[31:16] ^ A5[15:0]
	andi	$21, $13, 0xff
	srl	$22, $13, 8
	xor	$13, $21, $22			# C = C[15:8] ^ C[7:0]
	
	sw	$13, 0($23)			# val[$13] --> current address
	addi	$23, $23, 4			# Address + 4 (32-bits)
	addi	$22, $0, 0x64			# Check if counter <= 100
	bne	$22, $10, continue		# Loop if count <= 100

	xor	$21, $0, $23			# Store address for comparison in part B.ii
		
#
# Part B.i
# Registers
# | $10 = maxVal | $11 = tempVal | $12 = tempVal2 | 
# | $22 = base address | $23 = current address |
#

	addi	$10, $0, 0			# Initialize maxVal to 0
	addi	$23, $0, 0x2020			# Hold address value 0x2020
	
nxt_byte1:
	lbu	$11, 5($23)