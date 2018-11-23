import string
import random

rand_numbers_list = []
for i in range(7):
    rand_numbers_list.append(random.randint(13, 48))

rand_numbers_list = sorted(rand_numbers_list, reverse = False)


lis_letters = list(string.ascii_letters)


for i in range(len(rand_numbers_list)):
    print('The string for a number ' + str(rand_numbers_list[i]) + ' with the responsive letter '+ str(lis_letters[rand_numbers_list[i]]) + ' is ' + str(lis_letters[rand_numbers_list[i]]) + 'string' + '\n')
