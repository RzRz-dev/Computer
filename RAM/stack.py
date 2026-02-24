class Stack:
    #This piece of code makes the object singleton.
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(Stack, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.stack = [] #The stack will be implemented as a list, with the top of the stack being the end of the list
    
    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        if len(self.stack) == 0:
            raise Exception("Stack underflow")
        return self.stack.pop()
    
    def peek(self):
        if len(self.stack) == 0:
            raise Exception("Stack is empty")
        return self.stack[-1]
    
stack_ram = Stack()