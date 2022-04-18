import sys
from multiprocessing import Process, Queue
import queue
import argparse as ap
from datetime import datetime

import parser
import solution_generator as sol_gen


def main(content: str, number_of_processes = 1):

    # Ввод из XML файла
    
    info = parser.xml_parse(content)
    if info.is_file_correct == False:
        print("File is incorrect. Exiting", file=sys.stderr)
        exit()
        
    # Запуск алгоритма без параллельности
    
    if number_of_processes == 1:
        solution_tuple = sol_gen.search_solution(info)
        if solution_tuple[0] == [-1] * info.number_of_programs:
            solution_tuple = (False, -1, sol_gen.ITERATIONS_LIMIT) 
        
    # Запуск алгоритма параллельно на нескольких процессах
    # Число процессов было указано в качестве аргумента командной строки
    
    else:
        # Для каждого процесса создадим 2 очереди
        # Одна для чтения, другая для записи
        input_queue_list = []
        output_queue_list = []
        proc_list = []
        for i in range(number_of_processes):
            input_queue_list.append(Queue())
            output_queue_list.append(Queue())
            tmp_proc = Process(target=sol_gen.search_solution, 
                               args=(info, input_queue_list[i], output_queue_list[i]))
            proc_list.append(tmp_proc)
            
        for proc in proc_list:
            proc.start()

        # [вектор-решение, нагрузка сети, кол-во итераций]
        solution_tuple = (False, -1, sol_gen.ITERATIONS_LIMIT) 
        alive_processes = list(range(number_of_processes))
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
                    for another_proc_num in range(number_of_processes):
                        if proc_num != another_proc_num:
                            output_queue_list[another_proc_num].put(new_solution)
                        if solution_tuple[0] != False: 
                            if solution_tuple[1] > new_solution[1]:
                                solution_tuple = new_solution
                        else:
                            # Инициализация solution_tuple при первом чтении из очереди
                            solution_tuple = new_solution
                except queue.Empty:
                    pass

        # Освобождение ресурсов

        for i in range(number_of_processes):
            proc_list[i].join()
            proc_list[i].close()
            input_queue_list[i].close()
            output_queue_list[i].close()
            
    return solution_tuple
        
        
        
if __name__ == '__main__':
    
    start_time = datetime.now()
    
    # Обработка аргументов командной строки
    
    arg_parser = ap.ArgumentParser()
    arg_parser.add_argument('-p', dest="number_of_processes", 
                            default=1, type=int)
    arg_parser.add_argument('-i', dest="filename",
                            default="../client/tests/test1.xml")
    args = arg_parser.parse_args()
    
    f = open(args.filename, 'r')
    lines_list = f.readlines()
    f.close()
    content = str()
    for line in lines_list:
        content += line
        
    # Запуск алгоритма 
    solution_tuple = main(content, args.number_of_processes % 5)
    
    # Вывод 
        
    if solution_tuple[0] != False:
        print("success")
        print("Number of iterations =", solution_tuple[2])
        print("Solution:", *solution_tuple[0])
        print("Network load =", solution_tuple[1])
    else:
        print("failure")
        print("Number of iterations =", solution_tuple[2])
    print("time:", datetime.now() - start_time)