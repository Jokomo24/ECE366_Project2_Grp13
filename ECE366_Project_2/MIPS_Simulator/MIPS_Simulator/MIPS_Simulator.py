from decodeASM import *
from ASMOperations import *

# define registers and memory as dictionaries
registers = {0:0,
          'PC':0,
          'hi':0,
          'lo':0}
memory = {}
for i in range(8,24):
    registers[i] = 0

# main program, will read the file and execute the instructions
instr_list = []
line_count = 0
debug = False
userASMFile = input("This program is a MIPS assembly simulator. Please Enter the name of the MIPS txt file you wish to simulate.\n\n\n")
print("loading Assembly Code from " + userASMFile)

while(decodeASM(userASMFile) == 0):
    print("\nFile Not Found\n")
    userASMFile = input("\nPlease Enter the name of the MIPS txt file you wish to simulate.\n\n\n")
    print("loading Assembly Code from " + userASMFile + '\n')
    decodeASM(userASMFile)

if (input('enable debug? y/n \n').lower() == 'y'):
    print('debug enabled\n')
    debug = True

h = open("mc.txt","r")
hexFile = h.readlines()  #open the instruction file

#for line in hexFile:
 #   print(line)

# you will need to read in the whole file first before executing anything
i = 0
for instr in hexFile:
    if (instr == '\n' or instr[0] == '#'):
        continue
    line_count += 1
    instr = instr[0:10]
    if debug:
        print(instr)
    temp = Instruction(instr)
    instr_list.append(temp)
    instr_list.append('')
    instr_list.append('')
    instr_list.append('')
    i += 4

# the simulation of the program:
pc = 0
while pc < line_count*4:
    if pc % 4 == 0:
        if (instr_list[pc].type == 'r_type'):
            function = r_types[instr_list[pc].func]
        else:
            function = i_types[instr_list[pc].opcode]
        function(instr_list[pc], registers, debug, memory)
    pc = registers['PC']
# show the contents of the registers and memory after program completion
print_all(registers, memory)