#!/bin/bash

BOT_NAME=meteobot.service

usage() {
    echo "Usage: $0 [start][stop][restart][log][status]"
    exit 0
}

log() {
    journalctl --unit=$BOT_NAME -n 25 --no-pager
    exit 0
}

restart() {
    echo "restarting bot"
    systemctl restart $BOT_NAME
    exit 0
}

start() {
    echo "starting bot"
    systemctl start $BOT_NAME
}

status() {
    systemctl status -l $BOT_NAME
}

stop() {
    echo "stopping bot"
    systemctl stop $BOT_NAME
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
    "stop") stop;;
    *) usage;;
esac
