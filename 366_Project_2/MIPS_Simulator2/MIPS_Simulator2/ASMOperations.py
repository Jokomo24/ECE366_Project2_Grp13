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
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    if(operand1 < 0):
        operand1 = 65536 - operand1
    operand2 = int((instruction.heximm).zfill(32), 2)
    andVal = operand1 & operand2
    registers[instruction.rt] = hex(andVal)
    #print(hex(operand1),hex(operand2), hex(andVal), registers['PC'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addi(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    operand2 = instruction.imm
    #print(operand1,operand2,)
    sum = operand1 + operand2
    #print(operand1,operand2,sum)
    registers[instruction.rt] = hex(sum)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def add(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = hex(operand1 + operand2)
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
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    operand2 = registers[instruction.rt]
    if (str(operand2).count('x') > 0):
        operand2 = int(operand2, 16)
    if debug:
        instruction.print()
        print_all(registers, memory)
    if (operand1 != operand2):
        registers['PC'] += (4 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    print(operand1 != operand2,operand1,operand2, instruction.imm, registers['PC'])
    return registers

def ori(instruction, registers, debug, memory): # Done/Working
    #print(registers[instruction.rs])
    operand1 = registers[instruction.rs]
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    else:
        operand1 = int(operand1)
    operand2 = int(sextb(instruction.imm, '16'), 2)
    oriVal = operand1 | operand2
    registers[instruction.rt] = hex(oriVal)
    #print(hex(operand1), hex(operand2),hex(oriVal))
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def xor(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    else:
        operand1 = int(operand1)
    operand2 = int(registers[instruction.rt], 16)
    if (str(operand2).count('x') > 0):
        operand2 = int(operand2, 16)
    else:
        operand2 = int(operand2)
    #print(registers[instruction.rs],registers[instruction.rt])
    registers[instruction.rd] = hex(operand1 ^ operand2)
    #print(hex(operand1),hex(operand2),registers[instruction.rd], registers['PC'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def multu(instruction, registers, debug, memory): # Done/Working
   # print(registers[instruction.rs],registers[instruction.rt])
    operand1 = int(registers[instruction.rs], 16)
    operand2 = int(registers[instruction.rt], 16)
    product = operand1 * operand2
    product = format(product, '064b')
    registers['hi'] = hex(int(product[0:32], 2))
    registers['lo'] = hex(int(product[32:64], 2))
    #print(hex(operand1),hex(operand2),registers['hi'], registers['lo'])
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
    if (str(operand1).count('x') > 0):
        operand1 = int(operand1, 16)
    else:
        operand1 = int(operand1)
    operand2 = registers[instruction.rt]
    if (str(operand2).count('x') > 0):
        operand2 = int(operand2, 16)
    else:
        operand2 = int(operand2)
    registers[instruction.rd] = int(operand1 < operand2) # turn bool into 1 or 0
    print(hex(operand1),hex(operand2), registers[instruction.rd])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def srl(instruction, registers, debug, memory): # Done/Working
    operand1 = bin(int(registers[instruction.rt], 16))[2:]
    #print(operand1)
    operand2 = instruction.shamt         # good catch!
    registers[instruction.rd] = hex(int(operand2 * '0' + operand1[:-operand2], 2))
    #print(hex(int(operand1,2)),hex(operand2), registers[instruction.rd])
    if debug:
        instruction.shiftopprint()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lui(instruction, registers, debug, memory): # Done/Working
    imm = int(sextb(instruction.imm, '16'), 2)
    registers[instruction.rt] = hex(int(bin(imm)[2:] + '0000000000000000', 2))
    #print(hex(instruction.imm), hex(imm), registers[instruction.rt])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lbu(instruction, registers, debug, memory): # FIX MEEEE!!!!!
    address = registers[instruction.rs]
    offset = instruction.imm
    #print(address, offset, registers[instruction.rt])
    if (str(address).count('x') > 0):
        address = int(address, 16)
    memAddress = memory[address + offset]
    byte = int(memAddress) & 0xff
    registers[instruction.rt] = hex(byte)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    #print(address, offset,byte,registers['PC'])
    return registers

def lb(instruction, registers, debug, memory): # Correct??
    address = registers[instruction.rs]
    offset = instruction.imm
    byteLoc = int(hex(0x00000011), 16) << offset
    byte = memory[address] & byteLoc
    registers[instruction.rt] = hex(byte)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lw(instruction, registers, debug, memory):
    offset = registers[instruction.imm]
    registers[instruction.rt] = memory[offset]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sw(instruction, registers, debug, memory):
    addr_index = registers[instruction.rs]
    storeLoc = instruction.rt
    if (str(addr_index).count('x') > 0):
        addr_index = int(addr_index, 16)
    else:
        addr_index = int(addr_index)
    if (str(storeLoc).count('x') > 0):
        storeLoc = int(storeLoc, 16)
    offset = int(sextb(instruction.imm, '16'), 2)
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
    memory[addr_index + offset] = hex(registers[instruction.rt])
    #print(addr_index, offset, int(registers[instruction.rt],2))
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

