# leetcode 9

from random import randint

MAX_INT = 2 ** 31 - 1
MIN_INT = -2 ** 31

class ListNode:
   def __init__(self, val = 0, next = None):
      self.val = val
      self.next = next

class TreeNode:
   def __init__(self, val = 0, left = None, right = None):
      self.val = val
      self.left = left
      self.right = right

class Solution:

   # leetcode 1
   def bruteForce(self, nums, target):
      length = len(nums)

      for i in range(length):
         sol = target - nums[i]

         for j in range(length):
            if nums[j] == sol:
               return [i, j]

      return []

   def fastSearch(self, nums, target):
      complements = dict()

      for i in range(len(nums)):
         comp = target - nums[i]

         if comp not in complements:
            complements[nums[i]] = i
         else:
            return [complements[comp], i]

      return [] 

   # leetcode 6
   def reverse_integer(self, val):
      reverse_num = 0

      while val:
         if reverse_num > MAX_INT / 10 or (reverse_num == MAX_INT / 10 and val % 10 > 7):
            return 0
         elif reverse_num < MIN_INT / 10 or (reverse_num == MIN_INT / 10 and val % 10 < -8):
            return 0

         reverse_num = reverse_num*10 + val % 10
         val = int(val / 10)

      return reverse_num

   # leetcode 9
   def palindrome_number(self, x):
      
      # if number is less than 0, has a negative sign
      # cannot be a palindrome
      if x < 0:
         return False

      reverse = 0
      while x > reverse:
         reverse = reverse * 10 + x % 10
         x = int(x / 10)

      return x == reverse or x == int(reverse / 10)

   # leetcode 13
   def roman_to_integer(self, s):
      roman = {
         'I': 1,
         'V': 5,
         'X': 10,
         'L': 50,
         'C': 100,
         'D': 500,
         'M': 1000
      }

      if len(s) == 0:
         return 0

      x = 0
      for i in range(len(s) - 1):
         if roman[s[i]] < roman[s[i+1]]:
            x -= roman[s[i]]
         else:
            x += roman[s[i]]
      x += roman[s[len(s) - 1]]

      return x

   # leetcode 14
   def common_prefix(self, strings):
      
      min_length = MAX_INT
      prefix = ''
      index = 0

      # gets shortest word
      for i in range(len(strings)):
         s = strings[i]

         if len(s) < min_length:
            index = i
            min_length = len(s)

      p = strings[index]

      for i in range(len(strings)):
         if i == index:
            continue

         s = strings[i]

         for j in range(len(p)):
            if p[j] == s[j]:
               prefix += s[j]

         if len(prefix) <= len(p):
            p = prefix[:]
            prefix = ''

      prefix = p[:]

      return prefix

   # leetcode 20
   def valid_parentheses(self, s):

      stack = list()
      matches = {
         '}': '{',
         ']': '[',
         ')': '('
      }

      for char in s:
         if char in matches:
            
            if stack:
               top = stack.pop()
            else:
               top = '!'

            if matches[char] != top:
               return False
         else:
            stack.append(char)

      return stack == list()

   # leetcode 21
   def print_list(self, l):
      while l.next != None:
         print(l.val, end = '')
         
         if l.next.next != None:
            print('->', end = '')
         l = l.next

      print()

   def merge_lists(self, l1, l2):
      l3 = ListNode()
      temp = l3

      while l1.next != None and l2.next != None:
         if l1.val <= l2.val:
            temp.next = l1
            l1 = l1.next
         
         else:
            temp.next = l2
            l2 = l2.next
         
         temp = temp.next

      if l1.next == None:
         temp.next = l2

      if l2.next == None:
         temp.next = l1
            
      return l3.next

   # leetcode 83
   def delete_duplicates(self, head):
      temp = head
      prev = head

      val = -2 ** 31
      while temp.next != None:
         n = temp.val

         if n != val:
            val = n
            prev = temp

         else:
            prev.next = temp.next

         temp = temp.next

      return head

   # leetcode 26
   def remove_duplicate(self, nums):

      if len(nums) == 0:
         return 0

      i = 0
      for j in range(1, len(nums)):
         if nums[i] != nums[j]:
            i += 1
            nums[i] = nums[j]

      return i + 1

   # leetcode 27
   def remove_element(self, nums, val):
      if len(nums) == 0:
         return 0

      i = 0
      for j in range(0, len(nums)):
         if nums[j] != val:
            nums[i] = nums[j]
            i += 1

      return i

   # leetcode 28
   def strings(self, haystack, needle):
      if len(needle) == 0:
         return 0

      size = len(needle)
      for i in range(len(haystack) - size):

         if haystack[i:i+size] == needle:
            return i

      return -1

   # leetcode 35
   def search_insert(self, nums, target):
      if len(nums) == 0:
         return 0
      
      for i in range(len(nums)):
         val = nums[i]

         if val >= target:
            return i

      return i + 1

   # leetcode 38
   def count_say(self, n):

      string = '1'
      count = 0
      char = string[0]

      for i in range(2, n+1):

         temp = ''

         for j in range(len(string)):
            c = string[j]

            if c == char:
               count += 1

            if c != char:
               temp = temp + str(count) + char
               count = 1
               char = c

         temp = temp + str(count) + char
         count = 0
         string = temp[:]
         char = temp[0]

      return string

   # leetcode 53
   def max_sub_array(self, nums):
      end = len(nums)
      length = end
      total = 0

      while end > 0:
         start = 0

         while start <= length and end <= length:

            sub = nums[start : start + end]
            
            add = 0
            for val in sub:
               add += val

            if add > total:
               total = add

            start += 1
         
         end -= 1

      return total

   def proper_max_sub_array(self, nums):
      for i in range(1, len(nums)):
         if nums[i-1] > 0:
            nums[i] += nums[i-1]
      return max(nums)

   # leetcode 58
   def length_last_word(self, s):
      if len(s) == 0:
         return 0

      if ' ' not in s:
         return len(s)

      space_index = len(s) - s[::-1].index(' ')

      # i = len(s) - 1
      # count = 0
      # while s[i] != ' ':
      #    count += 1
      #    i -= 1
      # print(count)
      
      return len(s) - space_index

   # leetcode 66
   def plus_one(self, digits):
      if digits[-1] < 9:
         digits[-1] += 1

      else:

         val = digits[-1]
         i = len(digits) - 1
         while val == 9 and i >= 0:
            digits[i] = 0
            
            if i == 0:
               digits.insert(0, 1)

            else:
               val = digits[i]

            i -= 1

         if i > 0:
            digits[i] += 1

      return digits

   # leetcode 67
   def add_binary(self, a, b):
      

      a = list(a)
      b = list(b)
      c = ''
      carry = 0

      while a or b or carry:
         if a:
            carry += int(a.pop())
         if b:
            carry += int(b.pop())

         c += str(carry % 2)     
         
         carry //= 2

      
      return c[::-1] 

   # leetcode 69
   def mysqrt(self, x):
      left = 1
      right = x

      while left <= right:
         middle = (left + right) // 2

         if middle * middle <= x and (middle+1) * (middle + 1) > x:
            return middle

         elif x < middle * middle:
            right = middle
         
         else:
            left = middle

      return middle

   # leetcode 70
   def climb_stairs(self, n):
      sol = [1] * (n + 1)

      for i in range(2, n+1):
         sol[i] = sol[i-1] + sol[i-2]

      return sol[n]

   # leetcode 88
   def merge(self, nums1, m, nums2, n):
      # len(nums1) = m + n
      i = 0
      j = 0

      while i < m:
         if nums1[i] > nums2[j]:
            temp = nums1[i]
            nums1[i] = nums2[j]
            nums2[j] = temp

         i += 1

      nums1[i:m+n] = nums2[:]

      return

   def alt_merge(self, nums1, m, nums2, n):
      
      while m >= 0 and n >= 0:
         if nums1[m-1] >= nums2[n-1]:
            nums1[m+n - 1] = nums1[m-1]
            m -= 1
         else:
            nums1[m+n - 1] = nums2[n-1]
            n -= 1

      if n > 0:
         nums1[:n] = nums2[:n]

      return

   # leetcode 100
   def is_same_tree(self, p, q):

      if p == None and q == None:
         return True

      if p == None or q == None:
         return False

      if p.val != q.val:
         return False

      return self.is_same_tree(p.left, q.left) and self.is_same_tree(p.right, q.right)

   # leetcode 101
   def is_symmetric(self, root):
      if root.left == None and root.right == None:
         return True
      
      if root.left == None or root.right == None:
         return False

      
      return self.is_symmetric(root.left) and self.is_symmetric(root.right)

   # leetcode 104
   


def main():
   val = randint(MIN_INT, MAX_INT + 1)

   ans = Solution()

   # leetcode 1
   # nums = [2, 7, 11, 15]
   # target = 9
   # print(ans.bruteForce(nums, target))
   # print(ans.fastSearch(nums, target)) 

   # leetcode 6
   # print(val, ans.reverse_integer(val))
   
   # leetcode 9
   # print(val, ans.palindrome_number(val))

   # leetcode 13
   # test = ['III', 'IV', 'IX', 'LVIII', 'MCMXCIV']
   # for t in test:
   #    print(t, ans.roman_to_integer(t))

   # leetcode 14
   # vocab1 = ['flower', 'flow', 'flight']
   # vocab2 = ['dog', 'racecar', 'car']
   # print(vocab1, ans.common_prefix(vocab1))
   # print(vocab2, ans.common_prefix(vocab2))

   # leetcode 20
   # strings = [ '()', '()[]{}', '(]', '([)]', '{[]}']
   # for s in strings:
   #    print(s, ans.valid_parentheses(s))

   # leetcode 21
   # l1 = ListNode()
   # l2 = ListNode()
   # num1 = [1, 2, 4]
   # num2 = [1, 3, 4]

   # temp = l1
   # for n in num1:
   #    temp.val = n
   #    temp.next = ListNode()
   #    temp = temp.next

   # temp = l2
   # for n in num2:
   #    temp.val = n
   #    temp.next = ListNode()
   #    temp = temp.next

   # ans.print_list(l1)
   # ans.print_list(l2)
   # ans.print_list(ans.merge_lists(l1, l2))

   # leetcode 26
   # numbers = [[1, 1, 2], [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]]
   # for n in numbers:
   #    print(n, ans.remove_duplicate(n))
   
   # leetcode 27
   # nums = {3: [3, 2, 2, 3], 2: [0, 1, 2, 2, 3, 0, 4, 2]}
   # for key, val in nums.items():
   #    print(key, val, ans.remove_element(val, key))

   # leetcode 28
   # strings = {'hello': 'll', 'aaaaa': 'bba'}
   # for key, val in strings.items():
   #    print(key, val, ans.strings(key, val))

   # leetcode 35
   # nums = [1, 3, 5, 6]
   # targets = [5, 2, 7, 0]
   # for t in targets:
   #    print(nums, t, ans.search_insert(nums, t))

   # leetcode 38
   # for i in range(1, 11):
   #    print(i, ans.count_say(i))

   # nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
   # for i in range(1001):
   #    nums.append(randint(MIN_INT, MAX_INT))
   # print(nums, ans.max_sub_array(nums))
   # print(nums, ans.proper_max_sub_array(nums))

   # leetcode 58
   # s = 'Hello World'
   # print(s, ans.length_last_word(s))

   # leetcode 66
   # digits = [[1, 2, 3], [4, 3, 2, 1], [9], [1, 2, 9]]
   # for d in digits:
   #    print(d, end = ' ')
   #    print(ans.plus_one(d))

   # leetcode 67
   # tests = [['11', '1'], ['1010', '1011']]
   # for t in tests:
   #    print(t, ans.add_binary(t[0], t[1]))

   # leetcode 69
   # x = 64
   # print(x, ans.mysqrt(x))
   
   # leetcode 70
   # for i in range(5):
   #    print(i, ans.climb_stairs(i))
   
   # leetcode 83
   # lists = [[1, 1, 2], [1, 1, 2, 3, 3]]

   # for l in lists:
   #    head = ListNode()
   #    temp = head
   #    for num in l:
   #       temp.val = num
   #       temp.next = ListNode()
   #       temp = temp.next

   #    ans.print_list(head)
   #    ans.print_list(ans.delete_duplicates(head))

   # leetcode 88
   # nums1 = [1, 2, 3, 0, 0, 0]
   # nums2 = [0, 5, 6]
   # m = 3
   # n = 3
   # print(nums1, nums2)
   # # ans.merge(nums1, m, nums2, n)
   # ans.alt_merge(nums1, m, nums2, n)
   # print(nums1, nums2)

   # leetcode 100
   # a = [1, 2, 3]
   # b = [1, 2, 3]
   
   # a = [1 , 2, None]
   # b = [1, None, 2]

   # a = [1, 2, 1]
   # b = [1, 2, 2]

   # p = TreeNode()
   # q = TreeNode()

   # p.val = a[0]
   # p.left = TreeNode()
   # p.left.val = a[1]
   # p.right = TreeNode()
   # p.right.val = a[2]

   # q.val = b[0]
   # q.left = TreeNode()
   # q.left.val = b[1]
   # q.right = TreeNode()
   # q.right.val = b[2]
   
   # print(ans.is_same_tree(p, q))
   
   # leetcode 101
   nums = [1, 2, 2, 3, 4, 4, 3]
   root = TreeNode()
   root.val = 1
   root.left = TreeNode()
   root.right = TreeNode()
   
   root.left.val = 2
   root.left.left = TreeNode()
   root.left.right = TreeNode()

   root.left.left.val = 3
   root.left.right.val = 4

   root.right.val = 2
   root.right.left = TreeNode()
   root.right.right = TreeNode()

   root.right.right.val = 3
   root.right.left.val = 4

   print(ans.is_symmetric(root))

   return

if __name__ == "__main__":
   main()