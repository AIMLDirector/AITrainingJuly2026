l1 = [1,2.5, 3.2j, 'kk', 1,2.5 ]   # list 

# list we can add,modify, delete, append , sort, reverse, pop, remove, insert, extend, count, index, clear, copy
 # list - mutable, ordered, allows duplicate values, heterogeneous data types
# l2 = [10,20,21,20,30] # index - 0,1,2,3,4. index - negative index - -5,-4,-3,-2,-1
# l3 = [70,80]
# print(l2[0:3]) # 0,1,2
# print(l2[-1])
# l2.append(40)
# print(l2)
# l2.extend(l3)
# print(l2)
# l2.insert(1,15)
# print(l2)
# l2.sort(reverse=True)
# print(l2)

# # for i in l2:
# #     if i == 20:
# #         print("Found 20 in the list")
# #         l2.remove(20)
  
# if 20 in l2:
#     print("Found 20 in the list")
#     l2 = [i for i in l2 if i != 20]     
# print(l2)

t1 = (1,10,20,'kk', 1,10)  # tuple - immutable
t2 = ('root', 'admin', 'user')  # tuple - immutable
t2 = list(t2)
print(type(t2))
t2.append('guest')
t2 = tuple(t2)
print(type(t2))

s1 = {'root', 'admin', 'user'}  # set - mutable, unordered, no duplicate values , no indexing, no slicing
print(s1)

d1 = {'name':'kk', 'age':30, 'city':'NYC'}  # dictionary - mutable, unordered, key-value pairs, no indexing, no slicing

print(d1)
for key, value in d1.items():
    
    print(f"Key: {key}, Value: {value}")
  
print(d1.keys())
print(d1.values())
d1['address'] = "10th main"
print(d1)
d1.update({"age": 40})
print(d1)
# items function can be used along with dictionary, yaml, json