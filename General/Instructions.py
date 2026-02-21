class Instruction:
    def __init__(self, value):
        self.value = value
        self.next = None

    def traverseAndReturn(head):
        currentInstruction = head
        while currentInstruction:
            print(currentInstruction.value)
            currentInstruction = currentInstruction.next