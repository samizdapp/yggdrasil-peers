#!/bin/bash

while :
do
  rm hosts_crawled
  python3 example.py
  cat hosts_header > /peers/yg_hosts
  cat hosts_crawled >> /peers/yg_hosts
  sleep 5
done