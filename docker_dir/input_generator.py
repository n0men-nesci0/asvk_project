import sys
import random

NUMBER_OF_CPU_LIST = [16]
CPU_LOAD_LIMIT_LIST = [50, 70, 90, 100]
PROG_LOAD_LIST = [5, 5, 5, 5, 5, 5, 5, 10, 15, 20]
DATA_EXCHANGE_INTENSITY_LIST = [10, 50, 70, 100]

sys.stdout = open("input.xml", 'w')
print("<data>")
number_of_cpu = random.choice(NUMBER_OF_CPU_LIST)
print("\t<number_of_cpu>%d</number_of_cpu>" %number_of_cpu)
print("\t<cpu_load_limit>")
for i in range(number_of_cpu) :
    print("\t\t<cpu%d>%d</cpu%d>" % (i, random.choice(CPU_LOAD_LIMIT_LIST), i))
print("\t</cpu_load_limit>")
number_of_programms = random.randint(8, 10) * number_of_cpu
print("\t<number_of_programms>%d</number_of_programms>" %number_of_programms)
print("\t<programm_load>")
for i in range(number_of_programms) :
    print("\t\t<prog%d>%d</prog%d>" % (i, random.choice(PROG_LOAD_LIST), i))
print("\t</programm_load>")
print("\t<data_exchange>")
programms_links = []


for i in range(number_of_programms) :
    connected_program1 = random.randint(0, number_of_programms - 1)
    while (connected_program1 == i) :
        connected_program1 = random.randint(0, number_of_programms - 1)
    connected_program2 = random.randint(0, number_of_programms - 1)
    while (connected_program1 == connected_program2 or connected_program2 == i) :
        connected_program2 = random.randint(0, number_of_programms - 1)
    programms_links.append((connected_program1, connected_program2, random.choice(DATA_EXCHANGE_INTENSITY_LIST)))
for i in range(number_of_programms) :
    print('\t\t<pair prog1="%d" prog2="%d" intensity="%d"></pair>' %(i, programms_links[i][0], programms_links[i][2]))
    print('\t\t<pair prog1="%d" prog2="%d" intensity="%d"></pair>' %(i, programms_links[i][1], programms_links[i][2]))