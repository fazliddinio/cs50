"""
Data Structures Implementation
"""
from typing import Any, Optional, List


class Node:
    """Node for linked list."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[Node] = None


class LinkedList:
    """Singly Linked List implementation."""
    
    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self.head is None
    
    def append(self, data: Any) -> None:
        """Add element to end. O(n)"""
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self._size += 1
    
    def prepend(self, data: Any) -> None:
        """Add element to beginning. O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def delete(self, data: Any) -> bool:
        """Delete first occurrence of data. O(n)"""
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, data: Any) -> Optional[Node]:
        """Find node with data. O(n)"""
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None
    
    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def reverse(self) -> None:
        """Reverse the linked list in place. O(n)"""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev


class Stack:
    """Stack implementation using list."""
    
    def __init__(self):
        self._items: List[Any] = []
    
    def __len__(self) -> int:
        return len(self._items)
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def push(self, item: Any) -> None:
        """Add item to top. O(1)"""
        self._items.append(item)
    
    def pop(self) -> Any:
        """Remove and return top item. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self) -> Any:
        """Return top item without removing. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]


class Queue:
    """Queue implementation using list."""
    
    def __init__(self):
        self._items: List[Any] = []
    
    def __len__(self) -> int:
        return len(self._items)
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def enqueue(self, item: Any) -> None:
        """Add item to back. O(1)"""
        self._items.append(item)
    
    def dequeue(self) -> Any:
        """Remove and return front item. O(n)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.pop(0)
    
    def front(self) -> Any:
        """Return front item without removing. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]


class TreeNode:
    """Node for binary tree."""
    def __init__(self, data: Any):
        self.data = data
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinarySearchTree:
    """Binary Search Tree implementation."""
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
    
    def insert(self, data: Any) -> None:
        """Insert a new value. O(log n) average"""
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node: TreeNode, data: Any) -> None:
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)
    
    def search(self, data: Any) -> bool:
        """Search for a value. O(log n) average"""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node: Optional[TreeNode], data: Any) -> bool:
        if node is None:
            return False
        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
    
    def inorder(self) -> List[Any]:
        """Inorder traversal (sorted order)."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)
    
    def preorder(self) -> List[Any]:
        """Preorder traversal."""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder(self) -> List[Any]:
        """Postorder traversal."""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.data)


class HashMap:
    """Simple hash map implementation."""
    
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.buckets: List[List] = [[] for _ in range(capacity)]
    
    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity
    
    def put(self, key: Any, value: Any) -> None:
        """Insert or update key-value pair. O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.size += 1
    
    def get(self, key: Any, default: Any = None) -> Any:
        """Get value by key. O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def remove(self, key: Any) -> bool:
        """Remove key-value pair. O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        
        return False
    
    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None


if __name__ == "__main__":
    # Test LinkedList
    print("=== Linked List ===")
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    print(f"List: {ll.to_list()}")
    ll.reverse()
    print(f"Reversed: {ll.to_list()}")
    
    # Test Stack
    print("\n=== Stack ===")
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Pop: {stack.pop()}")
    print(f"Peek: {stack.peek()}")
    
    # Test Queue
    print("\n=== Queue ===")
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(f"Dequeue: {queue.dequeue()}")
    print(f"Front: {queue.front()}")
    
    # Test BST
    print("\n=== Binary Search Tree ===")
    bst = BinarySearchTree()
    for val in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(val)
    print(f"Inorder: {bst.inorder()}")
    print(f"Search 4: {bst.search(4)}")
    print(f"Search 9: {bst.search(9)}")
    
    # Test HashMap
    print("\n=== Hash Map ===")
    hm = HashMap()
    hm.put("name", "Alice")
    hm.put("age", 30)
    print(f"name: {hm.get('name')}")
    print(f"age: {hm.get('age')}")
    print(f"'name' in map: {'name' in hm}")

# unbalanced
