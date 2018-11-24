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
    dirs = tuple(sorted(d for d in dr if os.path.isdir(os.path.join(path, d))))
    files = tuple(sorted(f for f in dr if os.path.isfile(os.path.join(path, f))))
    return path, dirs, files


# recursive walk generator
def recursive_walk(path):
    path, dirs, files = walk_tuple(path)
    yield path, dirs, files
    for dr in dirs:
        dir_path = os.path.join(path, dr)
        inner_walk = recursive_walk(dir_path)
        for p, d, f in inner_walk:
            yield p, d, f



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


# return True if dir is last in last stack tuple
def is_last(stack, dir):
    if stack != []:
        dir_in_path = os.path.split(dir)[1]
        dir_in_stack = stack[-1][2][-1]
    if stack != [] and dir_in_path == dir_in_stack:
        return True
    else:
        return False


def tree_row(deep, element, is_last = False, is_dir = False):
    if not is_last:
        return " \u2223"*deep + "\u02EA" + element
    else:
        return " \u2223"*deep + "\u02EB" + element


def tree(input_path):
    input_path = os.path.abspath(input_path)
    wlk = recursive_walk(input_path)
    stack = []
    for wlk_tuple in wlk:
        deep = deep_level(input_path, wlk_tuple)
        fl_dir, dirs, fls = wlk_tuple

        # check is it last dir of level above
        islast = is_last(stack, fl_dir)

        output_string = tree_row(deep, os.path.split(fl_dir)[1], islast, True)
        yield output_string

        if dirs == ():
            for fl in fls:
                output_string = tree_row(deep, fl)
                yield output_string
            if islast:
                while stack != [] and islast:
                    last_element = stack.pop(len(stack)-1)
                    for fl in last_element[3]:
                        output_string = tree_row(deep, fl)
                        yield output_string
                    fl_dir = os.path.split(fl_dir)[0]
                    islast = is_last(stack, fl_dir)

        # add tuple to stack and form output string
        if dirs != ():
            stack.append((deep, fl_dir, dirs, fls))



def main():
    # get data
    p = (inp_check(inp(argv)))
    t = (task_check(task(argv)))
    wlk = recursive_walk(p)
    # form the tree
    if t == 1:
        t = tree(p)
        for row in t:
            print(row)
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

