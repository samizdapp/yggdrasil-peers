#!/bin/bash
export VERSION=5
touch "/peers/hosts_crawled$VERSION"
while :
do
  echo "peers crawl loop"
  tmp=$(mktemp)
  cat hosts_header > $tmp
  cat "/peers/hosts_crawled$VERSION" >> $tmp
  cat $tmp > /peers/yg_hosts
  cat /peers/yg_hosts
  echo "run crawl script"
  python3 -u example.py
  echo "ran script"

  sleep 10
done