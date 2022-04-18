import xmlrpc.client
import sys


try:
    proxy = xmlrpc.client.ServerProxy("http://" + sys.argv[1] + ":80")
except IndexError:
    print("ERROR: Can't find an ip argument", file=sys.stderr)
    
while True:
    
    filename = input("Enter the path to the input file. Enter / to finish.\n")
    if filename == '/':
        break
    try:
        number_of_processes = int(input("Enter number of processes which you want to use\n"))
    except ValueError:
        print("ERROR: It isn't a number. Exiting", file=sys.stderr)
        break
    
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: Can't find the file. Exiting", filename, file=sys.stderr)
        break
    lines_list = f.readlines()
    f.close()
    content = str()
    for line in lines_list:
        content += line

    try:
        solution_tuple = proxy.main(content)
    except ConnectionRefusedError:
        print("ERROR: Wrong address!. Exiting", file=sys.stderr)
        break

    if solution_tuple[0] != False:
        print("success")
        print("Number of iterations =", solution_tuple[2])
        print("Solution:", *solution_tuple[0])
        print("Network load =", solution_tuple[1])
    else:
        print("failure")
        print("Number of iterations =", solution_tuple[2])