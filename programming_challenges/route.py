'''
[2018-05-30] Challenge #362 [Intermediate] "Route" Transposition Cipher
Description

You've been taking some classes at a local university. Unfortunately, your theory-of-under-water-basket-weaving professor is really boring. He's also very nosy. In order to pass the time during class, you like sharing notes with your best friend sitting across the aisle. Just in case your professor intercepts any of your notes, you've decided to encrypt them.

To make things easier for yourself, you're going to write a program which will encrypt the notes for you. You've decided a transposition cipher is probably the best suited method for your purposes.

A transposition cipher is "a method of encryption by which the positions held by units of plaintext (which are commonly characters or groups of characters) are shifted according to a regular system, so that the ciphertext constitutes a permutation of the plaintext" (En.wikipedia.org, 2018).

Specifically, we will be implementing a type of route cipher today. In a route cipher the text you want to encrypt is written out in a grid, and then arranged in a given pattern. The pattern can be as simple or complex as you'd like to make it.
Task

For our purposes today, your program should be able to accommodate two input paramters: Grid Dimensions, and Clockwise or Counterclockwise Rotation. To make things easier, your program need only support the Spiral route from outside to inside.
Example

Take the following message as an example:

WE ARE DISCOVERED. FLEE AT ONCE

Given inputs may include punctuation, however the encrypted text should not. Further, given text may be in all caps, all lower case, or a mix of the two. The encrypted text must be in all caps.

You will be given dimensions in which to write out the letters in a grid. For example dimensions of:

9, 3

Would result in 9 columns and 3 rows:

W	E	A	R	E	D	I	S	C
O	V	E	R	E	D	F	L	E
E	A	T	O	N	C	E	X	X

As you can see, all punctuation and spaces have been stripped from the message.

For our cipher, text should be entered into the grid left to right, as seen above.

Encryption begins at the top right. Your route cipher must support a Spiral route around the grid from outside to the inside in either a clockwise or counterclockwise direction.

For example, input parameters of clockwise and (9, 3) would result in the following encrypted output:

CEXXECNOTAEOWEAREDISLFDEREV

Beginning with the C at the top right of the grid, you spiral clockwise along the outside, so the next letter is E, then X, and so on eventually yielding the output above.
Input Description

Input will be organized as follows:

"string" (columns, rows) rotation-direction

.

Note: If the string does not fill in the rectangle of given dimensions perfectly, fill in empty spaces with an X

So

"This is an example" (6, 3)

becomes:

T	H	I	S	I	S
A	N	E	X	A	M
P	L	E	X	X	X

Challenge Inputs

"WE ARE DISCOVERED. FLEE AT ONCE" (9, 3) clockwise
"why is this professor so boring omg" (6, 5) counter-clockwise
"Solving challenges on r/dailyprogrammer is so much fun!!" (8, 6) counter-clockwise
"For lunch let's have peanut-butter and bologna sandwiches" (4, 12) clockwise
"I've even witnessed a grown man satisfy a camel" (9,5) clockwise
"Why does it say paper jam when there is no paper jam?" (3, 14) counter-clockwise

Challenge Outputs

"CEXXECNOTAEOWEAREDISLFDEREV"
"TSIYHWHFSNGOMGXIRORPSIEOBOROSS"
"CGNIVLOSHSYMUCHFUNXXMMLEGNELLAOPERISSOAIADRNROGR"
"LHSENURBGAISEHCNNOATUPHLUFORCTVABEDOSWDALNTTEAEN"
"IGAMXXXXXXXLETRTIVEEVENWASACAYFSIONESSEDNAMNW"
"YHWDSSPEAHTRSPEAMXJPOIENWJPYTEOIAARMEHENAR"

Bonus

A bonus solution will support at least basic decryption as well as encryption.
Bonus 2

Allow for different start positions and/or different routes (spiraling inside-out, zig-zag, etc.), or for entering text by a different pattern, such as top-to-bottom.
'''

import string
import numpy

def stripData(info):
	punctuation = str.maketrans('', '', string.punctuation)
	
	new_data = info.translate(punctuation)
	new_data = new_data.replace(' ', '')
	new_data = new_data.lower()

	return new_data

def stringToMatrix(s, r, c):
	s = list(s)
	m = list()

	for row in range(r):
		start = row*c
		end = c*(row+1)
		m.append(s[start:end])

	m = numpy.array(m)

	return m

def listToString(m):
	s = ''
	for i in range(len(m)):
		s += m[i]
	return s

def encrypt(m, d):
	s = list()

	if d:
		m = numpy.rot90(m, k=-1)	# rotate clockwise to begin

		while len(m) > 0:
			val = m[-1]						# get last value of matrix
			m = m[:-1]						# remove last value in matrix
			val = val[::-1]				# reverse array
			s.extend(val)					# store array
			m = numpy.rot90(m, k=1)		# rotate counterclockwise
			

	else:
		while len(m) > 0:
			val = m[0]						# store top array in matrix
			val = val[::-1]				# reverse array
			s.extend(val)					# store array
			m = m[1:]						# remove array from matrix
			m = numpy.rot90(m, k=-1)	# rotate matrix clockwise

	return s

def main():
	# format is: string, row, column, direction, output
	# direction = 1 => clockwise
	# direction = 0 => counterclockwise

	tests = [ ['WE ARE DISCOVERED. FLEE AT ONCE', 3, 9, 1, 'CEXXECNOTAEOWEAREDISLFDEREV'.lower()],
				['For lunch let\'s have peanut-butter and bologna sandwiches', 12, 4, 1, 'LHSENURBGAISEHCNNOATUPHLUFORCTVABEDOSWDALNTTEAEN'.lower()],
				['I\'ve even witnessed a grown man satisfy a camel', 5, 9, 1, 'IGAMXXXXXXXLETRTIVEEVENWASACAYFSIONESSEDNAMNW'.lower()],
 				['why is this professor so boring omg', 5, 6, 0, 'TSIYHWHFSNGOMGXIRORPSIEOBOROSS'.lower()],
				['Solving challenges on r/dailyprogrammer is so much fun!!', 6, 8, 0, 'CGNIVLOSHSYMUCHFUNXXMMLEGNELLAOPERISSOAIADRNROGR'.lower()],
				['Why does it say paper jam when there is no paper jam?', 14, 3, 0, 'YHWDSSPEAHTRSPEAMXJPOIENWJPYTEOIAARMEHENAR'.lower()]]

	for test in tests:

		# remove punctuation and covert to lowercase
		pretty_info = stripData(test[0])

		# add extra characters to fill in message
		fill = (test[1] * test[2]) - len(pretty_info)	
		for i in range(fill):
			pretty_info = pretty_info + 'x'

		# get matrix representation
		grid = stringToMatrix(pretty_info, test[1], test[2])
		print(grid)
		print()

		# encrypt message
		message = encrypt(grid, test[3])
		message = listToString(message)

		print(message)
		print(test[4])
		print()

	return


if __name__ == '__main__':
	main()
