#!/bin/bash

ERROR="
	Wrong usage of command, use -h for help.
"

HELP="
	Ainda não to afim de fazer =]
"

nohup socat UDP-LISTEN:514,fork,range=$1/32 UDP:0.0.0.0:$2 &> /dev/null &
#echo "socat UDP-LISTEN:514,fork,range=$1/32 UDP:0.0.0.0:$2"
