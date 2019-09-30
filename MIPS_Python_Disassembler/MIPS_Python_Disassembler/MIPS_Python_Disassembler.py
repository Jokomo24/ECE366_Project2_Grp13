# Author: Joe Komosa
# Homework 2


# MIPS by-line Python Disassembler
print("-->ECE 366 MIPS by-line Python Disassembler<-- \n\nBuilt " +
      "with functionality for or, ori, lw, sw, addi, add, \n" +
      "mult, div, mflo, mfhi, sll, and srl instructions.\n\n")

progStmt = "Type \"exit\" to leave or enter an 8-digit hex to be decoded: "
userInput = input(progStmt)                        # Get hex code

while(userInput != 'exit'):

    hexStr = userInput                             # Store user input in type string
    hexVal = int(hexStr, 16)                       # Convert user input from type string to int(16-bit)
    opCode = hexVal & int('0xfc000000', 16)        # Determine if R or I type by evaluating the first 6 MSBs

    if opCode != int('0x00000000', 16):            # True = I type

        rs = hexVal & int('0x03e00000', 16)        # Source register rs
        rt = hexVal & int('0x001f0000', 16)        # Destination register rt
        imm = hexVal & int('0x0000ffff', 16)       # Immediate value

        if opCode == int('0x34000000', 16):        # True = ori instruction
            instrI = "ori"
        elif opCode == int('0x8c000000', 16):      # True = lw instruction
            instrI = "lw"
        elif opCode == int('0xac000000', 16):      # True = sw instruction
            instrI = "sw"
        elif opCode == int('0x20000000', 16):      # True = addi instruction
            instrI = "addi"
            neg = imm & int('0x00008000', 16)      # Check if imm is negative
            if neg > 0:
                imm = -(65536 - imm)               # True = imm is 2's compliment
        else: 
            instrI = "Instr N/A"

        print("\n0x" + str(hexStr) + " is: "       # Print assembly instruction
                     + instrI + " $"
                     + str(rt >> 16) + ", $"       # Shift left to LSB for correct decimal representation
                     + str(rs >> 21) + ", "        # ''    ''  ''  ''
                     + str(imm) + "\n")

        userInput = input(progStmt)
        continue

    elif opCode == int('0x00000000', 16):          # True = R type

        rs = hexVal & int('0x03e00000', 16)        # Source register rs
        rt = hexVal & int('0x001f0000', 16)        # Next register rt
        rd = hexVal & int('0x0000f800', 16)        # Destination register rd
        shamt = hexVal & int('0x000008c0', 16)     # Shift amount register shamt
        funct = hexVal & int('0x0000003f', 16)     # Function register funct

        if funct == int('0x00000025', 16):         # True = or instruction
            instrR = "or"
        elif funct == int('0x00000020', 16):       # True = add instruction
            instrR = "add"
        elif funct == int('0x00000018', 16):       # True = mult instruction
            instrR = "mult"
        elif funct == int('0x0000001a', 16):       # True = div instruction
            instrR = "div"
        elif funct == int('0x00000010', 16):       # True = mfhi instruction
            instrR = "mfhi"
        elif funct == int('0x00000012', 16):       # True = mflo instruction
            instrR = "mflo"
        elif funct == int('0x00000000', 16):       # True = sll instruction
            instrR = "sll"
        elif funct == int('0x00000002', 16):       # True = srl instruction
            instrR = "srl"
        else:
            instrR = "Instr N/A"

        if instrR == "or" or instrR == "add":
            print("\n0x" + str(hexStr) + " is: "    # Print assembly or instruction
                         + instrR + " $"
                         + str(rd >> 8) + ", $"               
                         + str(rs >> 21) + ", $"             
                         + str(rt >> 16) + "\n")
            
        elif instrR == "mult" or instrR == "div":
            print("\n0x" + str(hexStr) + " is: "    # Print assembly mult/div instruction
                         + instrR + " $"
                         + str(rs >> 21) + ", $"              
                         + str(rt >> 16) + "\n")     
            
        elif instrR == "mfhi" or instrR == "mflo":
            print("\n0x" + str(hexStr) + " is: "    # Print assembly mfhi/mflo instruction
                         + instrR + " $"
                         + str(rd >> 8) + "\n")

        elif instrR == "sll" or instrR == "srl":    # Print assembly sll/srl instruction
            print("\n0x" + str(hexStr) + " is: "          
                         + instrR + " $"
                         + str(rd >> 8) + ", $"               
                         + str(rt >> 16) + ", "
                         + str(shamt >> 6) + "\n") 
        else:
            print("Instruction Not Supported")

        userInput = input(progStmt)
        continue

    else:
        print("Instruction Not Supported")
        userInput = input(progStmt)
        continue

print("Goodbye.")