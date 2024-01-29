import json

def get_data():
    with open('data.json', 'r') as file:
        return json.load(file)