# Домашняя работа №4 по предмету "Конфигурационное управление" студента группы ИКБО-40-23 Савинского Владимира Олеговича

## Постановка задачи

Разработать ассемблер и интерпретатор для учебной вирутальной машины (УВМ). Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задаётся из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задаётся из командной строки. Дополнительный ключ командной строки задаёт путь к файлу-логу, в котором хранятся ассемблированные инфтрсукции в духе списков "ключ=значение", как в приведённых далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ м сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.

Форматом для файла-лога и файла-результата является xml.

Система команд УВМ:
- Загрузка константы. Размер команды: 6 байт. Операнд: поле C. Результат: ячейка памяти по адресу, которым является поле B. Тест (A = 214, B = 313, C = 561): 0xD6, 0x39, 0x01, 0x02, 0x00;
- Чтение из памяти. Размер команды: 5 байт. Операнд: ячейка памяти, по адресу, которым является ячейка памяти по адресу, которым является поле C. Результат: ячейка памяти по адресу, которым является поле B. Тест (A = 138, B = 37, C = 265): 0x8A, 0x25, 0x00, 0x09, 0x01;
- Запись в память. Размер команды: 5 байт. Операнд: ячейка памяти по адресу, которым является поле B. Результат: ячейка памяти по адресу, которым является ячейка памяти по адресу, которым является поле С. Тест (A = 9, B = 191, C = 666): 0x09, 0xBF, 0x00, 0x9A, 0x02;
- Унарная операция popcnt(). Размер команды: 5 байт. Операнд: ячейка памяти по адресу, которым является поле С. Результат: ячейка памяти по адресу, которым является ячейка памяти по адресу, которым является поле B. Тест (A = 241, B = 626, C = 97): 0xF1, 0x72, 0x02, 0x61, 0x00.

Тестовая программа: выполнить поэлементо операцию popcnt() над вектором длины 6; результат записать в новый вектор.

## Содержимое проекта

Файл assembler_test.asm - программа для тестирования всех команд АВМ.
Файл log.xml - лог-файл.
Файл main.py - файл, реализующий ассемблер и интерпретатор.
Файл main_test.asm - основная тестовая программа.
Файл program.bin - бинарный файл, содержащий результат работы ассемблера.
Файл results.xml - файл, содержащий участок памяти УВМ, ограниченный введёнными ключами.

## Тестирование

При запуске программы на файле для тестирования assembler_test.asm имеем результат работы ассемблера, представленный на рисунке ниже.
![image](https://github.com/user-attachments/assets/fbb4b54d-2fe5-4372-bf4c-c085d0810e4c)

Ввиду большого разброса тестовых данных по памяти содержимое файла results.xml не приводится.

При запуске программы на файле для тестирования main_test.asm имеем результат работы ассемблера, представленный на рисунке ниже.
![image](https://github.com/user-attachments/assets/83a597fa-a6f8-4d14-87b4-ee03f94f9265)

При этом в файле results.xml имеем содержимое участка памяти, представленное на рисунке ниже.
![image](https://github.com/user-attachments/assets/2505c6c2-f7cc-4728-ab30-57008d00a18d)



