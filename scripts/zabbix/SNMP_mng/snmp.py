#!/usr/bin/python3
#  Autor: Daniel Gomes Venzi Gonçalves     |
#  E-mail: gomesvenzi@gmail.com            |
#------------------------------------------#

#Incluir um break no loop de verificação de status da interface

import os
import sys
import json
import string
import random

#argv[1] = Endereço IP do firewall
#argv[2] = Community name do firewall
#argv[3] = Array de Objetos SNMP
#argv[4] = Nome da MIB

#----------------------------------------------------------------------

#Objetos desejados
arr = sys.argv[3].split(',')

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def get_error():
	STATUS = os.popen("echo $?").read()
	STATUS = STATUS.strip('\n')

	return STATUS

def get_snmp_OID(array):

	# SNMP OID's
	oid_array = []
		
	# Tradução dos nomes para OID's setados no arquivo de configuração
	for OBJ in array:
		PRE_OID = os.popen("cat ./INTERNAL_MIB/paloalto.oid | grep '^{0}'".format(OBJ)).read()
		PRE_OID = PRE_OID.strip('\n')
		OID = os.popen("echo '{0}' | cut -d':' -f2 ".format(PRE_OID)).read()
		OID = OID.strip("\n")
		oid_array.append(OID)

	return oid_array

def get_OID_value(array):
	
	oid_result = []

	# Gera uma string aleatória para servir de nome do arquivo processado
	archive_name = random_string(20)
	
	# Faz a requisição do valor do objeto SNMP e processa o resultado para deixar o valor exato

	for OID in array:
		VALUE = os.popen("snmpget -v 2c -c {0} {1} {2}".format(sys.argv[2],sys.argv[1],OID)).read()		
		VALUE = VALUE.strip('\n')

		if "Counter32" in VALUE:
			PROCESSED_VALUE = os.popen(" echo {0} > ./random_files/{1} ; cat ./random_files/{1} | cut -d'=' -f'2' | cut -d':' -f2 ".format(VALUE,archive_name)).read()

		elif "Counter64" in VALUE:
			PROCESSED_VALUE = os.popen(" echo {0} > ./random_files/{1} ; cat ./random_files/{1} | cut -d'=' -f'2' | cut -d':' -f2 ".format(VALUE,archive_name)).read()

		elif "STRING" in VALUE:
			PROCESSED_VALUE = os.popen(" echo {0} > ./random_files/{1} ; cat ./random_files/{1} | cut -d'=' -f'2' | cut -d':' -f2 ".format(VALUE,archive_name)).read()
		
		elif "INTEGER" in VALUE:
			PROCESSED_VALUE = os.popen(" echo {0} > ./random_files/{1} ; cat ./random_files/{1} | cut -d'=' -f'2' | cut -d':' -f2 ".format(VALUE,archive_name)).read()

		#elif "Timeticks" in VALUE:
		#	os.system("echo {0} > ./random_files/{1}".format(VALUE,archive_name))
		#	PROCESSED_VALE = os.popen("cat ./random_files/{1} | grep -Po 'Timeticks: \K.*' ".format(VALUE,archive_name)).read()

		else:	
			os.system("rm -f ./random_files/{0}".format(archive_name))
			continue

		# Delete os arquivos com nome aleaótorio
		os.system("rm -f ./random_files/{0}".format(archive_name))

		# Tira os endlines do valor processado do objeto
		PROCESSED_VALUE = PROCESSED_VALUE.strip('\n')	
	
		# Coloca o resultado processado no array
		oid_result.append(PROCESSED_VALUE)
	

	return oid_result

def JSONEncoder(mib_type,name_array,result_array):

	# Declaração do dicionário
	dic = {}

	# Determina qual o OID file a partir do tipo de MIB
	oid_file = os.popen("cat ./INTERNAL_MIB/MIB_CORREC/mib_correc | grep '{0}' | cut -d':' -f2".format(mib_type)).read()
	oid_file = oid_file.strip('\n') 
	
	i = 0
	for name in name_array:
		FIELD = os.popen("cat {0} | grep {1} |cut -d':' -f3".format(oid_file,name)).read()
		FIELD = FIELD.strip('\n')
	
		dic[FIELD] = result_array[i] 

		i = i+1	
		

	# Gera o generatetime em epoch milis		
	GenerateTime = os.popen("date +%s%3N").read()
	GenerateTime = GenerateTime.strip('\n')

	# Coloca no dicionário o campo GenerateTime
	dic["GenerateTime"] = GenerateTime
	
	# Faz a formatação de dados para json
	Json = json.dumps(dic, ensure_ascii=False)
	
	return Json

def main(array):

	Json = JSONEncoder(sys.argv[4],arr,get_OID_value(get_snmp_OID(array)))
	print(Json)

# Debugging section
#print(get_snmp_OID(arr)) # Printa o array com os OID
#print(get_OID_value(get_snmp_OID(arr))) # Printa o resultado da requisição SNMP
#main(arr)
