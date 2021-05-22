'''
Description

This challenge is about a simple card flipping solitaire game. You're presented with a sequence of cards, some face up, some face down. You can remove any face up card, but you must then flip the adjacent cards (if any). The goal is to successfully remove every card. Making the wrong move can get you stuck.

In this challenge, a 1 signifies a face up card and a 0 signifies a face down card. We will also use zero-based indexing, starting from the left, to indicate specific cards. So, to illustrate a game, consider this starting card set.

0100110

I can choose to remove cards 1, 4, or 5 since these are face up. If I remove card 1, the game looks like this (using . to signify an empty spot):

1.10110

I had to flip cards 0 and 2 since they were adjacent. Next I could choose to remove cards 0, 2, 4, or 5. I choose card 0:

..10110

Since it has no adjacent cards, there were no cards to flip. I can win this game by continuing with: 2, 3, 5, 4, 6.

Supposed instead I started with card 4:

0101.00

This is unsolvable since there's an "island" of zeros, and cards in such islands can never be flipped face up.
Input Description

As input you will be given a sequence of 0 and 1, no spaces.
Output Description

Your program must print a sequence of moves that leads to a win. If there is no solution, it must print "no solution". In general, if there's one solution then there are many possible solutions.

Optional output format: Illustrate the solution step by step.
Sample Inputs

0100110
01001100111
100001100101000

Sample Outputs

1 0 2 3 5 4 6
no solution
0 1 2 3 4 6 5 7 8 11 10 9 12 13 14

Challenge Inputs

0100110
001011011101001001000
1010010101001011011001011101111
1101110110000001010111011100110

Bonus Input

010111111111100100101000100110111000101111001001011011000011000

'''

from random import randint

def endGame(cards):
   count = 0

   # how many cards are removed
   for card in cards:
      if card == '.':
         count += 1

   # if removed cards equals number of cards
   # game over
   if count == len(cards):
      return 1
   else:
      return 0

def flip_help(cards, index):
   if cards[index] == 0:
      cards[index] = 1

   elif cards[index] == 1:
      cards[index] = 0

   return

def flip(cards, index, length):
   cards[index] = '.'

   if index > 0:
      flip_help(cards, index-1)

   if index < length-1:
      flip_help(cards, index+1)

   return

def checkStatus(cards):
   count = 0

   for card in cards:
      if card == 1:
         count += 1   

   if count == 0:
      return 1
   else:
      return 0

def getRoute(cards, length):
   count = []

   for i in range(length):
      if cards[i] == 1:
         count.append(i)

   return count


def cardFlip(cards, copy):
   indices = getRoute(cards, len(cards))
   for index in indices:
      flip(cards, index, len(cards))
      print(index)
      print(cards)

      if (endGame(cards)):
         print('Found Solution')
         return 1

      end = cardFlip(cards, copy)

      if end:
         return

      if (checkStatus):
         return
   
   print("No Solution")
   return

def main():
   hand1 = [0, 1, 0, 0, 1, 1, 0]
   hand2 = [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]
   hand3 = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0]
   hand4 = [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

   #cardFlip(hand1, hand1)
   #cardFlip(hand2, hand2)
   #cardFlip(hand3, hand3)
   cardFlip(hand4, hand4)

if __name__ == '__main__':
   main()