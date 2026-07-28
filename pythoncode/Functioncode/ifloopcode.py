import requests

url = "https://github.com"

response = requests.get(url)
# for item in response.headers:
#     print(item, ":", response.headers[item])

if response.status_code == 200:
    print("Request was successful")
else:
    print("Request failed with status code:", response.status_code)

# if response["status_code"] == 200:
#     print("Request was successful")
# else:
#     print("Request failed with status code:", response.status_code)

