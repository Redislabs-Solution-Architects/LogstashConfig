#!/usr/bin/env python3

import requests
import yaml
import getopt
import sys
import datetime
import json
import time

def fetch_data(config):

    try:
        logfile = open(config['log-file'], 'a')
    except Exception as err:
        print("Unable to open logfile: ", config['log-file'])
        exit(1)

    offset = 0
    try:
        f = open(config['state-file'], 'r')
        offset = int(f.read().rstrip())
        f.close()
    except Exception as err:
        logfile.write(json.dumps(
            {"time": int(datetime.datetime.now().timestamp()),
            "type": "Info",
            "description": "Writing new statefile {}".format(config['state-file'])}
            ))
        logfile.write("\n")

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
            logfile.write(json.dumps(
                {"time": int(datetime.datetime.now().timestamp()),
                "type": "Error",
                "description": "ERROR: HTTP status code: {} for {}".format(r.status_code, config['host'])}
                ))
            logfile.write("\n")
            logfile.close()
            return

        j = r.json()

        for entry in sorted(j['entries'], key=lambda item: item['id']):
            entry['time'] = int(datetime.datetime.strptime(entry['time'], "%Y-%m-%dT%H:%M:%SZ").strftime('%s'))
            if entry['time'] >= offset:
                logfile.write(json.dumps(entry))
                logfile.write("\n")
                offset = entry['time']

    except Exception as err:
        logfile.write(json.dumps(
            {"time": int(datetime.datetime.now().timestamp()),
            "type": "Error",
            "description": err}
            ))
        logfile.write("\n")


    try:
        w = open(config['state-file'], 'w')
        w.write(str(offset+1))
        w.close()
    except Exception as err:
        logfile.write(json.dumps(
            {"time": int(datetime.datetime.now().timestamp()),
            "type": "Error",
            "description": err}
            ))
        logfile.write("\n")

    logfile.close()

if __name__ == "__main__":

    configfile = "./config.yaml"

    options, z = getopt.getopt(sys.argv[1:], 'c:h', ['config=',"help"])
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print("Run with -c or --config to specify a config file other than ./config.yaml")
            exit
        if opt in ('-c', '--config'):
            configfile = arg

    try:
        with open(configfile) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except Exception as err:
        print("Unable to load config file: %s" %(configfile))
        exit(1)

    while True:
        fetch_data(config)
        time.sleep(config['poll-interval'])