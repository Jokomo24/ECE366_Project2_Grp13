#from numpy import *

# parses hex input into component instruction parts
class Instruction():
    func_dict = {'100010':'sub',
                 '100000':'add',
                 '100110':'xor',
                 '011001':'multu',
                 '011000':'mult',
                 '000010':'srl',
                 '010000':'mfhi',
                 '010010':'mflo',
                 '101011':'sltu',
                 '101010':'slt',
                 '001000':'addi',
                 '000100':'beq',
                 '000101':'bne',
                 '001101':'ori',
                 '101011':'sw',
                 '001001':'addiu',
                 '001100':'andi',
                 '000010':'j',
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
        elif self.opcode == '000010':
            self.func = self.opcode
            self.type = 'j_type'
        else: # in this case type i
            self.func = self.opcode
            self.type = 'i_type'
        self.rs = int(self.binary_string[6:11], 2)
        self.rt = int(self.binary_string[11:16], 2)
        self.rd = int(self.binary_string[16:21], 2)
        self.target = int(self.binary_string[7:32], 2) # jump label
        self.shamt = int(self.binary_string[6:11], 2) # shift amount
        if self.binary_string[16] == '1': # check the immediate for negative numbers and convert if needed
            self.imm = -((int(self.binary_string[16:32], 2) ^ 0xFFFF) + 1)
        else:
            self.imm = int(self.binary_string[16:32], 2)
        try:
            self.name = func_dict[self.func] # this will lookup the string name of the function in func_dict
        except:
            self.name = 'null'
    def print(self):
        if self.type == 'r_type':
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rd) + ', $' + str(self.rs) + ', $' + str(self.rt))
        elif self.type == 'i_type':
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', $' + str(self.rs) + ', ' + str(self.imm))
        else:
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', ' + str("labelIndex[i])"))

def print_all(registers, memory):
    print('Register Contents:')
    for value in registers.items():
        if value[1] != 0:
            print(value)
    print('Memory Contents:')
    for value in memory.items():
        print(value)


# supported instruction functions
def andi(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = operand1 & operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addi(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addiu(instruction, registers, debug, memory):
    operand1 = uint32(registers[instruction.rs])
    operand2 = uint32(instruction.imm)
    registers[instruction.rt] = uint32(operand1 + operand2)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def add(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sub(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs] #value in rs
    operand2 =  registers[instruction.rt] #value in rt
    registers[instruction.rd] = operand1 - operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def beq(instruction, registers, debug, memory):
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

def bne(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    if (operand1 != operand2):
        registers['PC'] += (4 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    return registers

def j(instruction, registers, debug, memory):
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += (4 + (instruction.target << 2))
    return registers

def ori(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = operand1 | operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def xor(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 ^ operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def multu(instruction, registers, debug, memory):
    operand1 = uint32(registers[instruction.rs])
    operand2 = uint32(registers[instruction.rt])
    registers[instruction.lo] = uint32(operand1[0:15] * operand2[0:15])
    registers[instruction.hi] = uint32(operand1[16:32] * operand2[16:32])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mult(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.lo] = operand1[0:15] * operand2[0:15]
    registers[instruction.hi] = operand1[16:32] * operand2[16:32]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mfhi(instruction, registers, debug, memory):
    registers[instruction.rd] = registers[instruction.hi]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mflo(instruction, registers, debug, memory):
    registers[instruction.rd] = registers[instruction.lo]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sltu(instruction, registers, debug, memory):
    operand1 = uint32(registers[instruction.rs])
    operand2 = uint32(registers[instruction.rt])
    registers[instruction.rd] = operand1 < operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def slt(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 < operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers


def srl(instruction, registers, debug, memory):
    operand1 = registers[instruction.rt]
    operand2 = registers[instruction.shamt]
    registers[instruction.rd] = operand1 >> operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lui(instruction, registers, debug, memory):
    registers[instruction.rt] = registers[instruction.imm]
    registers[instruction.rt] = registers[instruction.rt] & hex(0x0000)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lbu(instruction, registers, debug, memory):
    address = registers[instruction.rs]
    offset = registers[instruction.imm]
    byteLoc = hex(0x00000011) << offset
    byte = memory[address] & byteLoc
    registers[instruction.rt] = uint8(byte)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lb(instruction, registers, debug, memory):
    address = registers[instruction.rs]
    offset = registers[instruction.imm]
    byteLoc = hex(0x00000011) << offset
    byte = memory[address] & byteLoc
    registers[instruction.rt] = byte
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lw(instruction, registers, debug, memory):
    offset = registers[instruction.imm]
    registers[instruction.rt] = int32(memory[hex(offset)])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sw(instruction, registers, debug, memory):
    addr_index = registers[instruction.rs]
    offset = instruction.imm
    memory[hex(addr_index + offset)] = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

def sb(instruction, registers, debug, memory):
    addr_index = registers[instruction.rs]
    offset = instruction.imm
    memory[hex(addr_index + offset)] = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

# dictionaries of functions
j_types = {'000010':'j'}
r_types = {'100010': 'sub',
           '100000':'add',
           '100110':'xor',
           '011001':'multu',
           '011000':'mult',
           '000010':'srl',
           '010000':'mfhi',
           '010010':'mflo',
           '101011':'sltu',
           '101010':'slt'}
i_types = {'001000':'addi',
           '000100':'beq',
           '000101':'bne',
           '001101':'ori',
           '101011':'sw',
           '001001':'addiu',
           '001100':'andi',
           '001111':'lui',
           '100100':'lbu',
           '100000':'lb',
           '100011':'lw',
           '101000':'sb',
           '101011':'sw'}

