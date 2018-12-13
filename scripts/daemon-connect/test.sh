#!/bin/bash

NET_IN=$(cat ./ConnectCheck_config | grep NetScriptsIN)
ROLLER="A"
I=2

DELIMITER_COUNT=$(echo "$NET_IN" | awk -F":" '{print NF-1}')
DELIMITER_STOP=$(($DELIMITER_COUNT+1))


while [ $ROLLER == "A" ]
do

	PARSER=$(echo $NET_IN | cut -d: -f$I)

	if [ $I -le $DELIMITER_STOP ] ; then
	
		echo "$PARSER"

	elif [ $I -gt $DELIMITER_STOP  ] ; then

		ROLLER="B"
	fi
	
	I=$(($I+1))

done
