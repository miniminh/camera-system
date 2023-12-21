import requests

url = "https://xoso188.net/api/front/open/lottery/history/list/5/doth"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
