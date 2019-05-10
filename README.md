Introduction
============

Docker containers and configs to ship log information from prod and stage(server1)server to Elastcisearch on a differnt server.
Make the containers on which elasticsearch,Kibana website runs secure using SSL and webserver(for reverse proxy).
Communication between filebeat container and elasticsearch container needs to be encrypted too.


FILEBEAT
--------

#### prod

Filebeat container runs on each of our application servers .
filebeat is continously monitoring the log location . Whenever there is a new results-*.json available(on daily basis) , it ships it to elasticsearch.

#### Setup

Extract and ship the parsed logs from Server1 everyday to Elasticsearch container on Server2.
The parsed logs contain :
Info required to evaluate performance of your application
 
The app logs are parsed using a python script in prod servers that is set as a cronjob to run everyday.
parsed log location:
 
 `/var/log/someone/prod/results-*.json`

##Security

* Set SSL certificates for filebeat and elasticsearch communication


ELASTICSEARCH
-------------

Runs on container in server2.
Saves the data received from filebeat into index -prodinfo-6.3.2

The data in the index can be used to set up dashboards on kibana
9200 port not exposed outside, so without access to kibana not possible to run queries on elastic search

KIBANA
------

Runs on container in Server2
`kibana.someone.io:8080` . 

Webserver
----------

webserver container on Server2 hides kibana and elasticsearch by reverse proxy . this is to secure Kibana and lasticsearch from public access
Elasticsearch has its own security package called XPACK that will handle aaccess control but its a licensed package .
So if you want to implement access control then best way is to use webserver for reverse proxy and SSL certificates to encrypt the communication.

Access/signin controlled by username and password.

* username: someone
* password: someonetrial

The password can be changed in dockerfile of webserver container. Restart the webserver container to reload config of 
elasticsearch, webserver and kibana at location:
 
 `/opt/someone/dockerfiles/es_kibana`

