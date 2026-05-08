import requests
import json

payload = {
    "custom_nodes": [{"id": 0, "label": "0"}, {"id": 1, "label": "1"}, {"id": 2, "label": "2"}],
    "custom_edges": [{"from": 0, "to": 1}, {"from": 1, "to": 2}],
    "mode": "probabilistic",
    "q": 1.0,
    "k": 2,
    "victim": None,
    "origin": None
}

try:
    r = requests.post("http://127.0.0.1:5000/api/generate", json=payload)
    print("Status:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print(e)
