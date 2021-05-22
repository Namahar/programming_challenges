'''
Description

ISBN's (International Standard Book Numbers) are identifiers for books. Given the correct sequence of digits, one book can be identified out of millions of others thanks to this ISBN. But when is an ISBN not just a random slurry of digits? That's for you to find out.
Rules

Given the following constraints of the ISBN number, you should write a function that can return True if a number is a valid ISBN and False otherwise.

An ISBN is a ten digit code which identifies a book. The first nine digits represent the book and the last digit is used to make sure the ISBN is correct.

To verify an ISBN you :-

    obtain the sum of 10 times the first digit, 9 times the second digit, 8 times the third digit... all the way till you add 1 times the last digit. If the sum leaves no remainder when divided by 11 the code is a valid ISBN.

For example :

0-7475-3269-9 is Valid because

(10 * 0) + (9 * 7) + (8 * 4) + (7 * 7) + (6 * 5) + (5 * 3) + (4 * 2) + (3 * 6) + (2 * 9) + (1 * 9) = 242 which can be divided by 11 and have no remainder.

For the cases where the last digit has to equal to ten, the last digit is written as X. For example 156881111X.
Bonus

Write an ISBN generator. That is, a programme that will output a valid ISBN number (bonus if you output an ISBN that is already in use :P )
'''

import random

def valid_isbn(data):

	multiplier = 10
	total = 0
	code = list(data)
	length = len(code)
	
	
	# check if last digit is X
	if code[length - 1] == 'X':
		code[length - 1] = str(10)

	for i in range(length):	
		total += int(code[i]) * multiplier
		
		# decrease multiplier
		multiplier -= 1
		
	if (total % 11 == 0):
		print(data + " is a valid ISBN!")
		
	else:
		print(data + " is not a valid ISBN!")

	return
	
def isbn_generator():
	
	code = []
	total = 0
	multiplier = 10
	
	for i in range(9):
		code.append(random.randint(0, 9))
		total += code[i] * multiplier	
		multiplier -= 1

	checksum = 11 - (total % 11)
	
	if checksum == 11:
		checksum = 0
	
	if checksum == 10:
		code.append("X")
		
	else:
		code.append(checksum)
	
	data = ''.join(str(val) for val in code)
	valid_isbn(data)
	
	return
	
#valid_isbn("0747532699")
#valid_isbn("156881111X")
#valid_isbn("1568811114")
isbn_generator()

