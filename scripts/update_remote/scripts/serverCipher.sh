#!/bin/bash

# $1 - O caminho absoluto para o respositório atual do AvantData
#AVNTDT="/var/www/html"
AVNTDT="/root/AUTO_SCRIPT/Scripts/avantdata_scripts/update_remote/repos/dev"

if [ -n $1 ] ; then

	# Compila, comprime e cifra o conteúdo do repositório atual
	cd $AVNTDT ; tar -czf - * | openssl enc -e -k AvntDt,, -aes256 -out avntdt.tar.gz #; mv -f avntdt.tar.gz $AVNTDT/atual
	

fi
