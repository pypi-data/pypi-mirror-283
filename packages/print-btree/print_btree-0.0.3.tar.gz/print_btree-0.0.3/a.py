from src.print_btree import print_btree
from src.print_btree.utils import BTree

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.right.left = Node(6)
root.right.right = Node(7)
root.right.left.right = Node(8)
root.left.left.right = Node(9)
root.right.right.right = Node(7)

# root = BTree.gen_btree(['apple', 'orange', 'pear', 'pineapple','appleorangepear'])

print_btree(root)

# customize val, left, right

# remove Nones
