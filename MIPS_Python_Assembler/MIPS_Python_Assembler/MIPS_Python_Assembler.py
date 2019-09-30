# Author(s): Trung Le and Joe Komosa


# Remember where each of the jump label is, and the target location 
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
    labelIndex = []
    labelName = []
    f = open("mc.txt","w+")
    h = open("mips.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    
    for line in asm:
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0

        if(line[0:4] == "addi"): # ADDI
            line = line.replace("addi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')

        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            
        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]),'026b')) + '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n')

        elif(line[0:5] == "addiu"): # ADDIU
            line = line.replace("addiu","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            imm = format(int(line[2]),'016b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')

        elif(line[0:5] == "multu"): # MULTU
            line = line.replace("multu","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000') + str('011001') + '\n')

        elif(line[0:4] == "mult"): # MULT
            line = line.replace("mult","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000') + str('011000') + '\n')

        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            shamt = format(int(line[2]),'05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(shamt) + str('000010') + '\n')

        elif(line[0:2] == "lb"): # LB
            line = line.replace("lb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]

            if(addressAndOS.count("0x")): # If offset = hex value \/
                for item in range(addressAndOS.count("0x")):
                    offset = addressAndOS.replace('0x','')
                    offset = offset.split("(")
                    offset = format(int(offset[0]), '016b')
                    f.write(str('10000000000') + str(rt) + str(offset) + '\n')
                
            else: # If offset = 0 \/
                f.write(str('10000000000') + str(rt) + str('0000000000000000') + '\n')

        elif(line[0:2] == "sb"): # SB
            line = line.replace("sb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]

            if(addressAndOS.count("0x")):    
                for item in range(addressAndOS.count("0x")):
                    offset = addressAndOS.replace('0x','')
                    offset = offset.split("(")
                    offset = format(int(offset[0]), '016b')
                    f.write(str('10100000000') + str(rt) + str(offset) + '\n')
                    
            else:
                f.write(str('10100000000') + str(rt) + str('0000000000000000') + '\n')

        elif(line[0:2] == "lw"): # LW
            line = line.replace("lw","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]

            if(addressAndOS.count("0x")):    
                for item in range(addressAndOS.count("0x")):
                    offset = addressAndOS.replace('0x','')
                    offset = offset.split("(")
                    offset = format(int(offset[0]), '016b')
                    f.write(str('10001100000') + str(rt) + str(offset) + '\n')
                    
            else:
                f.write(str('10001100000') + str(rt) + str('0000000000000000') + '\n')

        elif(line[0:2] == "sw"): # SW
            line = line.replace("sw","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]

            if(addressAndOS.count("0x")):    
                for item in range(addressAndOS.count("0x")):
                    offset = addressAndOS.replace('0x','')
                    offset = offset.split("(")
                    offset = format(int(offset[0]), '016b')
                    f.write(str('10101100000') + str(rt) + str(offset) + '\n')
                    
            else:
                f.write(str('10101100000') + str(rt) + str('0000000000000000') + '\n')

        elif(line[0:3] == "beq"): # BEQ
            line = line.replace("beq","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            for i in range(len(labelName)):# Branching to label
                if(labelName[i] == line[2]):
                    f.write(str('000100') + str(rs) + str(rt) + str(format(int(labelIndex[i]),'016b')) + '\n')

        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            for i in range(len(labelName)):# Branching to label
                if(labelName[i] == line[2]):
                    f.write(str('000101') + str(rs) + str(rt) + str(format(int(labelIndex[i]),'016b')) + '\n')

        elif(line[0:4] == "sltu"): # SLTU
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')

        elif(line[0:3] == "slt"): # SLT
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010') + '\n')


    f.close()

if __name__ == "__main__":
    main()
