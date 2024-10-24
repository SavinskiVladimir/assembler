import struct
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

def assemble(input_file, binary_file, log_file):
    instructions = [] # список иснтрукций, переведённых в байт-код
    log_entries = [] # список кортежей для записи в лог-файл

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split() # разделение прочитанной команды на части
            if not parts:
                continue
            A, B, C = map(int, parts)  # получение значений аргументов и перевод их в int числа
            if A == 214: # обработка загрузки константы
                instruction = struct.pack('>BHI', A, B, C & 0xFFFFFF) # перевод аргументов в байт строку
                instruction = instruction[:3] + bytes([(C >> 16) & 0xFF, (C >> 8) & 0xFF, C & 0xFF]) # удаление лишнего байта для аргумента С
                instructions.append(instruction) # добавление инструкции в список для хранения инструкций
                log_entries.append(('LOAD_CONST', A, B, C)) # добавление кортежа аргументов инструкции для лог-файла

            elif A == 138: # обработа чтения из памяти
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append(('READ_MEM', A, B, C))

            elif A == 9:  # обработка записи в память
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append(('WRITE_MEM', A, B, C))

            elif A == 241: # обработка операции popcnt()
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append(('POP_CNT', A, B, C))
            else:
                print('Invalid command format')
                continue

        # запись байт кода в бинарный файл
        with open(binary_file, 'wb') as bin_file:
            for instruction in instructions:
                bin_file.write(instruction)

        # формирование лог-файла
        root = ET.Element("log") # создание корня xml дерева
        for entry in log_entries:
            # формирование записи об инструкции
            instruction_element = ET.SubElement(root, "instruction")
            key_elem = ET.SubElement(instruction_element, "key")
            key_elem.text = entry[0]
            a_elem = ET.SubElement(instruction_element, "A")
            a_elem.text = "A=" + str(entry[1])
            b_elem = ET.SubElement(instruction_element, "B")
            b_elem.text = "B=" + str(entry[2])
            c_elem = ET.SubElement(instruction_element, "C")
            c_elem.text = "C=" + str(entry[3])

        xml_str = ET.tostring(root).decode() # перевод xml дерева в строку для записи
        pretty_sml_str = minidom.parseString(xml_str).toprettyxml(indent="\t") # форматирование строки для записи
        pretty_sml_str = '\n'.join(pretty_sml_str.split('\n')[1:]) # удаление первой строки с версией лог-файла
        with open(log_file, 'w') as log_f:
            log_f.write(pretty_sml_str) # запись в лог-файл


class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size  # инициализация памяти
        # запись в память значений для тестирования простой программы
        self.memory[265] = 101
        self.memory[101] = 63
        self.memory[191] = 102
        self.memory[666] = 665
        self.memory[97] = 103
        self.memory[561] = 104
        self.memory[626] = 34
        self.memory[10] = 10 # для тестирования основной программы
        self.memory[11] = 11 # в ячейки, хранящие адреса результирующих ячеек,
        self.memory[12] = 12 # фиксируем сами эти ячейки для простоты
        self.memory[13] = 13
        self.memory[14] = 14
        self.memory[15] = 15
        self.pc = 0  # программный счетчик
    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()  # загрузка программы в памяти

    def execute(self, result_range_start, result_range_end):
        while self.pc < len(self.program):
            # Читаем первый байт для определения размера инструкции
            opcode = self.program[self.pc]

            if opcode == 0xD6:  # LOAD_CONST
                instruction = self.program[self.pc:self.pc + 6]  # чтение 6 байт
                A = instruction[0]
                B = struct.unpack('>H', instruction[1:3])[0]
                C = struct.unpack('>I', b'\x00' + instruction[3:])[0]  # читаем C как 3 байта с нулем
                self.memory[B] = C  # записываем константу в память по адресу B
                self.pc += 6

            elif opcode == 0x8A:  # READ_MEM
                instruction = self.program[self.pc:self.pc + 5]  # чтение 5 байт
                A = instruction[0]
                B = struct.unpack('>H', instruction[1:3])[0]
                C_address = struct.unpack('>H', instruction[3:])[0]
                C_value = self.memory[self.memory[C_address]]  # читаем из памяти по адресу, записанному в C
                self.memory[B] = C_value  # записываем в память по адресу B
                self.pc += 5

            elif opcode == 0x09:  # WRITE_MEM
                instruction = self.program[self.pc:self.pc + 5]  # чтение 5 байт
                A = instruction[0]
                B_address = struct.unpack('>H', instruction[1:3])[0]
                C_address = struct.unpack('>H', instruction[3:])[0]
                self.memory[self.memory[C_address]] = self.memory[B_address]  # запись значения в память по адресу, записанному в С, значения из B
                self.pc += 5

            elif opcode == 0xF1:  # POP_CNT
                instruction = self.program[self.pc:self.pc + 5]  # чтение 5 байт
                A = instruction[0]
                B_address = struct.unpack('>H', instruction[1:3])[0]
                C_address = struct.unpack('>H', instruction[3:])[0]

                value_to_count = self.memory[C_address]  # чтение значения из памяти по адресу C
                popcnt_result = bin(value_to_count).count('1')  # подсчет количества единиц в двоичном представлении значения
                self.memory[self.memory[B_address]] = popcnt_result  # запись результата в память по адресу, записанному в B
                self.pc += 5

            else:
                print(f"Unknown opcode: {opcode}")  # сообщение о неизвестном коде операции
                break

        return self.memory[result_range_start:result_range_end + 1] # возврат участка памяти, содержащего результат

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python assembler_interpreter.py <input_file> <binary_file> <log_file> <result_range_start> <result_range_end>")
        sys.exit(1)

    # получение аргументов из командной строки
    input_file = sys.argv[1] # путь к обрабатываемому файлу
    binary_file = sys.argv[2] # путь к бинарному файлу для записи результата работы ассемблера
    log_file = sys.argv[3] # путь к лог-файлу
    result_range_start = int(sys.argv[4]) # начало участка памяти, хранящего результат
    result_range_end = int(sys.argv[5]) # конец участка памяти, хранящего результат

    assemble(input_file, binary_file, log_file) # ассемблирование команд

    vm = VirtualMachine()
    vm.load_program(binary_file) # загрузка ассемблированных команд в память УВМ
    results = vm.execute(result_range_start, result_range_end) # интерпретация команд

    # запись результатов в XML файл
    root_results = ET.Element("memory_units")
    count = int(result_range_start)
    for i in range(len(results)):
        result_element = ET.SubElement(root_results, f"unit{count}")
        result_element.text = str(results[i])
        count += 1

    xml_str = ET.tostring(root_results).decode()
    pretty_sml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    pretty_sml_str = '\n'.join(pretty_sml_str.split('\n')[1:])
    with open("results.xml", 'w') as res_f:
        res_f.write(pretty_sml_str)  # запись в лог-файл

