import sys
import xml.etree.cElementTree as ET

from MyLib import InputInformation

class NonPosValException(Exception):
    pass


class NotInRangeException(Exception):
    pass


# Ввод информации из XML файла

def xml_parse(content: str):
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        print("Parse error: Check if the XML file is correct", file=sys.stderr)
        # При неккоректном входном xml файле возвращаем объект класса InputInformation с опущеным флагом is_file_correct
        return InputInformation(False)
    except FileNotFoundError:
        print("Input error: File not found")
        return InputInformation(False)

    if len(root) != 5:
        print("Parse error: Incorrect file structure", file=sys.stderr)
        return InputInformation(False)

    # Структура xml файла строго описана в прилагаемой pdf интсрукции, обращаемся к элементам по числовому индексу
    # Количество процессоров

    try:
        number_of_cpu = int(root[0].text)
        if number_of_cpu <= 0:
            raise NonPosValException
    except ValueError:
        print("Content error: Number of cpu is not an integer number", file=sys.stderr)
        return InputInformation(False)
    except NonPosValException:
        print("Content error: Number of cpu is not a positive number", file=sys.stderr)
        return InputInformation(False)

    # Предельная нагрузка для каждого процессора
    
    cpu_load_limits = []
    try:
        for i in range(number_of_cpu):
            cpu_load_limits.append(int(root[1][i].text))
            if not (0 <= cpu_load_limits[i] <= 100):
                raise NotInRangeException
    except ValueError:
        print("Content error: Cpu load limit number %d is not an integer number"
              %i, file=sys.stderr)
        return InputInformation(False)
    except IndexError:
        print("Content error: Wrong number of records in field cpu_load_limit", file=sys.stderr)
        return InputInformation(False)
    except NotInRangeException:
        print("Content error: Cpu load limit number %d is out of range [0,100]"
              %i, file=sys.stderr)
        return InputInformation(False)
    
    # Количество программ

    try:
        number_of_programs = int(root[2].text)
        if number_of_programs <= 0:
            raise NonPosValException
    except ValueError:
        print("Content error: Number of programs is not an integer number",
              file=sys.stderr)
        return InputInformation(False)
    except NonPosValException:
        print("Content error: Number of programs is not a positive number",
              file=sys.stderr)
        return InputInformation(False)

    # Нагрузка на процессор каждой из программ

    programs_load = []
    try:
        for i in range(number_of_programs):
            programs_load.append(int(root[3][i].text))
            if not (0 <= programs_load[i] <= 100):
                raise NotInRangeException
    except ValueError:
        print("Content error: Program load number %d is not an integer number" 
              %i, file=sys.stderr)
        return InputInformation(False)
    except IndexError:
        print("Content error: Wrong number of records in field program_load", 
              file=sys.stderr)
        return InputInformation(False)
    except NotInRangeException:
        print("Content error: program load number %d is out of range [0,100]"
              %i, file=sys.stderr)
        return InputInformation(False)

    # Программы обменивающиеся данными

    links = dict()
    try:
        cnt = 0
        for element in root[4]:
            link_info = element.attrib
            prog1 = int(link_info["prog1"])
            prog2 = int(link_info["prog2"])
            if not (0 <= prog1 < number_of_programs) or not (0 <= prog2 < number_of_programs):
                raise NotInRangeException
            if (prog2, prog1) in links or (prog1, prog2) in links:
                print("Content error: Pair of programs (%d, %d) recorded twice. Second time at found at pair number %d" 
                      %(prog1, prog2, cnt))
                return InputInformation(False)
            else:
                links[(prog1, prog2)] = int(link_info["intensity"])
            cnt += 1
    except KeyError:
        print("Content error: Wrong name of attribute in element pair number %d" 
              %cnt, file=sys.stderr)
        return InputInformation(False)
    except ValueError:
        print("Content error: Number of program or exchange intensity from attributes of element pair number %d is not an integer number"
              %cnt, file=sys.stderr)
        return InputInformation(False)
    except NotInRangeException:
        print("Content error: Number of program from attribute of element pair number %d is out of range [0, %d]"
              %(cnt, number_of_programs - 1), file=sys.stderr)
        return InputInformation(False)

    # Возвращаем данные полученные из файла через объект класса InputInforamtion

    return InputInformation(True).set(number_of_cpu, cpu_load_limits, number_of_programs, programs_load, links)
