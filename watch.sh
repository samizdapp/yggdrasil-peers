#!/bin/bash
export VERSION=3
while :
do
  echo "peers crawl loop"
  echo "run crawl script"
  python3 -u example.py
  echo "ran script"
  tmp=$(mktemp)
  cat hosts_header > $tmp
  cat "/peers/hosts_crawled$VERSION" >> $tmp
  cat $tmp > /peers/yg_hosts
  cat /peers/yg_hosts
  sleep 10
done