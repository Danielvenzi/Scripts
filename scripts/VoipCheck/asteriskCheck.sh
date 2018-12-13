#!/bin/bash


SERVICE="httpd"

if [ -n $1 ] ; then

		# Pega o PID do serviço setado na variável SERVICE
		PID_AST=$(systemctl status $SERVICE | grep "Main PID" | grep -Po '[0-9]{3,}' | tr -d ' ')
		
		# Pega a memória do serviço a partir do PID
                RES_AST=$(top -d1 -n1 -p$PID_AST | grep "$PID_AST" | cut -c38-44 | tr -d ' ')

		# Pega a CPU do serviço a partir do PID
		CPU_AST=$(top -d1 -n1 -p$PID_AST | grep "$PID_AST" | cut -c53-58 | tr -d ' ')

		
		# Pega memória Total do servidor
		MEMTOT=$(free | grep 'Mem' | cut -c10-26 | tr -d ' ')

		# Pega memória Usada do servidor
		MEMUSED=$(free | grep 'Mem' | cut -c26-34 | tr -d ' ')	

		./serverMem.py "$PID_AST:$RES_AST:$CPU_AST:$MEMTOT:$MEMUSED:"

fi
