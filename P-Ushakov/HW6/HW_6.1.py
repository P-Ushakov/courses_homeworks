"""
6.1
Написать скрипт, который принимает папку (параметром, если нет параметра - ввод от пользователя), а после:
Написать что-то в стиле меню:

Если пользователь ввел 1: вывести дерево этой папки (саму папку, папки в ней и так далее).
С отступами и что б все по красоте было.
Если два - выведет путь к файлу занимающим больше всего памяти
Если 3 - выведет отсортированный список папок и подпапок.
Сортировать по принципу - папка занимающая больше всего места - выше в списке
Не использовать os.walk, так-же не использовать os.system (или ему подобные).
Старайтесь максимально разбивать на функции и писать генераторы. Удачи )
"""

import os
from sys import argv


def inp(arg=[]):
    if len(arg)<=1:
        i = input('Please input path:')
        return i
    else:
        return arg[1]


def inp_check(i=""):
    if os.path.isdir(i):
        return os.path.abspath(i)
    elif i in ("--help", "-help"):
        print(hlp_message())
        exit(0)
    else:
        print("The path is wrong!")
        exit(1)


def task(arg=[]):
    if len(arg) <= 2:
        t = input('Please enter:\n'
                  ' "1" to see the folder tree\n'
                  ' "2" to see the size of largest file\n'
                  ' "3" to see the folder tree, sorted by size:')
        return t
    else:
        return arg[2]


def task_check(t=0):
    try:
        t = int(t)
    except ValueError:
        print("No a number.", hlp_message())
        exit(1)
    if t not in (1, 2, 3):
        print("Your decision isn't clear.", hlp_message())
        exit(1)
    return t


def hlp_message():
    return "This function accepts: [str:path] [int:1-3]"


def file_size_calc(file):
    return os.path.getsize(file)


def walk_tuple(path):
    dr = os.listdir(path)
    dirs = [d for d in dr if os.path.isdir(d) is True]
    files = [f for f in dr if os.path.isfile(f) is True]
    return path, dirs, files


def file_sizes(files):
    counts = tuple(map(file_size_calc, files))
    return zip(files, counts)


def max_file(files):
    try:
        m = max(file_sizes(files), key=lambda item: item[1])
    except ValueError:
        m = ("", 0)
    return m


def sum_of_files_in_dir(files):
    return sum(element[1] for element in file_sizes(files))


def main():
    p = (inp_check(inp(argv)))
    t = (task_check(task(argv)))

    if t == 1:
        pass
    elif t == 2:
        max_fl = max_file(walk_tuple(p)[2])
        print(f'The Max file is {max_fl[0]} with size: {max_fl[1]}')


if __name__ == '__main__':
    main()

