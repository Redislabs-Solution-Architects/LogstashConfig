## Download logstash

wget https://artifacts.elastic.co/downloads/logstash/logstash-7.6.0.tar.gz
tar -zxvf logstash-7.6.0.tar.gz


## Testing
./logstash-7.6.0/bin/logstash  -f LogstashConfig/redisenterprise.conf --config.reload.automatic


Tester: https://grokdebug.herokuapp.com/

## filebeat 

