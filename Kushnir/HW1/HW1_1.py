import random
print("You are welcome to the first task")
user_number = int(input("Please enter number (more than 0): " ))
if user_number <=  0:
    print("Error! Please enter number again.")
else:
    print(user_number)
    random_choice = random.randint(0, user_number)
    print("Random number is", random_choice)
    result = random.sample( range(0, user_number), random_choice)
    print(result)

