from a import A
from b import B

class C:
    def __init__(self):
        self.a = A()
        self.b = B()
    
    def methodC1(self):
        print("Method 1 from class C")
        self.a.methodA1()
        self.b.methodB1()
    
    def methodC2(self):
        print("Method 2 from class C")
        self.a.methodA2()
        self.b.methodB2()

def methodC3():
    print("Method 3 from module C")