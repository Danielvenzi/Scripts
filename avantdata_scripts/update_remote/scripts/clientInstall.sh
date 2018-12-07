#!/bin/bash

# Script utilizado para  verificar se existe uma nova versão para o AvantData
# $1 - Caminho do arquivo baixado no sistema de arquivos do cliente

#SECRET='AvantData!@#$%'
#echo $JSON | cut -d',' -f6 | cut -d':' -f2 | tr '}' ' ' | tr '"' ' ' | tr -s " " 
#echo $JSON_RESULT 
IP=192.168.102.5

	


if [ -z $1 ] ; then

	echo "Error, nenhum arquivo passado como argumento."

elif [ -n $1 ] ; then

	# Processo de mudança dos arquivos do apache para AvantData old
	systemctl stop httpd ; cd /var/www/html ; mv ./* /temp/old 
	
	# Faz o processo de descompressão, descifragem e descompactação
	cp -R $1 /temp/latest ; cd /temp/latest ; openssl enc -k AvantData,, -d -aes256 -in ./avantdata.tar.gz | tar -xz -C /temp/latest/avantdata_latest ; cd /temp/latest/avantdata_latest ; rm -f ./avantdata.tar.gz

	# Processo de mudança dos arquivos do apache para bckp e AvantData latest para o apache
	cp -R /temp/latest/avantdata_latest/* /var/www/html/ ; systemctl start httpd
			

fi
