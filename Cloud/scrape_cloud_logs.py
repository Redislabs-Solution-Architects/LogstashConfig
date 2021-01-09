#!/usr/bin/env python3

import requests
import yaml
import getopt
import sys

configfile = "./config.yaml"

options, z = getopt.getopt(sys.argv[1:], 'c:h', ['config=',"help"])
for opt, arg in options:
    if opt in ('-h', '--help'):
        print("HELP GOES HERE")
    if opt in ('-c', '--config'):
        configfile = arg
    

try:
    with open(configfile) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
except Exception as err:
    print("Unable to load config file: %s" %(configfile))
    exit(1)



url = "https://%s/v1/logs" % (config['host'])

payload = {'limit': 200, 'offset': 0}

headers = {
    'user-agent': 'logstash-scraper',
    'accept': 'application/json',
    'x-api-key': config['api-key'],
    'x-api-secret-key': config['api-secret'],
    }
try:
    r = requests.get(
        url,
        headers=headers,
        params=payload
        )

    if r.status_code != 200:
        print("ERROR: HTTP status code: %s for %s" % (r.status_code, config['host']))
        exit(1)

    j = r.json()
    
    for entry in j['entries']:
        print(entry)

except Exception as err:
    print("ERROR: ", err)
    exit(1)
