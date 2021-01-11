#!/usr/bin/env python3

import requests
import yaml
import getopt
import sys
import datetime
import json


def fetch_data(config):
    offset = 0
    try:
        f = open(config['state-file'], 'r')
        offset = int(f.read().rstrip())
        f.close()
    except Exception as err:
        print("no state file exists")

    url = "https://%s/v1/logs" % (config['host'])

    payload = {'limit': 200, 'offset': 0, 'order': 'asc'}

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

        for entry in sorted(j['entries'], key=lambda item: item['id']):
            entry['time'] = int(datetime.datetime.strptime(entry['time'], "%Y-%m-%dT%H:%M:%SZ").strftime('%s'))
            if entry['time'] >= offset:
                print(json.dumps(entry))
                offset = entry['time']

    except Exception as err:
        print("ERROR: ", err)


    try:
        w = open(config['state-file'], 'w')
        w.write(str(offset+1))
        w.close()
    except Exception as err:
        print("ERROR: ", err)

if __name__ == "__main__":

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

    fetch_data(config)