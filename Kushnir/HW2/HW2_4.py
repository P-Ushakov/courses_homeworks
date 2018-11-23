quantity = int(input('Your number: '))

for i in range(quantity + 1):
	text = "* "
	piramid = " " * (quantity - i) + text * i
	print(piramid)


 
