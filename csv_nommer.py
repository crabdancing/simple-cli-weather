#!/usr/bin/python3
# Copyleft Alexandria Pettit, 2019

import json

def csv_nommer(data):
    output = {}
    for i, line in enumerate(data.split('\n')):
        if i == 0 or not line:
            continue
        line = line.split(',')
        line = [i.strip() for i in line]
        output[line[0]] = line[1:]
    return output

data = open('zipcodes.csv').read()
dict_data = csv_nommer(data)
json_data = json.dumps(dict_data, indent=4, sort_keys=True)

with open('zipcodes.json', 'w') as output_fh:
    output_fh.write(json_data)
