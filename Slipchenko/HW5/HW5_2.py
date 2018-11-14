import os


def user_path():
    try:
        user_input = input('Which path to walk? \n')
        os.stat(user_input)
    except FileNotFoundError:
        return user_path()
    return user_input


def all_in_path(path):
    all1 = []
    dirs = []
    files = []
    for elem in os.listdir(path):
        if os.path.isdir(os.path.join(path, elem)):
            dirs.append(elem)
        elif os.path.isfile(os.path.join(path, elem)):
            files.append(elem)
    all1.append([[path], sorted(dirs), files])
    for paths in sorted(dirs):
        dirs1 = []
        files1 = []
        for element in os.listdir(os.path.join(path, paths)):
            if os.path.isdir(os.path.join(path, paths, element)):
                dirs1.append(element)
            elif os.path.isfile(os.path.join(path, paths, element)):
                files1.append(element)
        all1.append([[os.path.join(path, paths)], dirs1, files1])
    for j in range(1, len(all1)):
        for el in all1[j][1]:
            dirs2 = []
            files2 = []
            if el != 0:
                for l in os.listdir(os.path.join(''.join(all1[j][0]), el)):
                    if os.path.isdir(os.path.join(''.join(all1[j][0]), el, l)):
                        dirs2.append(l)
                    elif os.path.isfile(os.path.join(
                            ''.join(all1[j][0]), el, l)):
                        files2.append(l)
                all1.append([[os.path.join(
                    ''.join(all1[j][0]), el)], dirs2, files2])
    return all1


if __name__ == '__main__':
    for elements in all_in_path(user_path()):
        print(elements, sep='\n')
