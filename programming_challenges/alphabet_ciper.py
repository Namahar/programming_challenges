'''
Description

"The Alphabet Cipher", published by Lewis Carroll in 1868, describes a Vigenère cipher (thanks /u/Yadkee for the clarification) for passing secret messages. The cipher involves alphabet substitution using a shared keyword. Using the alphabet cipher to tranmit messages follows this procedure:

You must make a substitution chart like this, where each row of the alphabet is rotated by one as each letter goes down the chart. All test cases will utilize this same substitution chart.

  ABCDEFGHIJKLMNOPQRSTUVWXYZ
A abcdefghijklmnopqrstuvwxyz
B bcdefghijklmnopqrstuvwxyza
C cdefghijklmnopqrstuvwxyzab
D defghijklmnopqrstuvwxyzabc
E efghijklmnopqrstuvwxyzabcd
F fghijklmnopqrstuvwxyzabcde
G ghijklmnopqrstuvwxyzabcdef
H hijklmnopqrstuvwxyzabcdefg
I ijklmnopqrstuvwxyzabcdefgh
J jklmnopqrstuvwxyzabcdefghi
K klmnopqrstuvwxyzabcdefghij
L lmnopqrstuvwxyzabcdefghijk
M mnopqrstuvwxyzabcdefghijkl
N nopqrstuvwxyzabcdefghijklm
O opqrstuvwxyzabcdefghijklmn
P pqrstuvwxyzabcdefghijklmno
Q qrstuvwxyzabcdefghijklmnop
R rstuvwxyzabcdefghijklmnopq
S stuvwxyzabcdefghijklmnopqr
T tuvwxyzabcdefghijklmnopqrs
U uvwxyzabcdefghijklmnopqrst
V vwxyzabcdefghijklmnopqrstu
W wxyzabcdefghijklmnopqrstuv
X xyzabcdefghijklmnopqrstuvw
Y yzabcdefghijklmnopqrstuvwx
Z zabcdefghijklmnopqrstuvwxy

Both people exchanging messages must agree on the secret keyword. To be effective, this keyword should not be written down anywhere, but memorized.

To encode the message, first write it down.

thepackagehasbeendelivered

Then, write the keyword, (for example, snitch), repeated as many times as necessary.

snitchsnitchsnitchsnitchsn
thepackagehasbeendelivered

Now you can look up the column S in the table and follow it down until it meets the T row. The value at the intersection is the letter L. All the letters would be thus encoded.

snitchsnitchsnitchsnitchsn
thepackagehasbeendelivered
lumicjcnoxjhkomxpkwyqogywq

The encoded message is now lumicjcnoxjhkomxpkwyqogywq

To decode, the other person would use the secret keyword and the table to look up the letters in reverse.
Input Description

Each input will consist of two strings, separate by a space. The first word will be the secret word, and the second will be the message to encrypt.

snitch thepackagehasbeendelivered

Output Description

Your program should print out the encrypted message.

lumicjcnoxjhkomxpkwyqogywq

Challenge Inputs

bond theredfoxtrotsquietlyatmidnight
train murderontheorientexpress
garden themolessnuckintothegardenlastnight

Challenge Outputs

uvrufrsryherugdxjsgozogpjralhvg
flrlrkfnbuxfrqrgkefckvsa
zhvpsyksjqypqiewsgnexdvqkncdwgtixkx

Bonus

For a bonus, also implement the decryption portion of the algorithm and try to decrypt the following messages.
Bonus Inputs

cloak klatrgafedvtssdwywcyty
python pjphmfamhrcaifxifvvfmzwqtmyswst
moore rcfpsgfspiecbcc

Bonus Outputs

iamtheprettiestunicorn
alwayslookonthebrightsideoflife
foryoureyesonly

'''

import sys

# get command line inputs
master_key = ""
key = sys.argv[1]
message = sys.argv[2]
funct = sys.argv[3]

# repeat keyword
def full_key(master_key, message, key):
	j = 0
	for i in range(0, len(message)):
		master_key += key[j]
		j += 1
		if (j == len(key)):
			j = 0
			
	return master_key

def encryption(string):
	for i in range(0, len(master_key)):
		code_1 = ord(master_key[i]) - 96
		code_2 = ord(message[i]) - 96
		final_code = code_1 + code_2 - 1
		
		if (final_code > 26):
			final_code -= 26
		final_code += 96
		
		string += chr(final_code)
	
	return string
	
def decryption(encrypted, key):
	string = ""
	for i in range(0, len(encrypted)):
		code_1 = ord(encrypted[i]) - 96
		code_2 = ord(key[i]) - 96
		final_code = code_1 - code_2 + 1
		if (final_code < 1):
			final_code += 26
		
		string += chr(final_code + 96)
		
	return string
	
# get master key
master_key = full_key(master_key, message, key)
print(master_key)
print(message)

if (int(funct) == 1):
	encryption = encryption("")
	print(encryption)

elif (int(funct) == 2):
	decryption = decryption(message, master_key)
	print(decryption)