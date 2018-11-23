import random

arr = []
for i in range(25):
	arr.append(random.randint(0, 100))
	
print('The list of numbers before buble sorting: \n', arr)

#Buble sorting

for i in range(len(arr), 0, -1):
	for j in range(0, len(arr) - 1):
		if arr[j] > arr[j + 1]:
			arr[j], arr[j+1] = arr[j+1], arr[j]
			#array2.append(arr[j]) 

print('The list of numbers after buble sorting: \n', arr)
