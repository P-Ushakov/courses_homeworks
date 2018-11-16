"""
5.1
Написать скрипт, который берет файл, введенный пользователем и возвращает самый часто используемый символ в нем.
Чувствительно к регистру. Если самый популярный символ - пробел,
выводить второй по популярности. Если файла нет - просить ввод заново.
"""

import os


def path_input(input_path_to_file=None):
    """
    Checking if user enter correct path to file

    :param input_path_to_file: If argument absent or wrong - asking new path
    :return input_path_to_file or None:
    """
    for tr in range(3):
        if not input_path_to_file:
            input_path_to_file = input("Please enter path and filename with extension:")
        if os.path.isfile(input_path_to_file):
            return input_path_to_file
        else:
            print("Can't find file.")
            input_path_to_file = None

    print("Sorry, the file is not exist or path is wrong")
    exit()


def letter_calc(path):
    if path_input(path):
        with open(path, 'r') as f:
            letters = [" "]
            output = []
            diff_len = 0
            f_str = str(f.read())
            f_str_len = len(f_str)
            for letter in f_str:
                if letter not in letters:
                    letters.append(letter)
                    new_len = len(''.join(f_str.split(letter)))
                    new_diff_len = f_str_len-new_len

                    if diff_len < new_diff_len:
                        diff_len = new_diff_len
                        output = []
                        output.append(letter)
                    elif diff_len == new_diff_len:
                        output.append(letter)
        print("Letters", output, "is most popular after space and found in quantity:", diff_len)


if __name__ == '__main__':
    inp = path_input("HW_5.1.py")
    if inp:
        letter_calc(inp)
