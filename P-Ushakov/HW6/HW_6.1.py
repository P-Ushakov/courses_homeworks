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


# help message
def hlp_message():
    return "This function accepts: [str:path] [int:1-3]"


# get input path
def inp(arg=[]):
    if len(arg) <= 1:
        i = input('Please input path:')
        return i
    else:
        return arg[1]


# check input path
def inp_check(i=""):
    if os.path.isdir(i):
        return i                     # possible solution: return os.path.abspath(i)
    elif i in ("--help", "-help"):
        print(hlp_message())
        exit(0)
    else:
        print("The path is wrong!")
        exit(1)


# get input task
def task(arg=[]):
    if len(arg) <= 2:
        t = input('Please enter:\n'
                  ' "1" to see the folder tree\n'
                  ' "2" to see the size of largest file\n'
                  ' "3" to see the sorted list of folders and suborders:')
        return t
    else:
        return arg[2]


# check input task
def task_check(t=0):
    try:
        t = int(t)
    except ValueError:
        print("Not a number.", hlp_message())
        exit(1)
    if t not in (1, 2, 3):
        print("Your decision isn't clear.", hlp_message())
        exit(1)
    return t


# form one element of walk object
def walk_tuple(path):
    try:
        dr = os.listdir(path)
    except PermissionError:
        dr = []
    dirs = tuple(d for d in dr if os.path.isdir(os.path.join(path, d)))
    files = tuple(f for f in dr if os.path.isfile(os.path.join(path, f)))
    return path, dirs, files


# recursive walk generator
def recursive_walk(path):
    path, dirs, files = walk_tuple(path)
    for dr in dirs:
        dir_path = os.path.join(path, dr)
        inner_walk = recursive_walk(dir_path)
        for p, d, f in inner_walk:
            yield p, d, f
    yield path, dirs, files


# calculate file size
def file_size_calc(file):
    return os.path.getsize(file)


# generator of files with path and sizes ((path+file, size) , (path+file, size) , ...)
def fls_info(walk_obj):
    for walk_tpl in walk_obj:
        for f in walk_tpl[2]:
            file_with_path = os.path.join(walk_tpl[0], f)
            size = file_size_calc(file_with_path)
            yield file_with_path, size


# return func for max file
def max_file_decorator(func_fls_info):
    def inner(walk_obj):
        try:
            result = max([x for x in func_fls_info(walk_obj)], key=lambda x: x[1])
        except ValueError:
            return '', 0
        return result
    return inner


# accept walk_object return (file_with_path, max_size) or ('', 0) if empty input
max_file = max_file_decorator(fls_info)


# return func for dir sort
def dir_sort_decorator(func_fls_info):
    def inner(walk_obj):
        result = [(0, '', '')]
        for wlk in walk_obj:
            w = wlk,
            dir_files_sum = sum(x[1] for x in func_fls_info(w))
            dir_size_tuple = dir_files_sum, wlk[0], wlk[1]
            for r in result:
                if dir_files_sum > r[0]:
                    result.insert(result.index(r), dir_size_tuple)
                    break
        result.remove((0, '', ''))
        return tuple(result)
    return inner


# accept walk object, return sorted list: (size, dir, (subdirs, ...), ...)
dir_sort = dir_sort_decorator(fls_info)


# level of subdirs in walk_tuple. Accept str: path, tuple: walk_tuple
def deep_level(path, walk_tuple):
    head = walk_tuple[0]
    counter = 0
    while len(head) > len(path):
        head, body = os.path.split(head)
        counter += 1
    return counter


# return index to add new element or -1
def find_list_tree_index(input_path, full_path, list_tree):
    index = -1
    enum_list_tree = enumerate(list_tree)
    while len(full_path) >= len(input_path):
        full_path, right_part = os.path.split(full_path)
        for elt in enum_list_tree:
            compared_part = elt[1][0][0:len(full_path)]
            if full_path == compared_part:
                index = elt[0]
                break
    return index


def tree(input_path):
    input_path = os.path.abspath(input_path)
    wlk = recursive_walk(input_path)
    # list_tree accept:[full_path, is_dir, is_last = None for root, deep_level, element]
    list_tree = [(input_path, True, None, 0, os.path.split(input_path)[1])]
    for wlk_tuple in wlk:
        deep = deep_level(input_path, wlk_tuple)
        is_last = True
        is_dir = False
        fl_dir, dirs, fls = wlk_tuple
        dirs, fls = map(lambda x: sorted(list(x)), (dirs, fls))
        #todo: take index out of the scope
        for fl in fls:
            full_path = os.path.join(fl_dir, fl)
            index = find_list_tree_index(input_path, full_path, list_tree)
            list_tree.insert(index, (full_path, is_dir, is_last, deep,  fl))
            is_last = False


    # for wlk_tuple in sorted(list(wlk)):
    #     deep = deep_level(path, wlk_tuple)
    #     print(' |'*deep, "-", os.path.split(wlk_tuple[0])[1])


def main():
    # get data
    p = (inp_check(inp(argv)))
    t = (task_check(task(argv)))
    wlk = recursive_walk(p)
    # form the tree
    if t == 1:
        tree(p)
    # find max file
    elif t == 2:
        max_fl = max_file(wlk)
        print(f'The Max file is {max_fl[0]} with size: {max_fl[1]} bytes')
    #  sorted list of dirs
    elif t == 3:
        for row in dir_sort(wlk):
            print(f'{row[0]} kb   dir: {row[1]}  subdirectories: {row[2]}')
    # can be used to add another functions
    else:
        raise ValueError


if __name__ == '__main__':
    main()

