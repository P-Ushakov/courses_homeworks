"""
5.2
В стандартном модуле os есть функция walk() которая получает параметром папку,
а после выводит все фалы в ней, папки, под папки, файлы в подпапках и так пока не выведет все что есть.
Ваша задача написать копию этой функции в двух экземплярах:
Рекурсивно
Не рекурсивно
"""
# not recursively
import os


def path_adapter(path_str='', convert_to_abspath=False):
    """
    Convert Path to used OS between Windows, Linux

    :param path_str: path to be converted
    :param convert_to_abspath: if True - return absolute path
    :return: path_string, separator
    """
    if os.name == "nt":
        path_str = '\\'.join(path_str.split("/"))
        slash = '\\'
    else:
        path_str = '/'.join(path_str.split("\\"))
        slash = '/'
    if convert_to_abspath:
        path_str = os.path.abspath(path_str)
    return path_str, slash


def my_tuple(path="", searator='/'):
    """
    Run listdir and make walk_object tuple and dirs to visit tuple
    :param path: dir path
    :param separator: in linux '/' in windows '\\'
    :return: ("dir path", (dirs...),(files...)) , (dirs to visit)
    """
    list_dir = os.listdir(path)
    dirs = [f for f in list_dir if os.path.isdir(path + searator + f)]
    files = tuple(f for f in list_dir if os.path.isfile(path + searator + f))
    dirs_to_visit = tuple(map(lambda x: (path + searator + x), dirs))

    return (path, tuple(dirs), files), dirs_to_visit


def my_walk(path='.', abspath=False):
    """
    my walk non recursive function

    :param path: path for walk
    :param abspath: convert path to absolute path if given relative
    :return: walk_list [str: directory path , (directory_1 , ...), (file_1, ...)]
    """
    # converting path. Use True if want to use abspath
    path, slash = path_adapter(path, abspath)

    w, n = my_tuple(path, slash)
    walk_list = [w]
    not_visited = [*n]

    while not_visited != []:
        w, n = my_tuple(not_visited.pop(0), slash)
        walk_list.append(w)
        not_visited += n
    walk_list.sort()

    return walk_list


if __name__ == '__main__':
    p = input("Please input the path:")
    if not os.path.exists(p):
        print("Sorry, this path doesn't exist")
        if input("Should I use default path? y/n or Enter:") in ("y", ""):
            p = '..\\..'
        else:
            exit()

    abspath = False
    if input("Do You want to use absolute path y/n or Enter:") in ("y", ""):
        abspath = True

    # run my_walk
    a = my_walk(p, abspath)

    if input("Print result to console? y/n or Enter:") in ("y", ""):
        for row in a:
            print(row)


