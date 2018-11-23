user_input = int(input("Введите число: "))
lis = list(range(2, user_input)) 

print(lis)

for i in lis:
	if i != 0:
		for j in range(2 * i, user_input, i):
			lis[j - 2] = 0

lis2 = [i for i in lis if i != 0]
print('Простые числа до числа ', user_input, ':\n', lis2)

