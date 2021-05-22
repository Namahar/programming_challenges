# binary search program

import random

def fill(length):
	arr = []

	for i in range(length):
		arr.append(random.randint(0, 100))

	return arr

def bin_search(numbers, val, min, max):
	guess = 0

	while guess != val:
		index = int( (max - min) / 2 ) + min
		guess = numbers[index]

		if guess > val:
			max = index

		elif guess < val:
			min = index

	return guess

def main():
	size = 100
	numbers = fill(size)
	numbers.sort()

	search_val = numbers[random.randint(1, size) - 1]
	min = 0
	max = size - 1

	print(numbers)
	print(search_val)

	ans = bin_search(numbers, search_val, min, max)

	print(ans)

	return

if __name__ == '__main__':
	main()
