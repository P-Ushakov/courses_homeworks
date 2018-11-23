import os


def user_path():
    try:
        user_input = input('Which path to walk? \n')
        os.stat(user_input)
    except FileNotFoundError:
        return user_path()
    return user_input


def all_in(path):
    all1 = []
    dirs = [elements for elements in os.listdir(path)
            if os.path.isdir(os.path.join(path, elements))]
    files = [file for file in os.listdir(path)
             if os.path.isfile(os.path.join(path, file))]
    all1.append([[path], dirs, files])
    for dir in all1[0][1]:
        all1.append(all_in(os.path.join(path, dir)))
    return all1


if __name__ == '__main__':
    for elements in all_in(user_path()):
        print(elements)
