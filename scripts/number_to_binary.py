from random import randint
from math import floor

def binary(value, ans):

   if value == 0:
      return '0'

   if value < 1:
      return ans

   ans += str(value % 2)
   value = floor(value / 2)

   ans = binary(value, ans)
   return ans

def main():  
   value = randint(0, 101)
   answer = ''

   answer = binary(value, answer)
   answer = answer[::-1]

   print(value, answer)
   return

if __name__ == '__main__':
   main() 