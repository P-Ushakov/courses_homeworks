"""
5.2
В стандартном модуле os есть функция walk() которая получает параметром папку,
а после выводит все фалы в ней, папки, под папки, файлы в подпапках и так пока не выведет все что есть.
Ваша задача написать копию этой функции в двух экземплярах:
Рекурсивно
Не рекурсивно
"""
# recursively
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


def my_walk_recursive(path='.', logging=False, abspath=False, deep=0):
    """
    my walk recursive function with logging output

    :param path: path for walk
    :param logging: if True, function make log.txt with result of operation in tree view
    :param abspath: convert path to absolute path if given relative
    :param deep: technical parameter to draw spaces in logging
    :return: walk_list [str: directory path , (directory_1 , ...), (file_1, ...)]
    """
    # converting path. Use True if want to use abspath
    path, slash = path_adapter(path, abspath)

    # divide input list to directories and files
    list_dir = os.listdir(path)
    dirs = [f for f in list_dir if os.path.isdir(path + slash + f)]
    files = [f for f in list_dir if os.path.isfile(path + slash + f)]
    del list_dir    # Destroy object to reduce memory consumption
    mylist = [(path, tuple(dirs), tuple(files))]

    line = ' '*deep
    for dir in dirs:
        if logging:
            with open("log.txt", "a") as log:
                log.write(line + dir + "\n")
        # recursive walking
        mylist += my_walk_recursive(path + slash + dir, logging, abspath, deep + 1)

    for f in files:
        if logging:
            with open("log.txt", "a") as log:
                log.write(line + "-" + f + "\n")

    # Deep 0 means function end recursive walk and ready to return walk_list

    return mylist



if __name__ == '__main__':
    p = input("Please input the path:")
    if not os.path.exists(p):
        print("Sorry, this path doesn't exist")
        if input("Should I use default path? y/n or Enter:") in ("y", ""):
            p = '..\\..'
        else:
            exit()

    logging = False
    if input("Do You want to log data to log.txt? y/n or Enter:") in ("y", ""):
        logging = True

    abspath = False
    if input("Do You want to use absolute path y/n or Enter:") in ("y", ""):
        abspath = True

    # run my_walk
    a = my_walk_recursive(p, logging, abspath)

    if input("Print result to console? y/n or Enter:") in ("y", ""):
        for row in a:
            print(row)
