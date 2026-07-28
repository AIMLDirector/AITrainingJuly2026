# module are divided into 2 types 
# in build module part of python  -- os , sys, math,date, datetime, yaml, 
# external module provided by vendor : platform/ product/db/ 

import os
import time
from dotenv import load_dotenv
load_dotenv()

# cur_dir = os.getcwd()
# print(cur_dir)

# dir_name = "testdir"
# dir_path = os.path.join(cur_dir, dir_name)
# # print(dir_path)

# if os.path.exists(dir_path):
#     print("Directory is already created")
# else:
#     os.mkdir(dir_path)
    
    
# if os.name == 'nt':
#     os.system("cls")
# else:
#     time.sleep(10)
#     os.system("clear")


# os.system("df -h")

open_api_key = os.getenv("OPENAI_API_KEY")
username = os.getenv("oracle_user")
print(open_api_key)
print(username)


