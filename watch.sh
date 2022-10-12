#!/bin/bash
export VERSION=11
touch "/shared_etc/hosts_crawled$VERSION"
while :
do
  echo "peers crawl loop"
  tmp=$(mktemp)
  cat hosts_header > $tmp
  cat "/shared_etc/hosts_crawled$VERSION" >> $tmp
  cat $tmp > /shared_etc/yg_hosts
  rm $tmp
  cat /shared_etc/yg_hosts
  echo "run crawl script"
  python3 -u example.py
  echo "ran script"

  sleep 10
done