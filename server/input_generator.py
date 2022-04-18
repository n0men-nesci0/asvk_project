import sys
import random

NUMBER_OF_CPU_LIST = [4, 8, 16]
CPU_LOAD_LIMIT_LIST = [50, 70, 90, 100]
PROG_LOAD_LIST = [5, 5, 5, 5, 5, 10, 10, 10, 15, 20]
DATA_EXCHANGE_INTENSITY_LIST = [10, 50, 70, 100]

# Генерация случайного входного файла

sys.stdout = open("input.xml", 'w')

print("<data>")

number_of_cpu = random.choice(NUMBER_OF_CPU_LIST)
print("\t<number_of_cpu>%d</number_of_cpu>" %number_of_cpu)

print("\t<cpu_load_limit>")
for i in range(number_of_cpu) :
    print("\t\t<cpu%d>%d</cpu%d>" % (i, random.choice(CPU_LOAD_LIMIT_LIST), i))
print("\t</cpu_load_limit>")

number_of_programs = random.randint(8, 10) * number_of_cpu
print("\t<number_of_programs>%d</number_of_programs>" %number_of_programs)

print("\t<program_load>")
for i in range(number_of_programs) :
    print("\t\t<prog%d>%d</prog%d>" % (i, random.choice(PROG_LOAD_LIST), i))
print("\t</program_load>")

print("\t<data_exchange>")
programs_links = []
for i in range(number_of_programs) :
    connected_program1 = random.randint(0, number_of_programs - 1)
    while (connected_program1 == i) :
        connected_program1 = random.randint(0, number_of_programs - 1)
    connected_program2 = random.randint(0, number_of_programs - 1)
    while (connected_program1 == connected_program2 or connected_program2 == i) :
        connected_program2 = random.randint(0, number_of_programs - 1)
    if (connected_program1, connected_program2) not in programs_links:
        programs_links.append((connected_program1, connected_program2, random.choice(DATA_EXCHANGE_INTENSITY_LIST)))
for i in range(number_of_programs) :
    print('\t\t<pair prog1="%d" prog2="%d" intensity="%d"></pair>' %(i, programs_links[i][0], programs_links[i][2]))
    print('\t\t<pair prog1="%d" prog2="%d" intensity="%d"></pair>' %(i, programs_links[i][1], programs_links[i][2]))
print('\t</data_exchange')

print('</data>')