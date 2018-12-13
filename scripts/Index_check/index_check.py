#!/usr/bin/python
from __future__ import print_function


import os
import sys
import json


# sys.argv[1] - regex para o indice nao comprimido , exemplo logs-.*
# sys.argv[2] - regex para o indice comprimido , exemplo logs_mc-.*
# sys.argv[3] - IP do elasticsearch a ser requisitado

IP=sys.argv[3]

def get_first_part(string):

        final_string=""
        stop =85
        i=0
        while i <= len(string)-1:

                if i >= stop:
                        final_string += string[i]

                i += 1

        return final_string

def get_import_part(string):

        final_string=""
        stop=8
        i=0
        while i <= len(string)-1:

                if i <= stop:
                        final_string += string[i]

                i += 1

        final_string = final_string.strip(':')
        return final_string


def get_indexes_pan():

	# Cria  o arquivo indexes_file
	os.system("touch ./indexes_file")
	indexes_file = open("./indexes_file","r+")

	index_arr = []
	#Pega o tamanho de cada indice existente do paloalto
	indexes_info = os.popen("curl -X GET '{0}:9200/_cat/indices' | grep {1}".format(IP,sys.argv[1])).read()
	
	os.system("echo '{0}' > ./indexes_file".format(indexes_info))

	for index in indexes_file:
		index=index.strip('\n')
		index=index.replace(' ',':')
		index= get_first_part(index)
		index_arr.append(index)
	
	os.system("rm -f ./indexes_file")

	return index_arr

def get_indexes_mc():

        # Cria  o arquivo indexes_file
        os.system("touch ./indexesmc_file")
        indexes_file = open("./indexesmc_file","r+")

        index_arr = []
        #Pega o tamanho de cada indice existente do paloalto
        indexes_info = os.popen(" curl -X GET '{0}:9200/_cat/indices' | grep {1}".format(IP,sys.argv[2])).read()

        os.system("echo '{0}' > ./indexesmc_file".format(indexes_info))

        for index in indexes_file:
                index=index.strip('\n')
                index=index.replace(' ',':')
                index= get_first_part(index)
                index_arr.append(index)

        os.system("rm -f ./indexesmc_file")

        return index_arr

	
def get_sizes(arr):

	size_arr = []
	for string in arr:
		size = get_import_part(string)
		size_arr.append(size)

	size_arr.pop()

	return size_arr


def sum_sizes(arr):

	byte_arr=[]
	for size in arr:

		if "gb" in size:
			size = size.strip("gb")
			# Transforma em mb
			size = float(size)*1000
			byte_arr.append(float(size))

		elif "mb" in size:
			size = size.strip("mb")
			byte_arr.append(float(size))

		elif "kb" in size:
			size = size.strip("kb")
			# Transforma em mb
			size = float(size)/1000
			byte_arr.append(float(size))

		elif "b" in size:
			size = size.strip("b")
			# Transforma em mb
			size = float(size)/1000000
			byte_arr.append(float(size))

	size=0
	for byte in byte_arr:
		size += float(byte)

	size = size/1000
	return size

def json_construct(size_crude, size_comp):
	
	GenerateTime = os.popen("date +%s%3N").read()
	GenerateTime = GenerateTime.strip("\n")

	Proportion = size_crude/size_comp
	Percent = size_comp/size_crude
	Proportion = round(Proportion, 2)
	Percent = round(Percent,2)

	#dicionary = {
	#	"GenerateTime":"{0}",
	#	"PAN Log Size":"{1}",
	#	"PAN Log MC Size":"{2}",
	#	"PAN Log Proportion":"{3}",
	#	"PAN Log Percent":"{4}".format(GenerateTime,round(size_crude,2),round(size_comp,2),Proportion,Percent)}

	#dicionary["GenerateTime"] = GenerateTime
	#dicionary["PAN Log Size"] = round(size_crude,2)
	#dicionary["PAN Log MC Size"] = round(size_comp,2)
	#dicionary["PAN Log Proportion"] = Proportion
	#dicionary["PAN Log Percent"] = Percent

	#Response = json.dumps(dicionary, ensure_ascii=False)
	#Response = Response.strip('\n')
	#print(Response)
	
	#print(dicionary,end='')
	print("{0};{1};{2};{3};{4}".format(GenerateTime,round(size_crude,2),round(size_comp,2),Proportion,Percent),end='')

	#return Response

INDEX_PANMC=get_indexes_mc()
SIZE_PANMC=get_sizes(INDEX_PANMC)


INDEX_PAN=get_indexes_pan()
SIZE_PAN=get_sizes(INDEX_PAN)

json_construct(sum_sizes(SIZE_PAN),sum_sizes(SIZE_PANMC))
