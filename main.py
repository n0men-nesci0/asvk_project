import queue
import sys
from multiprocessing import Process, Queue
import argparse as ap
from datetime import datetime

import parser
import solution_generator as sg


if __name__ == '__main__':
    
    start_time = datetime.now()
    
    # Обработка аргументов командной строки
    
    arg_parser = ap.ArgumentParser()
    arg_parser.add_argument('-p', dest="number_of_processes", 
                            default=1, type=int)
    arg_parser.add_argument('-i', dest="filename", default="input.xml")
    args = arg_parser.parse_args()
    # Теперь соответствующие значения аргументов командной строки находятся в 
    # args.number_of_processes, args.filename
    args.number_of_processes %= 5

    # Ввод из XML файла
    
    info = parser.xml_parse(args.filename)
    if info.is_file_correct == False:
        print("File is incorrect. Exiting", file=sys.stderr)
        exit()
        
    # Запуск алгоритма без параллельности
    
    if args.number_of_processes == 1:
        solution, network_load, iterations = sg.search_solution(info)
        if solution != [-1] * info.number_of_programs:
            print("success")
            print("Number of iterations =", iterations)
            print("Solution:", *solution)
            print("Network load =", network_load)
        else:
            print("failure")
            print("Number of iterations =", sg.ITERATIONS_LIMIT)
        print("time:", datetime.now() - start_time)
        
    # Запуск алгоритма параллельно на нескольких процессах
    # Число процессов было указано в качестве аргумента командной строки
    
    else:
        # Для каждого процесса создадим 2 очереди
        # Одна для чтения, другая для записи
        input_queue_list = []
        output_queue_list = []
        proc_list = []
        for i in range(args.number_of_processes):
            input_queue_list.append(Queue())
            output_queue_list.append(Queue())
            tmp_proc = Process(target=sg.search_solution, 
                               args=(info, input_queue_list[i], output_queue_list[i]))
            proc_list.append(tmp_proc)
            
        for proc in proc_list:
            proc.start()

        solution_tuple = None # После инициализации [вектор-решение, нагрузка сети, кол-во итераций]
        alive_processes = list(range(args.number_of_processes))
        while len(alive_processes) != 0:
            # Для каждого работающего процесса проверяем его очередь вывода
            for proc_num in alive_processes:
                try:
                    new_solution = input_queue_list[proc_num].get_nowait()
                    # Получив признак конца удаляем номер процесса из списка alive_processes
                    if new_solution == "END":
                        alive_processes.remove(proc_num)
                        continue
                    # Получив решение отправляем его всем остальным процессам
                    for another_proc_num in range(args.number_of_processes):
                        if proc_num != another_proc_num:
                            output_queue_list[another_proc_num].put(new_solution)
                        if solution_tuple != None: # Инициализация solution_tuple
                            if solution_tuple[1] > new_solution[1]:
                                solution_tuple = new_solution
                        else:
                            # Инициализация solution_tuple при первом чтении из очереди
                            solution_tuple = new_solution
                except queue.Empty:
                    pass
                
        # Освобождение ресурсов

        for i in range(args.number_of_processes):
            proc_list[i].join()
            proc_list[i].close()
            input_queue_list[i].close()
            output_queue_list[i].close()
            
        # Вывод 
        
        if solution_tuple != None:
            print("success")
            print("Number of iterations =", solution_tuple[2])
            print("Solution:", *solution_tuple[0])
            print("Network load =", solution_tuple[1])
        else:
            print("failure")
            print("Number of iterations =", sg.ITERATIONS_LIMIT)
        print("time:", datetime.now() - start_time)