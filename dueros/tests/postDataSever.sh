#!/usr/bin/env bash
#记得根据自己的服务切换IP和端口
cd $(dirname $0)
dir=$(pwd)
#curl -H "Content-Type: application/json" -XPOST -d @$dir/$1 http://127.0.0.1:8000
#curl -H "Content-Type: application/json" -XPOST -d @$dir/$1 http://192.168.0.52:8000
curl -H "Content-Type: application/json" -XPOST -d @$dir/$1 http://things.yy845.com:8100