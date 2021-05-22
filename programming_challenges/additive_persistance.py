'''
Description

Inspired by this tweet, today's challenge is to calculate the additive persistence of a number, defined as how many loops you have to do summing its digits until you get a single digit number. Take an integer N:

    Add its digits

    Repeat until the result has 1 digit

The total number of iterations is the additive persistence of N.

Your challenge today is to implement a function that calculates the additive persistence of a number.
Examples

13 -> 1
1234 -> 2
9876 -> 2
199 -> 3

Bonus

The really easy solution manipulates the input to convert the number to a string and iterate over it. Try it without making the number a strong, decomposing it into digits while keeping it a number.

On some platforms and languages, if you try and find ever larger persistence values you'll quickly learn about your platform's big integer interfaces (e.g. 64 bit numbers).
'''

def additive_persistance(x):
	val = str(x)
	count = 0
	sum = 10
	
	while sum > 9:
		
		sum = 0
		for num in val:
			sum += int(num)
		
		count += 1
		
		val = str(sum)
	
	print("Count = " + str(count))
	return
	
def bonus(x):
	count = 0
	sum = 0
	
	while True:
		sum += x % 10
		x = int(x / 10)
		
		if x == 0:
			count += 1
			
			if sum < 10:
				print("Count = " + str(count))
				return
				
			else:
				x = sum
				sum = 0				
	
	
def main():
	#additive_persistance(13)
	#additive_persistance(1234)
	#additive_persistance(9876)
	#additive_persistance(199)
	
	bonus(13)
	bonus(1234)
	bonus(9876)
	bonus(199)
	bonus(10)
	bonus(999)
	bonus(9007199254740991)
	
if __name__ == "__main__":
	main()