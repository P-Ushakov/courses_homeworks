import os
import operator

def check(path):
    #path = nput('Please enter path to your file: \n')
    check = os.path.isfile(path)
    if check is True:
        return path#mk_dict(path)
    else:
        print('The file does not exist. Please enter file again! ')
        searching()


def searching():
    path = input('Please enter path to your file: \n')
    check(path)
    with open(path, 'r') as f:
        f = f.read()
        fr = {}
        for symbol in f:
            fr[symbol] = fr.setdefault(symbol, 0) + 1
        fr = sorted(fr.items(), key=lambda x: x[1], reverse=True)
        v = list(fr)
        if v[0][0] == ' ':
                print('The most often used symbol is: ', v[1][0])
        else:
            print(v[0][0])
        exit()


def main():
    searching()


if __name__ == '__main__':
    main()
