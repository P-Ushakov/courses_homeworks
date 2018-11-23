import os


def walk():
    for i in path_file:
        def q_2(s):
            w = [d for d in os.listdir(path=i) if s(os.path.join(i, d)) is True]
            return w
        catalog = (os.path.abspath(i), (q_2(os.path.isdir)), (q_2(os.path.isfile)))
        for x in catalog[1]:
            path_file.extend([os.path.join(i, x)])
        rew.append(catalog)

    for dirs in rew:
        print(dirs)


def input_1():
    user_input = input('Please enter the path file: ')
    if os.path.exists(user_input) is True:
        return user_input
    exit(1)


if __name__ == '__main__':
    rew = []
    path_file = [input_1()]
    walk()
