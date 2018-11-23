
attempts = 0
while True:
	try:
		user_input = int(input("Please enter year: "))
	except ValueError:
		attempts += 1
		if attempts >= 3: # not == because of possible future changes in code
			print("You are fucken looser!")
			exit()
		print("Please enter a number, man")
		continue
	if user_input % 4 == 0:
		print("This is a leap year")
		exit()
	elif user_input % 4 > 2:
		user_input += 1
	elif user_input % 4 == 2:
		user_input += 2
	elif user_input % 4 < 2:
		user_input -= 1
	else:
		print("404 not found")
	print(f"The closest leap year is {user_input}")
	exit()
