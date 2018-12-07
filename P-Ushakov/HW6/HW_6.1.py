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
import AsyncWalk


# help message
def hlp_message():
    return "This function accepts: [str:path] [int:1-3]"


# get input path
def inp(arg=[]):
    """
    User can enter arguments after file [path task]. Function accept ARGV, and check,
    if present first parameter
    :param arg: sys.argv or nothing
    :return: str: first file argument or user input (suppose to be path)
    """
    if len(arg) <= 1:
        i = input('Please input path:')
        return i
    else:
        return arg[1]


# check input path
def inp_check(i=""):
    """
    Checking, if path data is correct
    :param i: str: path to directory, "--help" for help message
    :return: path if path is correct or help message if "--help" or error
    """
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
    """
    Take task number from ARGV or if file haven't second argument - ask user input
    :param arg: sys.argv
    :return: int: number of task to execute
    """
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
    """
    Check if entered data is valid task number
    :param t: int: task number
    :return: int task number if task is valid or error
    """
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
    """
    Use system directory list command to scan given path
    Form walk tuple (dir_path, (dir1, dir2, ...), (file1, file2, ...))

    :param path: str: path to scan
    :return: tuple: (dir_path, (dir1, dir2, ...), (file1, file2, ...))
    """
    try:
        dr = os.listdir(path)
    except PermissionError:         # exception to pass directories with denied access
        dr = []
    except OSError:                 # exception to pass "wine" directories
        dr = []
    dirs = tuple(sorted(d for d in dr if os.path.isdir(os.path.join(path, d))))
    files = tuple(sorted(f for f in dr if os.path.isfile(os.path.join(path, f))))
    return path, dirs, files


# recursive walk generator
def recursive_walk(path):
    """
    Recursively walk through all directories from given path
    :param path: str: path to walk
    :return: generator with walk tuples (dir_path, (dir1, dir2, ...), (file1, file2, ...))
    """
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
    """
    Calculate size of files of walk object
    :param walk_obj: walk object
    :return: tuple (file with path, file size)
    """
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
        """
        This function return list of tuples (dir_position, dir_name, sum of all file sizes)
        :param walk_obj: Walk object
        :return: list of tuples (dir_position, dir_name, sum of all file sizes)
        """
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


# return True if dir is last dir in last stack tuple
def is_last_dir(stack, dir, include_files=False):
    if stack != []:
        dir_in_path = os.path.split(dir)[1]
        dir_in_stack = stack[-1][2][-1]
        fls_in_stack = stack[-1][3]
        if dir_in_path == dir_in_stack:
            if not include_files:
                return True
            else:
                if fls_in_stack == ():
                    return True
    return False


def tree_row(deep, element, is_lst=False, is_dir=True, deep_map=[]):
    """
    Form tree row for printing
    :param deep: INT relative level of inclusion from given path
    :param element: STR directory or file to print
    :param is_lst: True if this directory is last (needed to add files after last dir)
    :param is_dir: True if element is directory
    :param deep_map: list with numbers of finished roots to change root line to space
    :return: STR: string to print
    """
    str_f = ""
    str_last = "\u251C"
    list_deep = ["\u2502  " for x in range(0, deep)]

    # change pillars to spaces, if directory haven't files
    for r in deep_map:
            list_deep[r] = "   "
    # file tail is longer for better separation
    if not is_dir:
        str_f = "\u2500\u2500"
    # if dir is last we change last symbol; to conner instead turned "T"
    if is_lst:
        str_last = "\u2514"

    row_with_pillars = "".join(list_deep)

    return row_with_pillars + str_last + str_f + element


# reduce map of roots if walk exit from sub folders
def deep_map_reduce(deep_map, deep=0):
    if deep_map != []:
        sorted(deep_map)
        while deep_map[-1] > deep:
            deep_map.remove(deep_map[-1])
            if deep_map == []:
                break
    return deep_map


def tree(input_path):
    """
    Generator to form the printed tree of directories
    :param input_path: STR: root path to start build the tree
    :return: STR tree rows
    """
    input_path = os.path.abspath(input_path)
    yield os.path.split(input_path)[0]
    wlk = recursive_walk(input_path)
    stack = []
    deep_map = []
    for wlk_tuple in wlk:
        deep = deep_level(input_path, wlk_tuple)
        fl_dir, dirs, fls = wlk_tuple

        # check is it last dir of level above
        islast = is_last_dir(stack, fl_dir)
        # check is last dir of level above and level above haven't files
        islastelement = is_last_dir(stack, fl_dir, True)

        # print directory
        output_string = tree_row(deep, os.path.split(fl_dir)[1], islastelement, True, deep_map=deep_map)
        yield output_string

        # map with roots and spaces
        deep_map = deep_map_reduce(deep_map, deep)
        if islastelement:
            deep_map.append(deep)

        # print files
        if dirs == ():
            if fls != ():
                for fl in fls[:-1]:
                    output_string = tree_row(deep+1, fl, is_dir=False, deep_map=deep_map)
                    yield output_string
                output_string = tree_row(deep+1, fls[-1], is_lst=True, is_dir=False, deep_map=deep_map)
                yield output_string

            if islast:
                while stack != [] and islast:
                    last_element = stack.pop(len(stack)-1)
                    if last_element[3] != ():
                        for fl in last_element[3][:-1]:
                            output_string = tree_row(deep, fl, is_dir=False, deep_map=deep_map)
                            yield output_string
                        output_string = tree_row(deep, last_element[3][-1], is_lst=True,
                                                 is_dir=False, deep_map=deep_map)
                        yield output_string
                    deep -= 1
                    fl_dir = os.path.split(fl_dir)[0]
                    islast = is_last_dir(stack, fl_dir)
                    deep_map = deep_map_reduce(deep_map, deep)

        # add walk tuple to stack
        if dirs != ():
            stack.append((deep, fl_dir, dirs, fls))


def main():
    # get data
    p = (inp_check(inp(argv)))
    t = (task_check(task(argv)))
    wlk =AsyncWalk.awalk(p)   # can be used recursive walk wlk = recursive_walk(p)
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
