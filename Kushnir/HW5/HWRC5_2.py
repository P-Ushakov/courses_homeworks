from HW5_2 import main, resolve_dir


def walk(root_dir):
    """
    Changing one function
    """
    res = resolve_dir(root_dir)
    yield res
    for director in res:
        for element in walk(directory):
            yield element


if __name__ == '__main__':
    for i in main():
        print(i)
