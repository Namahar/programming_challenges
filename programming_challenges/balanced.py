'''
Given a string containing only the characters x and y, find whether there are the same number of xs and ys.

balanced("xxxyyy") => true
balanced("yyyxxx") => true
balanced("xxxyyyy") => false
balanced("yyxyxxyxxyyyyxxxyxyx") => true
balanced("xyxxxxyyyxyxxyxxyy") => false
balanced("") => true
balanced("x") => false

Optional bonus

Given a string containing only lowercase letters, find whether every letter that appears in the string appears the same number of times. Don't forget to handle the empty string ("") correctly!

balanced_bonus("xxxyyyzzz") => true
balanced_bonus("abccbaabccba") => true
balanced_bonus("xxxyyyzzzz") => false
balanced_bonus("abcdefghijklmnopqrstuvwxyz") => true
balanced_bonus("pqq") => false
balanced_bonus("fdedfdeffeddefeeeefddf") => false
balanced_bonus("www") => true
balanced_bonus("x") => true
balanced_bonus("") => true

Note that balanced_bonus behaves differently than balanced for a few inputs, e.g. "x".
'''

def balanced(string, counter):
	if (len(string) == 0):
		
		if (counter == 0):
			print("True")
		else:
			print("False")
			
		return
		
	#print(ord(string[0]) - 96)
	
	if (string[0] == 'x'):
		counter += 1
	else:
		counter -= 1
		
	string = string.replace(string[0], "", 1)
	
	balanced(string, counter)
	
	counter = 0		
	return
	
def better_balanced(string):
	if (string.count('x') == string.count('y')):
		print("True")
	else:
		print("False")
		
	return

def balanced_bonus(string):
	
	if (len(string) > 0):
		true_count = string.count(string[0])
	
	while (len(string) != 0):
		letter = string[0]
		count = string.count(letter)
		
		if (count != true_count):
			print("False")
			return
		
		string = string.replace(letter, "")
	
	print("True")
	return
	
def better_bonus(string):

	if (string == ""):
		print("True")
		return

	trueCount = string.count(string[0])
	
	for letter in set(string):
		if (string.count(letter) != trueCount):
			print("False")
			return
	
	print("True")
	return
	
def main():
	xy = 0
	
	
	#balanced("xxxyyy", xy)						# true
	#balanced("yyyxxx", xy)						# true
	#balanced("xxxyyyy", xy)						# false
	#balanced("yyxyxxyxxyyyyxxxyxyx", xy) 		# true
	#balanced("xyxxxxyyyxyxxyxxyy", xy) 			# false
	#balanced("", xy) 							# true
	#balanced("x", xy) 							# false
	
	#better_balanced("yyxyxxyxxyyyyxxxyxyx") 		# true
	
	#balanced_bonus("xxxyyyzzz")						# true
	#balanced_bonus("abccbaabccba") 					# true
	#balanced_bonus("xxxyyyzzzz")					# false
	#balanced_bonus("abcdefghijklmnopqrstuvwxyz") 	# true
	#balanced_bonus("pqq")							# false
	#balanced_bonus("fdedfdeffeddefeeeefddf")		# false
	#balanced_bonus("www")							# true
	#balanced_bonus("x")								# true
	#balanced_bonus("")								# true
	
	better_bonus("abccbaabccba")
	balanced_bonus("xxxyyyzzzz")
	
	return
	
if __name__ == "__main__":
    main()