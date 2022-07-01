#!/bin/bash
while :
do
  echo "peers crawl loop"
  echo "run script"
  python3 -u example.py
  echo "ran script"
  tmp=$(mktemp)
  cat hosts_header > $tmp
  cat hosts_crawled >> $tmp
  cat $tmp > /peers/yg_hosts
  cat /peers/yg_hosts
  sleep 10
done