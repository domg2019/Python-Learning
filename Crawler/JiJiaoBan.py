import requests

url = "https://www.bb2y.com/page128"

head = {
   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

response = requests.get(url, headers=head)

print(response.text)
