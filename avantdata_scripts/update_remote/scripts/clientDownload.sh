#!/bin/bash

# Script para baixar a nova versão do programa
# $1 - Nome do arquivo que teremos que baixar
IP=192.168.102.5

if [ -z $1 ] ; then

	echo "Error, faltou o parâmetro."

elif [ -n $1 ] ; then
	
	# Faz o Download do arquivo passado como parâmetro
	wget --no-check-certificate -q -P /temp/latest https://$IP:8443/atualizacao/versao/$1

fi
