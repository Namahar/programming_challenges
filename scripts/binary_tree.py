class TreeNode():
   def __init__(self, val, left = None, right = None):
      self.val = val
      self.left = left
      self.right = right
      return

class ListNode():
   def __init__(self, val = 0, next = None):
      self.val = val
      self.next = next
      return

def print_tree(root):
   if root == None:
      return

   q = list()
   q.append(root)

   while len(q):
      temp = q[0]
      q.pop(0)

      print(temp.val, end = ' ')

      if temp.left:
         q.append(temp.left)

      if temp.right:
         q.append(temp.right)

   print()

   return

def insert_node(root, val):

   queue = list()
   queue.append(root)

   while len(queue):
      temp = queue[0]
      queue.pop(0)

      if temp.val !=  None:

         if temp.left == None:
            temp.left = TreeNode(val)
            break

         else:
            queue.append(temp.left)

         if temp.right == None:
            temp.right = TreeNode(val)
            break
         else:
            queue.append(temp.right)

   return

def is_symmetric(root):
   if root.left == None and root.right == None:
      return True

   else:
      return mirror(root.left, root.right)

def mirror(l, r):
   if l == None and r == None:
      return True

   if l == None or r == None:
      return False

   if l.val == r.val:
      
      return mirror(l.left, r.right) and mirror(l.right, r.left)
   else:
      return False

def test_is_symmetric():
   nums = [[1, 2, 2, 3, 4, 4, 3], [1, 2, 2, None, 3, None, 3]]
   
   for n in nums:
      root = TreeNode(n[0])


      for i in range(1, len(n)):
         insert_node(root, n[i])

      print(n)
      print_tree(root)
      print(is_symmetric(root))

   return

def is_same_tree(p, q):
   if p == None and q == None:
      return True

   if p == None or q == None:
      return False

   if p.val != q.val:
      return False

   return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

def test_same_tree():
   pq = [ [[1, 2, 3], [1, 2, 3]], [[1, 2], [1, None, 2]], [[1, 2, 1], [1, 1, 2]] ]
   for duo in pq:
      p = TreeNode(duo[0][0])
      q = TreeNode(duo[1][0])

      for i in range(1, len(duo[0])):
         insert_node(p, duo[0][i])

      for i in range(1, len(duo[1])):
         insert_node(q, duo[1][i])

      print_tree(p)
      print_tree(q)
      print(is_same_tree(p, q))

   return

def max_depth(root):
   h = 0
   q = list()
   q.append(root)

   while len(q):
      h += 1
      temp = list()

      for node in q:
         if node.left:
            temp.append(node.left)

         if node.right:
            temp.append(node.right)

      q = temp

   return h

def max_depth_recursive(root):
   if root == None:
      return 0

   return 1 + max(max_depth(root.left), max_depth(root.right))

def test_max_depth():
   nums = [3, 9, 20, None, None, 15, 7]
   root = TreeNode(nums[0])

   for i in range(1, len(nums)):
      insert_node(root, nums[i])

   print_tree(root)
   print(max_depth(root))

   return

def level_order_bottom(root):
   if root == None:
      return []
   
   q = list()
   q.append(root)
   values = list()

   while q:
      temp = []
      level = []

      for node in q:
         # if node.val != None:
         level.append(node.val)

         if node.left:
            temp.append(node.left)

         if node.right:
            temp.append(node.right)

      q = temp
      values.append(level)

   return values

def test_level_order_bottom():
   nums = [3, 9, 20, None, None, 15, 7]
   root = TreeNode(nums[0])

   for i in range(1, len(nums)):
      insert_node(root, nums[i])

   print_tree(root)
   nodes = level_order_bottom(root)
   print(nodes)

   return

def bst_insert(root, val):
   if not root:
      return TreeNode(val)

   elif val < root.val:
      root.left = bst_insert(root.left, val)
   
   elif val >= root.val:
      root.right = bst_insert(root.right, val)

   return root

def construct_tree_from_array(nums, low, high):
   if low > high:
      return None

   mid = low + (high - low) // 2
   root = TreeNode(nums[mid])
   root.left = construct_tree_from_array(nums, low, mid - 1)
   root.right = construct_tree_from_array(nums, mid + 1, high)

   return root

def sorted_array_to_bst(nums):
   if len(nums) == 0:
      return None

   return construct_tree_from_array(nums, 0, len(nums) - 1)

def test_array_to_bst():
   nums = [-10, -3, 0, 5, 9]
   nums = [-10, -5, -3, 0, 5, 8, 9]
   print(nums)

   root = sorted_array_to_bst(nums)
   
   # print_tree(root)
   print(level_order_bottom(root))
   return

def print_list(head):
   if head.next == None:
      print()
      return

   print(head.val, end = ' ')
   print_list(head.next)

def insert_list(head, val):
   if head.next == None:
      head.val = val
      head.next = ListNode()
      return

   insert_list(head.next, val)

def get_length_list(head):
   if head.next == None:
      return 0

   return 1 + get_length_list(head.next)

def sorted_list_to_bst(head):
   if not head:
      return None

   length = get_length_list(head)

   def construct_tree_from_list(low, high):
      nonlocal head
      
      if low > high:
         return None

      mid = low + (high - low) // 2

      left = construct_tree_from_list(low, mid - 1)
      node = TreeNode(head.val)
      node.left = left
      head = head.next

      node.right = construct_tree_from_list(mid + 1, high)

      return node
   
   return construct_tree_from_list(0, length - 1)

def is_balanced(root):
   left = max_depth_recursive(root.left)
   right = max_depth_recursive(root.right)

   print(left, right)

   if left == right:
      return True

   return False
   
def test_is_balanced():
   nums = [[3, 9, 20, None, None, 15, 7], [1, 2, 2, 3, 3, None, None, 4, 4]]

   for n in nums:

      root = TreeNode(n[0])

      for i in range(1, len(n)):
         insert_node(root, n[i])

      print(level_order_bottom(root))
      print(is_balanced(root))

   return

def test_list_to_bst():
   nums = [-10, -3, 0, 5, 9]
   print(nums)

   head = ListNode()

   for i in range(len(nums)):
      insert_list(head, nums[i])

   root = sorted_list_to_bst(head)

   # print_list(head)
   print(level_order_bottom(root))
   return

def min_depth(root):

   if not root or root.val == None:
      return 0

   # if root.left == None or root.right == None:
   #    return max(min_depth(root.left), min_depth(root.right)) + 1

   # else:
   #    return min(min_depth(root.left), min_depth(root.right)) + 1
   
   left = 1 + min_depth(root.left)
   right = 1 + min_depth(root.right)

   return min(left, right)

def test_min_depth():
   nums = [3, 9, 20, None, None, 15, 7]

   root = TreeNode(nums[0])
   for i in range(1, len(nums)):
      insert_node(root, nums[i])

   print(level_order_bottom(root))
   print(min_depth(root))

   return

# pre order traversal
def get_paths(root, total, paths, travel):
   if root == None:
      return 

   travel.append(root.val)

   if root.val != None:
      total -= root.val

   if root.left == None and root.right == None:
      if total == 0:
         paths.append(travel[:])

   else:
      get_paths(root.left, total, paths, travel)
      get_paths(root.right, total, paths, travel)

   travel.pop()

def all_path_sum(root, total):
   
   if root == None:
      return []

   paths = []
   get_paths(root, total, paths, [])
   
   return paths


def path_sum(root, total):
   if root == None or root.val == None or total < 0:
      return False

   total -= root.val

   if total == 0 and root.left == None and root.right == None:
      return True

   return path_sum(root.left, total) or path_sum(root.right, total)

def test_path_sum():
   nums = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
   total = 22

   if nums:
      root = TreeNode(nums[0])
   else:
      return 

   for i in range(1, len(nums)):
      insert_node(root, nums[i])

   print(level_order_bottom(root))
   print(path_sum(root, total))
   paths = all_path_sum(root, total)
   print(paths)

   return

def flatten(root):
   if root is None:
      return

   if root.left:

      flatten(root.left)
      
      if root.left.val != None:
         temp = root.right
         root.right = root.left
         root.left = None
      else:
         root.left = None
         temp = None

      traverse = root.right
      while traverse.right != None:
         traverse = traverse.right
      
      traverse.right = temp

   flatten(root.right)
   
   return

def test_flatten():
   nums = [1, 2, 5, 3, 4, None, 6]
   root = TreeNode(nums[0])

   for i in range(1, len(nums)):
      insert_node(root, nums[i])

   print(level_order_bottom(root))
   flatten(root)
   print(level_order_bottom(root))

   while root != None:
      print(root.val)
      root = root.right


def main():

   # test_same_tree()
   # test_is_symmetric()
   # test_max_depth()
   # test_level_order_bottom()
   # test_array_to_bst()
   # test_list_to_bst()
   # test_is_balanced()
   # test_min_depth()
   # test_path_sum()
   test_flatten()
   
   return

if __name__ == '__main__':
   main()