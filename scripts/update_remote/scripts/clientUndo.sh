#!/bin/bash

APACHE="/var/www/html"

if [ -z $1 ] ; then


	# Deleta o conteúdo de /temp/latest/avantdata_latest
	cd /temp/latest/avantdata_latest ; rm -rf ./*

	# Deleta o conteúdo do diretório do apache
	cd $APACHE ; rm -rf ./*

	# Move o conteúdo de /temp/old, ou seja, a versao anterior do AvantData
	cd /temp/old ; mv -f ./*  $APACHE


fi
