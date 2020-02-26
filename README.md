# Logstash Config

This contains an example configuration to pull and process Redis Enterprise log files for centralization in an ELK deployment.

## Download logstash

wget https://artifacts.elastic.co/downloads/logstash/logstash-7.6.0.tar.gz
tar -zxvf logstash-7.6.0.tar.gz


## Testing
./logstash-7.6.0/bin/logstash  -f LogstashConfig/redisenterprise.conf --config.reload.automatic


Tester: https://grokdebug.herokuapp.com/


## Usage

If using filebeat comment out the local file selection in the input configuration

If using local files comment out the beats selection in the input configuration

## Data collected

### cnm_exec.log

cnm_exec contains cluster level logs containing information about data base creation, modification as well as failover events

### event_log.log

event_log is for processing Redis Enterprise monitoring events which can be configured in the Database configuration monitoring section

### redis-*.log

redis-*.log contains the low-level shard logs for all shards on the Redis Enterprise Cluster
