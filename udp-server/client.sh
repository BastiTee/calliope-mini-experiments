#!/bin/bash

[ -z "$1" ] && { 
    echo "no host provided."
    exit 1
}

echo -n "hello, it's $( date ) on $( hostname )" > /dev/udp/192.168.43.231/33333
