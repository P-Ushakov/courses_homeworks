import random
print ("You are welcome to the second task!")
random_number = random.randint(1000, 1000000)
print("Random number is ", random_number)
print("Fourth element of random number is ", ((random_number % 10000) - (random_number % 1000))//1000)
