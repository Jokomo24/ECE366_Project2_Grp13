# parses hex input into component instruction parts
class instruction():
    func_dict = {'100000':'add',
                 '100110':'xor',
                 '011001':'multu',
                 '000010':'srl',
                 '010000':'mfhi',
                 '010010':'mflo',
                 '101010':'slt',
                 '001000':'addi',
                 '000100':'beq',
                 '000101':'bne',
                 '001101':'ori',
                 '101011':'sw',
                 '001100':'andi',
                 '001111':'lui',
                 '100100':'lbu',
                 '100000':'lb',
                 '100011':'lw',
                 '101000':'sb',
                 '101011':'sw'}

    def __init__(self, hex_num):
        temp_num = int(hex_num, 16) # convert the input string to type int

        self.hex_num = hex_num # this just makes the hex number pretty with the 0x

        #make a binary string, the format gets rid of the 0b prefix in the string
        self.binary_string = format(temp_num, '0{}b'.format(32))
        # the string[0:3] syntax means the first 4 characters of string, use this fact to decode the binary
        self.opcode = self.binary_string[0:6]
        if self.opcode == '000000': # all r_types have this opcode, and function is the last 5 bits
            self.func = self.binary_string[26:32]
            self.type = 'r_type'
        else: # in this case type i
            self.func = self.opcode
            self.type = 'i_type'
        self.rs = int(self.binary_string[6:11], 2)
        self.rt = int(self.binary_string[11:16], 2)
        self.rd = int(self.binary_string[16:21], 2)
        self.shamt = int(self.binary_string[21:26], 2) # shift amount
        self.heximm = self.binary_string[16:32]
        if self.binary_string[16] == '1': # check the immediate for negative numbers and convert if needed
            self.imm = -((int(self.binary_string[16:32], 2) ^ 0xFFFF) + 1)
        else:
            self.imm = int(self.binary_string[16:32], 2)
        try:
            self.name = func_dict[self.func] # this will lookup the string name of the function in func_dict
        except:
            self.name = 'null'
    def heximm(self):
        self.imm = self.binary_string[16:32]
    def print(self):
        if self.type == 'r_type':
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rd) + ', $' + str(self.rs) + ', $' + str(self.rt))
        else:
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', $' + str(self.rs) + ', ' + str(self.imm))
    def shiftopprint(self):
        print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', $' + str(self.rs) + ', ' + str(self.shamt))

def sextb(num, bits):
    if (num < 0): # signed extension
       imm = 65536 + num # removes negative sign
       imm = str(format(int(imm),'0' + bits + 'b'))
       i = 0
       zeros = 0
       ones = str()
       while imm[i] != '1':
           zeros += 1
           ones = ones + '1'
           i += 1
       imm = ones + imm[zeros:] 
    else:
        imm = str(format(int(num),'0' + bits + 'b'))
    return imm

def print_all(registers, memory):
    print('Register Contents:')
    for value in registers.items():
        if value[1] != None:
            print(value)
    print('Memory Contents:')
    for value in memory.items():
        print(value)

# supported instruction functions
def andi(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = str(instruction.heximm).zfill(32)
    andVal = str()
    i = 0
    #print(operand1,operand2)
    while i < 32:
        if (operand1[i] == '1' and operand2[i] == '1'):
            andVal = andVal + '1'
        else:
            andVal = andVal + '0'
        i += 1
    registers[instruction.rt] = andVal
    #print(operand1,operand2,  registers[instruction.rt])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addi(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = str(int(operand1) + int(operand2))
    #print(operand1,operand2, registers[instruction.rt])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def add(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def beq(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    if (operand1 == operand2):
        registers['PC'] += (4 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    return registers

def bne(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
        print('hi')
    if (str(operand1) != str(operand2)):
        registers['PC'] += (4 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    #print(operand1,operand2, instruction.imm, registers['PC'])
    return registers

def ori(instruction, registers, debug, memory): # Done/Working
    #print(registers[instruction.rs])
    operand1 = registers[instruction.rs]
    imm = instruction.imm
    imm = sextb(int(imm), '16')
    operand2 = '0000000000000000' + imm 
    oriVal = str()
    i = 0
    while i < 32:
        if (operand1[i] == '1' or operand2[i] == '1'):
            oriVal = oriVal + '1'
        else:
            oriVal = oriVal + '0'
        i += 1
    registers[instruction.rt] = oriVal
    #print(operand1,operand2,oriVal)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def xor(instruction, registers, debug, memory): # Done/Working
    operand1 = str(format(int(registers[instruction.rs]), '032b'))
    operand2 = str(format(int(registers[instruction.rt]), '032b'))
    #print(operand1, operand2)
    xorVal = str()
    i = 0
    while i < 32:
        if (operand1[i] != operand2[i]):
            xorVal = xorVal + '1'
        else:
            xorVal = xorVal + '0'
        i += 1
    registers[instruction.rd] = xorVal
    #print(registers[instruction.rd])
    #print(operand1,operand2,xorVal)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def multu(instruction, registers, debug, memory): # Done/Working
    if(int(registers[instruction.rs]) > 0):
        operand1 = int(registers[instruction.rs])
    else:
        operand1 = int(str(registers[instruction.rs]), 2)
    operand2 = int(str(registers[instruction.rt]), 2)
    product = operand1 * operand2
    product = format(product, '064b')
    registers['hi'] = product[0:32]
    registers['lo'] = product[32:64]
    #print(product)
    #print(operand1,operand2,registers['hi'], registers['lo'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mfhi(instruction, registers, debug, memory): # Done/Working
    registers[instruction.rd] = registers['hi']
    #print(registers['hi'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mflo(instruction, registers, debug, memory): # Done/Working
    registers[instruction.rd] = registers['lo']
    #print('lo'+registers['lo'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def slt(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = int(int(operand1, 10) < int(operand2, 2)) # turn bool into 1 or 0
    #print(int(operand1, 10),int(operand2, 2), registers[instruction.rd])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def srl(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rt]
    operand2 = instruction.shamt          # good catch!
    registers[instruction.rd] = operand2 * '0' + operand1[:-operand2]
    #print(operand1,operand2, registers[instruction.rd])
    if debug:
        instruction.shiftopprint()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lui(instruction, registers, debug, memory): # Done/Working
    imm = instruction.imm
    imm = sextb(imm, '16')
    registers[instruction.rt] = str(imm) + '0000000000000000'
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lbu(instruction, registers, debug, memory): # FIX ME!! needs to be unsigned operation
    address = int(registers[instruction.rs], 10)
    offset = int(str(instruction.imm), 10)
    print(address, offset)
    byteLoc = 0x00000011 << offset   # Correct???
    byte = memory[address] & byteLoc
    registers[instruction.rt] = byte
    print(address, offset, registers[instruction.rt])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lb(instruction, registers, debug, memory): # Correct??
    address = registers[instruction.rs]
    offset = instruction.imm
    byteLoc = int(hex(0x00000011), 16) << offset
    byte = memory[address] & byteLoc
    registers[instruction.rt] = byte
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lw(instruction, registers, debug, memory):
    offset = registers[instruction.imm]
    registers[instruction.rt] = memory[hex(offset)]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sw(instruction, registers, debug, memory):
    addr_index = int(registers[instruction.rs])
    offset = int(instruction.imm)
    memory[addr_index + offset] = registers[instruction.rt]
    #print(addr_index, offset, registers[instruction.rd])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

def sb(instruction, registers, debug, memory):
    addr_index = int(registers[instruction.rs])
    offset = int(instruction.imm)
    #print(addr_index, offset, registers[instruction.rt])
    memory[addr_index + offset] = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

# dictionaries of functions
r_types = {'100000':add,
           '100110':xor,
           '011001':multu,
           '000010':srl,
           '010000':mfhi,
           '010010':mflo,
           '101010':slt}
i_types = {'001000':addi,
           '000100':beq,
           '000101':bne,
           '001101':ori,
           '101011':sw,
           '001100':andi,
           '001111':lui,
           '100100':lbu,
           '100000':lb,
           '100011':lw,
           '101000':sb,
           '101011':sw}

