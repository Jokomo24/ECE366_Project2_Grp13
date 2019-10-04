# ECE 366 HW #3 Q3 
#
# Author: Joe Komosa
	
	
# Part 1
	addi	$4, $0, 0				# Initialize counter to 0
	addi	$2, $0, 0x2000				# Initialize address to 0x2000

continue:		
	addi	$4, $4, 1				# Counter++
	sb	$4, 0($2)				# Store current byte from counter into memory
	addi	$2, $2, 1				# Address + 1 (8-bits)
	ori	$5, $0, 0xfe
	slt	$3, $4, $5				# Check if counter <= 254
	bne	$3, $0, continue			# Loop if true
	
	sb	$4, 0($2)				# Store last 255 into memory