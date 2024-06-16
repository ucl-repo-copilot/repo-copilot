from uuid import uuid4

class A:
    def methodA1(self):
        str(uuid4())
        print("Method 1 from class A")
    
    def methodA2(self):
        print("Method 2 from class A")
        
def methodA3():
    print("Method 3 from module A")