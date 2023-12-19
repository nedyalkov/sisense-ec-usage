import requests
import pandas as pd
import json

def get_usage(base_url, token):
    HEADERS = {
        "Authorization": f"Bearer {token}"
    }

    url = f'{base_url}/api/elasticubes/servers'
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code}, {response.json()}')

    response_json = response.json()

    ec_size_data = []

    for obj in response_json:
        for i in obj['cubes']:
            title = i['title']
            size = i['sizeInMb']
            ec_size_data.append({'ec_name': str(title), 'size': size})

    ec_size_data
    return pd.DataFrame(ec_size_data)

with open('config.json') as config:
    envs = json.load(config)["environments"]

for env in envs:
    usage = get_usage(env['url'], env['token'])
    usage.sort_values(by=['size'], inplace=True, ascending=False)
    print(f'Usage for {env["url"]}: {usage}')
    print(f'Total: \t{usage["size"].sum()} MB')