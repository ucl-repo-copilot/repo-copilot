
## C.methodC1
```python
def methodC1(self):
    print('Method 1 from class C')
    self.a.methodA1()
    self.b.methodB1()
```
Internal calls: ``['A.methodA1', 'B.methodB1']`` <br/>
External calls: ``['print']`` <br/>
Documentation generated: ``X``
<br/>
    

## A.methodA1
```python
def methodA1(self):
    str(uuid4())
    print('Method 1 from class A')
```
Internal calls: ``[]`` <br/>
External calls: ``['str', 'print', 'uuid4']`` <br/>
Documentation generated: ``X``
<br/>
    

## B.methodB1
```python
def methodB1(self):
    print('Method 1 from class B')
    self.a.methodA1()
```
Internal calls: ``['A.methodA1']`` <br/>
External calls: ``['print']`` <br/>
Documentation generated: ``X``
<br/>
    