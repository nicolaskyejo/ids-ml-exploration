#!/usr/bin/env bash

sudo apt-get update && sudo apt-get install -y dvwa
sudo sed -i 's/127\.0\.0\.1:42001/127.0.0.1:80/g' "$(which dvwa-start)"
sudo sed -i 's/listen 42001/listen 80/g' /etc/dvwa/vhost/dvwa-nginx.conf
sudo sed -i '/allow 127\.0\.0\.1;/a \    allow 192.168.56.0/21;' /etc/dvwa/vhost/dvwa-nginx.conf
