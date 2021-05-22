'''
Most credit card numbers, and many other identification numbers including the Canadian Social Insurance Number, can be validated by an algorithm developed by Hans Peter Luhn of IBM, described in U. S. Patent 2950048 in 1954 (software patents are nothing new!), and now in the public domain. The Luhn algorithm will detect almost any single-digit error, almost all transpositions of adjacent digits except 09 and 90, and many other errors.

The Luhn algorithm works from right-to-left, with the right-most digit being the check digit. Alternate digits, starting with the first digit to left of the check digit, are doubled. Then the digit-sums of all the numbers, both undoubled and doubled, are added. The number is valid if the sum is divisible by ten.

For example, the number 49927398716 is valid according to the Luhn algorithm. Starting from the right, the sum is 6 + (2) + 7 + (1 + 6) + 9 + (6) + 7 + (4) + 9 + (1 + 8) + 4 = 70, which is divisible by 10; the digit-sums of the doubled digits have been shown in parentheses.

Your task is to write two functions, one that adds a check digit to a identifying number and one that tests if an identifying number is valid.
'''

def find_check(code, length):
	for i in range(length-1, 0, -2):
		code[i] = str(int(code[i]) * 2)
	
def check_valid(code, length):
	for i in range(length-2, 0, -2):
		code[i] = str(int(code[i]) * 2)


def calculate(data, option):
	length = len(data)
	code = list(data)
	
	# double alternate numbers
	if (option == 0):
		find_check(code, length)
	elif (option == 1):
		check_valid(code, length)
		
	# add undoubled and doubed numbers
	total = 0
	for i in range(0, length):
		if (int(code[i]) > 9):
			total += int(code[i]) % 10
			total += 1
		
		else:
			total += int(code[i])
			
	return total

def check_digit(data):
	total = calculate(data, 0)
			
	count = 0
	while (total % 10 != 0):
		count += 1
		total += 1
			
	data += str(count)
	
	print(str(count) + " => " + data)
		
	return
	
def valid_num(data):
	total = calculate(data, 1)
	
	if (total % 10 == 0):
		print(data + " is valid!")
	else:
		print(data + " is not valid!")
	
	return
	
check_digit("4992739871")
valid_num("49927398716")
valid_num("49927398714")
