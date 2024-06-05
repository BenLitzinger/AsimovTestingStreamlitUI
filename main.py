import requests
from requests.structures import CaseInsensitiveDict
import json

url = "https://ac-pbconvai-dev-project.web.app/api/submitMessage"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

user_messages = ["Kreditkarte", "Hilfe", "Wie wird das Wetter morgen?"]

for user_message in user_messages:
    data = {
        "user_message": user_message,
        "agentId": "ed63e9f6-e8c7-4737-83cc-3f3be93ce2b4",
        "languageCode": "de",
        "sessionId": "874a8f1e-eb47-41ea-aa75-7821b7530d77",
        "useRoentgen": False
    }

    data_json = json.dumps(data)

    resp = requests.post(url, headers=headers, data=data_json)

    response_dict = json.loads(resp.text)

    response_text = response_dict['responseText']

    print(response_text)