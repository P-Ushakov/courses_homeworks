import os
from sys import argv


def get_dir():
    """
    Getting directory path
    """
    if len(argv) <= 1:
        return input('Please enter a directory: ').strip()
    return argv[1]


def check_dir():
    """
    Checking directory for existing
    :return: root_dir or False
    """
    root_dir = os.path.abspath(root_dir)
    if os.path.isdir(root_dir):
        return root_dir
    else:
        return False


def resolve_dir(directory):
    """
    Transforming directories to tuples
    get: existing directory
    :return: directory, dirs, files
    """
    contents = os.listdir(directory)
    dirs = []
    files = []
    #Instead of we can use listcomprehension
    for element in contents:
        if os.path.isdir(os.path.join(directory, element)):
            dirs.append(os.path.join(directory, element))
        elif os.path.isfile(os.path.join(directory, element)):
            files.append(element)
    return directory, dirs, files


def walk(root_dir):
    """
    :get: root dir
    :return: generator object(no implementation)
    """
    #List with 1 element
    dirs = [root_dir]
    for directory in dirs:
        res = resolve_dir(directory)    #making a tuple
        dirs.extend(res[1])
        yield res


def main():
    """
    :get: generator object walk()
    :return: main result object
    """
    root_dir = get_dir()
    return walk(root_dir)


if __name__ == '__main__':
    #Showing result of generator
    for elem in main():
        print(elem)
