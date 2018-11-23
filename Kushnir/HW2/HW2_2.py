import random

#Here we create a list with logins, passwords, random numbers.

users = {
	"Ivanov":{
		"password": "fuyuf51",
		"random_number": random.sample(range(999), 1)
	},
	"Petrov":{
		"password": "fuyuf52",
		"random_number": random.sample(range(999), 1)
	},
	"PEtrov":{
		"password": "fuyuf54",
		"random_number": random.sample(range(999), 1)
	},
	"korsunov":{
		"password": "fuyuf55", 
		"random_number": random.sample(range(999), 1)
	},
	"ptashka":{
		"password": "fuyu56f",
		"random_number": random.sample(range(999), 1)
	},
	"king23":{
		"password": "fu5yuf7",
		"random_number": random.sample(range(999), 1)
	},
	"queen231":{
		"password": "fuy58uf",
		"random_number": random.sample(range(999), 1)
	},
	"prince231":{
		"password": "fuyu5f9",
		"random_number": random.sample(range(999), 1)
	},
	"princes3232":{
		"password": "fuy6u0f",
		"random_number": random.sample(range(999), 1)
	},
	"graf":{
		"password": "f6uyuf1",
		"random_number": random.sample(range(999), 1)
	}
}

#Getting login and password from user.
login_input = input('Enter your login: ')


#Checking login and password.

if login_input in users:	
	
	password_input = input('Please, enter your password: ')
	if password_input in users[login_input]["password"]:
		print("Your random number is ",users[login_input]["random_number"])
	else:
#Adding new user to a dictionary
		print("Error! Try again.")

else:
	print("We didn't find the user with login you provided. We create a new one for you!")
	
	pass_creative = input("Please enter your password: ")
	users[login_input] = {"password": pass_creative, "random_number": random.sample(range(999), 1)}
	print("Your login ", login_input, "Successfully added to our list!")


