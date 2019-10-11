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
	lbu	$11, 0($23)			# Load current byte from memory
	slt	$12, $11, $10			# currentVal < maxVal = ?
	bne	$12, $0, skip			# False = skip
	lbu	$10, 0($23)			# True = store maxVal
	sw	$23, 0x2000($0)			# Store address of current maxVal into M[0x2000]
skip:
	#addi	$21, $0, 0x2024			# Temp line
	
	addi	$23, $23, 4			# Address + 4 (32-bits)
	bne	$23, $21, nxt_byte1		# Branch if $23 != last word
	
	sw	$10, 0x2004($0)			# Store maxVal into M[0x2004]
	
#
# Part B.ii
# | $10 = "11111" bitVal | $11 = curByte | $12 = truthVal | 
# | $13 = compareCnt | $14 = yesCnt | 
# | $21 last byte in mem = temp2 | $23 = current address |
#
	addi	$23, $0, 0x2020			# Hold address value 0x2020
	addi	$10, $0, 0x1f			# Five successive 1's starting from LSB
	addi	$14, $0, 0			# Initialize yesCnt	
nxt_byte2:
	lbu	$11, 0($23)			# Load current byte from memory
	addi	$13, $0, 4			# 4 count for 4 comparisons (3 zeros) 			
	addi	$23, $23, 4			# Address + 4 (32-bits)
nxt_bit:
	andi	$12, $11, 0x1f			# Match?
	bne	$12, $10, no_match1
	addi	$14, $14, 1			# yesCnt++
	beq	$0, $0, nxt_byte2		# Quit and load next byte
no_match1:	
	srl	$11, $11, 1			# Shift right 1 bit
	addi	$13, $13, -1			# Count--
	bne	$13, $0, nxt_bit 
	bne	$23, $21, nxt_byte2 		# Branch if $23 != last byte in memory
	
	sw	$14, 0x2008($0)			# Store yesCnt into M[0x2008]	

#
# Part B.iii
# Registers
# | $10 = compVal | $11 = ith byte val | $12 = truthVal | 
# | $14 = colli count | $21 = addr of last byte | 
# | $22 = addr of compByte | $23 = ith address |
#

	ori	$22, $0, 0x2020			# Set base data address	
nxt_comp_byte:
	addi	$14, $0, 0			# Initialize collision count
	lbu	$10, 0($22)			# Load current byte from memory
	ori	$23, $0, 0x2020
nxt_byte3:
	lbu	$11, 0($23) 			# Load ith byte from memory
	bne	$11, $10, no_match2
	addi	$14, $14, 1			# yesCnt++
no_match2:
	addi	$23, $23, 4			# Address + 4
	bne	$23, $21, nxt_byte3
	addi	$22, $22, 4			# Address + 4 of compare byte
	slt	$12, $14, $15			# compare with current max collision count
	bne	$12, $0, LTmax
	beq	$14, $15, LTmax			# Go with first occuring pattern
	sw	$14, 0x2014($0)			# Store new collision count into M[0x2014]
	xor	$15, $0, $14			# Hold current max
	sw	$10, 0x2010($0)			# Store value of max collision/match 
LTmax:
	beq	$22, $21, end			# Continue until all bytes compared
	beq	$23, $21, nxt_comp_byte		
end:

	
	
	
