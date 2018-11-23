import os


def q_2(s):
    w = [x for x in os.listdir(path=file_path[i]) if s(file_path[i] + '//' + x) is True]
    return w


def path_1(fold):
    a_path = [file_path[i] + '//' + x for x in fold]
    return a_path


def walk():
    try:
        global i
        catalog = (os.path.abspath(file_path[i]), (q_2(os.path.isdir)), (q_2(os.path.isfile)))
        file_path.extend(path_1(catalog[1]))
        walk_list.append(catalog)
        i += 1
        return walk()
    except IndexError:
        for inside_walk in walk_list:
            print(inside_walk)


def input_1():
    user_input = input('Please enter the path file: ')
    if os.path.exists(user_input) is True:
        return user_input
    exit(1)


if __name__ == '__main__':
    file_path = [input_1()]
    walk_list = []
    i = 0
    walk()
