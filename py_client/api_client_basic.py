import json
import requests

def basic_retrieve(token, pk=""):
    endpoint = f"http://localhost:8000/dorinsocialapi/profiles/{pk}"
    data = {}
    headers = {"Authorization": f"Bearer {token}"}
    get_response = requests.patch(endpoint, headers=headers, json=data)
    formatted_response = get_response.json()
    try:
        return print(json.dumps(formatted_response, indent=4))
    except:
        return print(get_response)

pk = input("Do you have a primary-key? (If not, press Enter)")
token_inp = input("What is your token?")

basic_retrieve(token_inp, pk)

