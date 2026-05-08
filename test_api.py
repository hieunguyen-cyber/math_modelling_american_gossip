import requests
import json

payload = {
    "custom_nodes": [{"id": 0, "label": "0"}, {"id": 1, "label": "1"}],
    "custom_edges": [{"from": 0, "to": 1}],
    "mode": "local",
    "q": 1.0,
    "k": 2,
    "victim": None,
    "origin": None
}

try:
    r = requests.post("http://127.0.0.1:5000/api/generate", json=payload)
    print("Status Code:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print(e)
