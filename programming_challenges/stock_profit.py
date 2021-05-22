def brute_max_profit(prices):

   profit = 0

   for i in range(len(prices) - 1):

      for j in range(i + 1, len(prices)):
         if prices[j] - prices[i] > profit:
            profit = prices[j] - prices[i]
         
   return profit

def max_profit(prices):

   profit = 0
   min_price = 2**31

   for i in range(len(prices)):
      if prices[i] < min_price:
         min_price = prices[i]

      elif prices[i] - min_price > profit:
         profit = prices[i] - min_price

   return profit

def multiple_max_profit(prices):
   profit = 0

   for i in range(1, len(prices)):
      if prices[i] > prices[i - 1]:
         profit += prices[i] - prices[i-1]

   return profit


def main():
   # prices = [7, 1, 5, 3, 6, 4]
   # prices = [1, 2, 3, 4, 5]
   prices = [7, 6, 4, 3, 1]
   day = max_profit(prices)
   print(prices, day)

   all_days = multiple_max_profit(prices)
   print(all_days)

   return

if __name__ == '__main__':
   main()