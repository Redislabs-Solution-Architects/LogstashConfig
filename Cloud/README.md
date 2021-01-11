## Redis Cloud Log Scraper

This script is intended to poll the redis cloud log endpoint and pull the log entries for ingestion into logstash


### Prerequisites

Python 3


### Installation

1) Copy the script scrape_cloud_logs.py to /usr/local/bin

2) Copy the example_config.yaml to /etc/config.yaml and edit the file

3) Use redisenterprise.config or filebeat.yaml example configurations for your logstash setup

4) Setup a Systemd unit file similar to the following in /lib/systemd/system/scrape-cloud-logs.service

```
#####################################################################
[Unit]
Description=Scrape Redis Cloud logs
After=network.target

[Service]
WorkingDirectory=/tmp
Type=simple
User=redislabs
ExecStart=/usr/local/bin/scrape_cloud_logs.py -c /etc/config.yaml
StandardOutput=file:/var/log/rediscloud-out.log
StandardError=file:/var/log/rediscloud-error.log


[Install]
WantedBy=multi-user.target
Alias=scrapte-cloud-logs.service

```

5) Setup the service

```
systemctl daemon-reload
systemctl enable scrape-cloud-logs.service
systemctl start scrape-cloud-logs.service

```

