# function are divided into 3 category
# 1. In-built function  - input(), print(), append(), extend(), split(), join()
# 2. package/product based function  pandas-- , langchain.agent(), langchain,create_agent()
# 3. user defined function


# def func1():
#     print("this is a function")


# func1()


# def func2(a, b):
#     c = a + b
#     return c


# d = func2(10, 20)  # 30
# print(d)

# # black  and mypy
# # pip install black mypy


# def func3(a: int, b: int):
#     c = int(a + b)
#     return c


# E = func3(10, 20.55)  # 30
# print(E)



# def func4(a: int=5, b: int=10):
#     c = int(a + b)
#     return c

# E = func4(30, 40)  # 30
# print(E)


def func5(*args):
    print(args)
    
    
l1 = [1,2,3,4,5]
l2 = [20.5,"kumar"]
func5(l1,l2)