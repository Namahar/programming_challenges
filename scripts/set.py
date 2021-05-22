''' find difference between two arrays '''

def find_missing(full_set, partial_set):
   missing = set(full_set) - set(partial_set)
   return missing

def op(full, partial):
   xor_sum = 0
   for num in full:
      xor_sum ^= num
   for num in partial:
      xor_sum ^= num
   print(xor_sum)
   
def main():
   full = [4, 12, 9, 5, 6]
   partial = [4, 9, 12, 6]
   print(find_missing(full, partial))
   op(full, partial)

if __name__ == '__main__':
   main()