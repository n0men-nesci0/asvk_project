import xmlrpc.client
import sys


proxy = xmlrpc.client.ServerProxy("http://172.17.0.2:80")

"""while True:
    
    filename = input("Enter the path to the input file. Enter / to finish.\n")
    if filename == '/':
        break
    try:
        number_of_processes = int(input("Enter number of processes which you want to use\n"))
    except ValueError:
        print("ERROR: It isn't a number. Exiting", file=sys.stderr)
        break"""
    
    
filename = "./tests/test1.xml"
    
try:
    f = open(filename, 'r')
except FileNotFoundError:
    print("ERROR: Can't find the file", filename, file=sys.stderr)
lines_list = f.readlines()
f.close()
content = str()
for line in lines_list:
    content += line

solution_tuple = proxy.main(content)

if solution_tuple[0] != False:
    print("success")
    print("Number of iterations =", solution_tuple[2])
    print("Solution:", *solution_tuple[0])
    print("Network load =", solution_tuple[1])
else:
    print("failure")
    print("Number of iterations =", solution_tuple[2])