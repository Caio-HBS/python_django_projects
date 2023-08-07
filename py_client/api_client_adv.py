import json
import requests

def obtain_auth_token():
    endpoint = "http://localhost:8000/dorinsocialapi/get-auth-token/"
    data = {'username': 'test_user', "password": '23061999Mj'}
    get_response = requests.post(endpoint, data=data)
    if get_response.status_code == 200:
        json_response = get_response.json()
        token = json_response['token']
        user_id = json_response['user_id']
        print(f'Token: {token}')
        print(f'User ID: {user_id}')
    else:
        print(f'Falha na autenticação. Status code: {get_response.status_code}')


def coisa_linda():
    endpoint = "http://localhost:8000/dorinsocialapi/profiles/"
    headers = {'Authorization': "Bearer b781a2fae6ccc831972dd3404f0df8ff26c11337"}
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print(json.dumps(json_response, indent=4))
    else:
        print(response)


# coisa_linda()
obtain_auth_token()
