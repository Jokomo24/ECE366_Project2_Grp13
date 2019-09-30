addi $5,$12,-4
add $2,$4,$zero
L1:add $1,$0,$8
add $7,$7,$8
addi $3,$3,-2
TEST: addi $2,$5,-1
j L1
nxt_byte1:
lb $11, 0($23)		
sltu $12, $11, $10			
bne $12, $0, skip		
lb $10, 0($2)
sw $23, 100($0)			
skip:
addi $23, $23, -1			
bne $23, $22, nxt_byte1		
sb $10, 0x2004($0)		
addi $10, $0, 6		
addi $14, $0, 0			
nxt_byte2:
lb $11, 0($23)
addi $13, $0, 4					
addi $23, $23, 1			
bne $12, $10, no_match1
addi $14, $14, 1			
beq $0, $0, nxt_byte2	
no_match1:	
srl $11, $11, 8
addi $13, $13, -1		
sw $14, 0x2008($0)		
nxt_comp_byte:
addi $14, $0, 0			
lb $10, 0($22)			
nxt_byte3:
lb $11, 0($23) 			
bne $11, $10, no_match2
addi $14, $14, 1			
no_match2:
addi $23, $23, 1			
bne $23, $21, nxt_byte3
addi $22, $22, 1			
sltu $12, $14, $15			
bne $12, $0, LTmax
 beq $14, $15, LTmax			
sw $14,  0x2014($0)						
sw $10, 0x2010($0)			 
LTmax:
beq $22, $21, end			
beq $23, $21, nxt_comp_byte		
end:

	
	
	
