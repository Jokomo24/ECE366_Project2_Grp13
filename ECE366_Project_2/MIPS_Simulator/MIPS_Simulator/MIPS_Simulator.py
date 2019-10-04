from decodeASM import *

    # define registers and memory as dictionaries
registers = {0: 0,
            'PC': 0}
memory = {}
for i in range(8,24):
    registers[i] = 0

# main program, will read the file and execute the instructions
instr_list = []
line_count = 0
debug = False
userASMFile = input("This program is a MIPS assembly simulator. Please Enter the name of the MIPS txt file you wish to simulate.\n\n")
print("loading instructions from " + userASMFile)
decodeASM(userASMFile)
if (input('enable debug? y/n ').lower() == 'y'):
    print('debug enabled')
    debug = True

h = open("mc.txt","r")
hexFile = h.readlines()  #open the instruction file

for line in hexFile:
    print(line)
