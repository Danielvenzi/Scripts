#!/usr/bin/python3

#import sys
#sys.path.insert(0,'./code/snmp_avantdata.py')
from snmp_avantdata import *
# Pega o array dos elementos desejados pelo usuário
arr = sys.argv[3].split(',')
# Chama o main do programa
main(arr) 
