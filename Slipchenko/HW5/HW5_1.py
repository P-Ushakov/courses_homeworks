from collections import Counter


def input_user():
    try:
        with open(input('Which file to open? \n'), 'r') as file:
            return file.read()
    except FileNotFoundError:
        return input_user()


def key_sorting(dictionary):
    sorted_key = sorted(dictionary, key=dictionary.get, reverse=True)
    return sorted_key


if __name__ == '__main__':
    counter = Counter(input_user())
    if key_sorting(counter)[0] == ' ':
        print('The element that repeats the most is "{}"'.format(
                                                    key_sorting(counter)[1]))
    else:
        print('The element that repeats the most is "{}"'.format(
                                                    key_sorting(counter)[0]))
