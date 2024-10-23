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
            if not parts or parts[0] == 'END':
                continue
            command = parts[0]
            if command == 'LOAD_CONST': # обработка загрузки константы
                A, B, C = map(int, parts[1:]) # получение значений аргументов и перевод их в int числа
                instruction = struct.pack('>BHI', A, B, C & 0xFFFFFF) # перевод аргументов в байт строку
                instruction = instruction[:3] + bytes([(C >> 16) & 0xFF, (C >> 8) & 0xFF, C & 0xFF]) # удаление лишнего байта для аргумента С
                instructions.append(instruction) # добавление инструкции в список для хранения инструкций
                log_entries.append((command, A, B, C)) # добавление кортежа аргументов инструкции для лог-файла

            elif command == 'READ_MEM': # обработа чтения из памяти
                A, B, C = map(int, parts[1:])
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append((command, A, B, C))

            elif command == 'WRITE_MEM':
                A, B, C = map(int, parts[1:]) # обработка записи в память
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append((command, A, B, C))

            elif command == 'POP_CNT':
                A, B, C = map(int, parts[1:]) # обработка операции popcnt()
                instruction = struct.pack('>BHH', A, B, C)
                instructions.append(instruction)
                log_entries.append((command, A, B, C))

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


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input_file> <binary_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, binary_file, log_file)

