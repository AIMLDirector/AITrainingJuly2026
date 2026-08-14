import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwenmodel_Development:latest",
        "messages": [
            {"role": "user", "content": "Explain data lakehouse architecture"}
            
        ],
         "stream": False
    }
)

print(response.json()["message"]["content"])
