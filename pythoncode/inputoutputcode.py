# inbuild functions -- input(), print(), append(), delete(), extended(), sum() type()
a = input("Enter you name:")
from dotenv import load_dotenv
import os
load_dotenv()
username = os.getenv("account_username")
print(username)

print(a)
print("Hello " + a + " welcome to the world of python programming")
print(f"Hello {a} welcome to the world of python programming")  # preferred method 
print("Hello {} welcome to the world of python programming".format(a))
print("Hello %s welcome to the world of python programming" % a)

print(f"Total: {10 + 20}")  # expression inside f-string

print(f"PI value: {3.145665:.3f}")

b = 20
print(f"Total: {b + 30}")  # expression inside f-string
print(f"B value is {b = }")  # expression inside f-string

c = 30
print(f"{b = },{c = },{c + b = } ")

age = 11

print(f"Status: {'Adult' if age >= 18 else 'Minor'}")  # conditional expression inside f-string 

print(f"Welcome, {a.upper()}!")  # capitalize the first letter of the name

# sep and end - formatting and spacing 
print("09", "08", "2023", sep="/", end="\n")  # sep is used to separate the values and end is used to specify the end of the line