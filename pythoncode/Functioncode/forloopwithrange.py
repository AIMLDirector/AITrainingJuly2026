# range(start, stop, step) - start is inclusive, stop is exclusive, step is optional /incremental value, 
# default start is 0 , step default value is 1
#range(10)  -- 10 as stop value , start is 0, step is 1 
#range(1,10) - start  is 1 , stop is 10 , step is 1
#range(1,10, 2) - start is 1, stop is 10, step is 2

for i in range(10):  # output: 0,1,2,3,4,5,6,7,8,9
    print(i)
   
Even_number = []
odd_number = [] 
    
for i in range(1,10):
    if i % 2 == 0:
        Even_number.append(i)
    else:
        odd_number.append(i)
print("Even numbers:", Even_number)
print("Odd numbers:", odd_number)

word = "cherry"
count = 0
for i in range(len(word)):  # 6 - 0 to 5 
    if word[i] == "r":
        print("Found r at index:", i)
        count += 1
print(f"Total count of r in the word: {word} is {count}")


for i in range(1,10):
    if i == 6:
        print("Breaking the loop at i =", i)
        break
    print(i)

# word generated, word used in prompt 
documents = ['i am learning python for the past 3 weeks', 'python is easy to learn' ]
max_length = 6

for i in documents:
    token = i.split()
    if len(token) > max_length:
        print(f"Truncating the document: {token[:max_length]}")
        

# In built functions - input(), print(), len(), range(), len(), join(), split() append()
user_input = input("Enter your query:")

while True:
    if len(user_input.split()) > max_length:
        user_query = user_input.split()[:max_length]
        user_query = " ".join(user_query)
        print(f"Truncating the user input to: {user_query}")
        break
    else:
        print("User input is within the limit")
        break

# while <condition>:
#     <code block>

while True:
    user_input = input("Enter your query: ")
    if user_input.lower() == "exit":
        print("Exiting the loop")
        break
    elif user_input.lower() == "skip":
        print("Skipping the current iteration")
        continue    
    else:
        print(f"User input is: {user_input}")
        break
    
  

number = 0
while number < 10:
    print("Current number is:", number)
    number += 1
    if number == 5:
        print("Breaking the loop at number =", number)
        break
print("Loop has ended. Final number is:", number)
    
user_login_attempts = 0
max_login_attempts = 3

while user_login_attempts < max_login_attempts:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # Simulating a login check (replace with actual authentication logic)
    if username == "admin" and password == "password":
        print("Login successful!")
        break
    else:
        user_login_attempts += 1
        print(f"Login failed. Attempt {user_login_attempts} of {max_login_attempts}.")
        
        if user_login_attempts == max_login_attempts:
            print("Maximum login attempts reached. Access denied.")
            
