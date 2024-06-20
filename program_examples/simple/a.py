from uuid import uuid4

class A:
    def __init__(self):
        pass # Empty constructor
    
    def methodA1(self):
        str(uuid4())
        print("Method 1 from class A")
    
    def methodA2(self):
        self.methodA1()
        
def methodA3():
    print("Method 3 from module A")