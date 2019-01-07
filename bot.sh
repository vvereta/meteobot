#!/bin/bash

usage() {
    echo "Usage: $0 [start][stop][restart][log][status]"
    exit 0
}

log() {
    journalctl --unit=meteobot.service -n 25 --no-pager
    exit 0
}

restart() {
    echo "restarting bot"
    systemctl restart meteobot.service
    exit 0
}

start() {
    echo "starting bot"
}

status () {
    systemctl status -l meteobot.service
}

if [ $# -ne 1 ]
then
    usage
fi

case $1 in 
    "help") usage;;
    "log") log;;
    "restart") restart;;
    "start") start;;
    "status") status;;
esac