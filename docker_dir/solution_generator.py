import random
from multiprocessing import Queue
import queue

from MyLib import InputInformation # Класс для передачи даннымх между функциями 

ITERATIONS_LIMIT = 5000

# Алгоритм поиска решения задачи с помощью случайной генерации

def search_solution(info: InputInformation, output_queue: Queue = None, input_queue: Queue = None):
    
    # Распаковываем данные из объекта класса InputInformation

    number_of_cpu = info.number_of_cpu
    cpu_load_limits = info.cpu_load_limits
    number_of_programs = info.number_of_programs
    programs_load = info.programs_load
    links = info.links

    # Шаг 1. Рассчитать теоретическую максимальную нагрузку на сеть
    # Шаг 2. Установить полученное значение в качестве наилучшего

    minimal_network_load = 0
    for val in links.values():
        minimal_network_load += val
    # Вектор-решение задачи, по умолчанию [-1, ... , -1]
    best_solution = [-1] * number_of_programs

    # Шаг 3. Генерация случайного решения

    count_iter = 0
    while count_iter < ITERATIONS_LIMIT and minimal_network_load != 0:
        if input_queue != None:
            # Проверяем нет ли новых решений в очереди (при параллельном выполнении)
            try:
                new_solution, new_network_load, new_count_iter = input_queue.get_nowait()
                if new_network_load < minimal_network_load:
                    best_solution = new_solution
                    minimal_network_load = new_network_load
                    count_iter = 0
            except queue.Empty:
                pass
        count_iter += 1
        new_solution = [random.randint(0, number_of_cpu - 1)
                         for i in range(number_of_programs)]
        
        # Вычисление нагрузки на сеть для сгенерированного решения
        
        cur_network_load = 0
        for link in links.items():  
            # Программы исполняются на разных процессорах
            if new_solution[link[0][0]] != new_solution[link[0][1]]:
                cur_network_load += link[1]
        if cur_network_load >= minimal_network_load:
            continue  # Нагрузка >= наилучшей ==> возврат на шаг 3

        # Шаг 4. Проверка корректности нагрузок на процессоры

        cur_cpu_load = [0] * number_of_cpu
        for i in range(number_of_programs):
            cur_cpu_load[new_solution[i]] += programs_load[i]
        is_correct = True
        for i in range(number_of_cpu):
            is_correct = is_correct and cur_cpu_load[i] <= cpu_load_limits[i]

        if is_correct:
            minimal_network_load = cur_network_load
            best_solution = new_solution
            # Кладем найденное решение в очередь (при параллельном выполнении)
            if output_queue != None:
                output_queue.put((best_solution, 
                                  minimal_network_load, 
                                  count_iter))
            count_iter = 0

    # Уведомляем о завершении процесса и освобождаем ресурсы
    if output_queue != None and input_queue != None:
        output_queue.put("END")
        input_queue.close()
        output_queue.close()

    # Возвращаемое значение [вектор-решение, нагрузка сети, кол-во итераций]

    return (best_solution, minimal_network_load, count_iter)
