import re
import uuid

from a import A, methodA3

class B:
    def __init__(self):
        self.a = A()
    
    def methodB1(self):
        print("Method 1 from class B")
        self.a.methodA1()
    
    def methodB2(self):
        str(uuid.uuid4())
        re.compile(r"")
        print("Method 3 from class B")
        methodA3()