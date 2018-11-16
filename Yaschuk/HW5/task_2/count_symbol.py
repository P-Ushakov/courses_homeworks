from string import ascii_letters as a_l
import collections


if __name__ == '__main__':
    while True:
        try:
            user_input_path = input('Please enter path file: ')
            with open(user_input_path) as f_l:
                f_l = f_l.read()
            break
        except FileNotFoundError:
            continue
        except OSError:
            continue

    a = {}
    b = []
    for sym in f_l:
        a[sym] = a.setdefault(sym, 0) + 1

    b = [key for key, val in a.items() if val == max(a.values())]

    if b[0] == " " or ' ':
        a = collections.Counter(a)
        a = a.most_common(2)

    print(a)
