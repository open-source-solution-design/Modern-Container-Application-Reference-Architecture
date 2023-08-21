
import os
import json

def write_env(data):
    for key, value in data.items():
        os.environ[key] = str(value)

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)
