#!/usr/bin/env python

import json
import os

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Assuming the JSON file is in the 'output' directory
    output_dir = os.path.join('IAC', 'output')
    json_file = os.path.join(output_dir, 'output.json')

    instances = read_json(json_file)

    ansible_inventory = {
        '_meta': {
            'hostvars': {}
        },
        'aws': {
            'hosts': [],
            'vars': {}
        }
    }

    for instance in instances:
        ansible_inventory['aws']['hosts'].append(instance['public_ip_address'])

    print(json.dumps(ansible_inventory, indent=2))

if __name__ == '__main__':
    main()
