'''
[2019-08-05] Challenge #380 [Easy] Smooshed Morse Code 1

For the purpose of this challenge, Morse code represents every letter as a sequence of 1-4 characters, each of which is either . (dot) or - (dash). The code for the letter a is .-, for b is -..., etc. The codes for each letter a through z are:

.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..

Normally, you would indicate where one letter ends and the next begins, for instance with a space between the letters' codes, but for this challenge, just smoosh all the coded letters together into a single string consisting of only dashes and dots.
Examples

smorse("sos") => "...---..."
smorse("daily") => "-...-...-..-.--"
smorse("programmer") => ".--..-.-----..-..-----..-."
smorse("bits") => "-.....-..."
smorse("three") => "-.....-..."

An obvious problem with this system is that decoding is ambiguous. For instance, both bits and three encode to the same string, so you can't tell which one you would decode to without more information.
Optional bonus challenges

For these challenges, use the enable1 word list. It contains 172,823 words. If you encode them all, you would get a total of 2,499,157 dots and 1,565,081 dashes.

    The sequence -...-....-.--. is the code for four different words (needing, nervate, niding, tiling). Find the only sequence that's the code for 13 different words.

    autotomous encodes to .-..--------------..-..., which has 14 dashes in a row. Find the only word that has 15 dashes in a row.

    Call a word perfectly balanced if its code has the same number of dots as dashes. counterdemonstrations is one of two 21-letter words that's perfectly balanced. Find the other one.

    protectorate is 12 letters long and encodes to .--..-.----.-.-.----.-..--., which is a palindrome (i.e. the string is the same when reversed). Find the only 13-letter word that encodes to a palindrome.

    --.---.---.-- is one of five 13-character sequences that does not appear in the encoding of any word. Find the other four.
'''


import collections
import math
import itertools

code = {'a': '.-', 
         'b': '-...', 
         'c': '-.-.', 
         'd': '-..', 
         'e': '.', 
         'f': '..-.',
         'g': '--.',
         'h': '....',
         'i': '..',
         'j': '.---',
         'k': '-.-',
         'l': '.-..',
         'm': '--',
         'n': '-.',
         'o': '---',
         'p': '.--.',
         'q': '--.-',
         'r': '.-.',
         's': '...',
         't': '-', 
         'u': '..-', 
         'v': '...-',
         'w': '.--',
         'x': '-..-',
         'y': '-.--',
         'z': '--..'}

def smorse(word):
   morse = ''

   for letter in word:
      morse += code[letter]

   return morse

def max_word(words):
   c = collections.Counter()

   for word in words.values():
      c[word] += 1
      if c[word] == 13:
         return word

   return ''

def encode():
   words = {}

   with open('morse_dict.txt', 'r') as f:
      for line in f:
         line = line.rstrip()
         coded = smorse(line)
         words[line] = coded

   return words
         
def dashes(words):
   count = 0

   for key, word in words.items():
      if len(word) > 14:
         for i in range(len(word)):
            if word[i] == '-':
               count += 1

            if count == 15:
               print(word)
               return key
            
            if word[i] == '.':
               count = 0

   return ''

def perfectly_balanced(words):
   dots = 0
   dashes = 0

   for key, val in words.items():
      if len(key) == 21 and key != 'counterdemonstrations':
         for sym in val:
            if sym == '.':
               dots += 1
            elif sym == '-':
               dashes += 1

         if dots == dashes:
            return key
         else:
            dots = 0
            dashes = 0

   return ''

def palindrome(words):
   for key, val in words.items():
      if len(key) == 13:
         if val == val[::-1]:
            return key

   return ''

def sequences(words):
   seq = []

   combs = set(itertools.combinations('.-'*13, 13))

   for c in combs:
      s = ''.join(c)
      seq.append(s)
      for val in words.values():
         if s in val:
            seq.remove(s)
            break
   
   return seq

def lookup(letter):
   for key, val in code.items():
      if letter == val:
         return key
   return ''

# needs to be recursive
def smalpha(permutation):
   letter = permutation[:2]
   

   return ''   

def main():
   # test = ['sos', 'daily', 'programmer', 'bits', 'three']
   # for word in test:
   #    val = smorse(word)
   #    print(word + ' = ' + val)

   # words = encode()

   # print(max_word(words))
   # print(dashes(words))
   # print(perfectly_balanced(words))
   # print(palindrome(words))
   # print(sequences(words))

   print(smalpha('.--...-.-.-.....-.--........----.-.-..---.---.--.--.-.-....-..-...-.---..--.----..'))

   return


if __name__ == '__main__':
   main()
