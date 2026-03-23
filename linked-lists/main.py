class Node:
    def __init__(self,data,next=None):
        self.data = data
        self.next = next
    def get_data(self):
        return self.data
    def set_next(self, next):
        self.next = next
    def get_next(self):
        return self.next
    
 

class LinkedList:
    def __init__(self,head=None):
        self.head = head
    def add(self,data):
        new_node = Node(data,self.head)
        self.head = new_node
    def remove(self,data):
        node = self.head
        prev_node = None
        while node:
            if node.get_data() == data:
                if prev_node:
                    prev_node.set_next(node.get_next())
                else:
                    self.head = node.get_next()
                return True
            else:
                prev_node = node
                node = node.get_next()
        return False
                
    def traverse(self):
        current_node = self.head
        while current_node:
            print(current_node.get_data())
            current_node = current_node.get_next()

class Stack:
    def __init__(self,head=None):
        self.head = head
    def pop(self):
        head = self.head
        self.head = head.get_next()
        return head.get_data()
    def push(self,data):
        new_node = Node(data,self.head)
        self.head = new_node

class Queue:
    def __init__(self,head=None,tail=None):
        self.head = head
        self.tail = tail
    def enqueue(self,data):
        new_node = Node(data,None)
        if self.tail is None:
            self.head = new_node
        else:
            self.tail.set_next(new_node)
        self.tail = new_node
    def dequeue(self):
        head = self.head
        self.head = head.get_next()
        return head.get_data()

class HashMap:
    def __init__(self,head=None):
        self.main_list = [None] * 10
        self.head = head
    def put(self,key,value):
        index = (hash(key)) % 10
        if self.main_list[index] is None:
            self.main_list[index] = LinkedList()
            self.main_list[index].add((key, value))
        else:
            (self.main_list[index]).add((key,value))

    def get(self,key):
        index = (hash(key)) % 10
        if self.main_list[index] is None:
            return None
        current_node = (self.main_list[index]).head
        while current_node:
            if (current_node.get_data())[0] == key:
                return current_node.get_data()
            current_node = current_node.get_next()

    def delete(self,key):
        index = hash(key) % 10
        if self.main_list[index] is None:
            return None
    
        node = (self.main_list[index]).head
        prev_node = None

        while node:
            if (node.get_data())[0] == key:
                if prev_node:
                    prev_node.set_next(node.get_next())
                else:
                    self.main_list[index].head = node.get_next()
                return True
            else:
                prev_node = node
                node = node.get_next()
        return False






hm = HashMap()
hm.put("AAPL", 207.67)
hm.put("TSLA", 348.21)
hm.put("GOOGL", 307.69)
print(hm.get("AAPL"))    # should print 207.67
print(hm.get("TSLA"))    # should print 348.21
hm.put("AAPL", 210.50)   # update existing key
print(hm.get("AAPL"))    # should print 210.50
hm.delete("TSLA")
print(hm.get("TSLA"))    # should print None