import json
import requests

def hit_endpoint(token):
    endpoint = "http://localhost:8000/dorinsocialapi/profiles/"
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print(json.dumps(json_response, indent=4))
    else:
        print(
            f'Authentication failed while hitting the endpoint. Status code: {response.status_code}'
        )

def obtain_auth_token(username, password):
    endpoint = "http://localhost:8000/dorinsocialapi/get-auth-token/"
    data = {'username': username, "password": password}
    get_response = requests.post(endpoint, data=data)
    if get_response.status_code == 200:
        json_response = get_response.json()
        token = json_response['token']
        user_id = json_response['user_id']
        print(f'Token: {token}')
        print(f'User ID: {user_id}')
        hit_endpoint(token)
    else:
        print(
            f'Authentication failed while obtaining Token. Status code: {get_response.status_code}'
        )

username_inp = input("What is your username?")
password_inp = input("What is your password?")

obtain_auth_token(username_inp, password_inp)


