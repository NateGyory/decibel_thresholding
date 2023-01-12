import json
import requests

URL = "http://localhost:5000/test"
PAYLOAD = {
  "waypoint_id": "hedged-whale-twQBHx1YyDBR2tbLzRtVlw=="
}

#HEADERS = {
#  'Content-Type': 'application/json'
#}

response = requests.post(URL, json=PAYLOAD)
print(response.text)
