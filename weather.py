#!/usr/bin/env python3
# Simple weather lookup utility
# Copyleft Alexandria Pettit, 2019
# GNU GPLv3

from urllib import request
import json, gzip
from os import makedirs, path
from sys import argv
from pprint import pprint

def parse_json_url(url):
    data = request.urlopen(url).read()
    return json.loads(data)

def mkdir_p(directory):
    try:
        makedirs(directory)
    except FileExistsError:
        pass

work_dir = path.join(path.expanduser("~"), '.simpleweather')
zipcode_db_path = path.join(work_dir, 'zipcodes.json.gz')
zipcode_db_url = 'https://raw.githubusercontent.com/alxpettit/simple-cli-weather/master/zipcodes.json.gz'
zipcode_db = None

mkdir_p(work_dir)

if not path.exists(zipcode_db_path):
    with open(zipcode_db_path, 'wb') as db:
        data_gz = request.urlopen(zipcode_db_url).read()
        db.write(data_gz)
        zipcode_db = gzip.decompress(data_gz)
else:
    with gzip.open(zipcode_db_path, 'rb') as db:
        zipcode_db = db.read()

zipcode_db = json.loads(zipcode_db.decode('utf-8'))
zipcode = argv[1]
coords = zipcode_db[zipcode]


print('Querying api.weather.gov for zipcode {zipcode}, \
which will have coords {coords}.'.format(zipcode=zipcode, coords=coords))

# WARNING! Database input not sanitized!
# This could cause code injection down the line with malicious DBs -- please fix, future-me.
resource_json = parse_json_url('https://api.weather.gov/points/' + ','.join(coords))
forecast_url = resource_json['properties']['forecast']

print('Stage 1 finished. URL recieved: {url}'.format(url=forecast_url))
forecast_json = parse_json_url(forecast_url)

pprint(forecast_json)
