import os
import json
import yaml

def read_env():
    return dict(os.environ)

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
