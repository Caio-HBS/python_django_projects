import json
import requests

def basic_retrieve(pk=""):
    endpoint = f"http://localhost:8000/dorinsocialapi/profiles/{pk}/update/"
    data = {
        'first_name' : 'Martinho'
        #"full_name": "Martinho Daledale",
        #"endpoint": "dorinsocialapi/profiles/22/",
        #"endpoint_custom_slug": "/dorin/profile/martinho_daledale/"
    }
    get_response = requests.patch(endpoint, json=data)
    formatted_response = get_response.json()
    try:
        return print(json.dumps(formatted_response, indent=4))
    except:
        return print(get_response)


basic_retrieve(22)