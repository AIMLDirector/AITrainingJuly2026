
a = 1
b = 2

print(a)

def func1():
    c = 10  # local variables 
    print(c)
    print(a)


func1()

print(a)
print(c)  # This will raise a NameError because 'c' is not defined in this scope
