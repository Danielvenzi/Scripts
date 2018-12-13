#!/bin/bash

# Autor - Daniel Gomes Venzi - gomesvenzi@gmail.com
# $1 = IP exemplo para testar a conexão
# $2 = Tamanho máximo para tamanho do arquivo cache (em Bytes)

#Reset da posição dos parsers
mv /etc/logstash/conf.d/* /etc/logstash/desativados/

#Declaração de variáveis de controle
STAT="A"
LOOP="0"
ROLLER="A"
I=2

#Declaração das variáveis a partir do arquivo de configuração do parser
NET_IN=$(cat ./ConnectCheck_config | grep NetScriptsIN)
NET_OUT=$(cat ./ConnectCheck_config | grep NetScriptsOUT)
NET_COUNT=$(echo "$NET_IN" | awk -F":" '{print NF-1}')
NET_STOP=$(($NET_COUNT+1))

#Declaração das variáveis a partir do arquivo de configuração do parser de escrita em arquivos
CACHEW_IN=$(cat ./ConnectCheck_config | grep CacheWriteIN)
CACHEW_OUT=$(cat ./ConnectCheck_config | grep CacheWriteOUT)
CACHEW_COUNT=$(echo "$CACHEW_IN" | awk -F":" '{print NF-1}')
CACHEW_STOP=$(($CACHEW_COUNT+1))

#Declaração das variáveis a aprtir do arquivo de configuração do parser  de leitura em arquivos
CACHER_IN=$(cat ./ConnectCheck_config | grep CacheReadIN)
CACHER_OUT=$(cat ./ConnectCheck_config | grep CacheReadOUT)
CACHER_COUNT=$(echo "$CACHER_IN" | awk -F":" '{print NF-1}')
CACHER_STOP=$(($CACHER_COUNT+1))

while [ $STAT == "A" ] 
do
	if [ $LOOP == "0" ] ; then
		#Movimentação dos parsers de rede para as pastas de funcionamento correto
		while [ $ROLLER == "A" ]
		do
		
		        PARSER=$(echo $NET_IN | cut -d: -f$I)
		
		        if [ $I -le $NET_STOP ] ; then
	
		                mv $PARSER /etc/logstash/conf.d

		        elif [ $I -gt $NET_STOP  ] ; then

		                ROLLER="B"
		        fi
	
		        I=$(($I+1))
		done		
		I=2
		#STAT="B"
		LOOP="1"
	
	elif [ $LOOP == "1" ] ; then
	 	while [ $LOOP == "1" ] 
		do
			ping -c 1  $1
			if [ $? != "0" ] ; then
		
				#Executa a retirada dos parsers que enviam pela rede
				while [ $ROLLER == "B" ]
				do

				        PARSER=$(echo $NET_OUT | cut -d: -f$I)

				        if [ $I -le $NET_STOP ] ; then

				                mv $PARSER /etc/logstash/desativados

				        elif [ $I -gt $NET_STOP  ] ; then

				                ROLLER="C"
				        fi

				        I=$(($I+1))

				done	

				I=2

				#Colocar em execução os parser de escrita em arquivo
				while [ $ROLLER == "C" ]
				do

				        PARSER=$(echo $CACHEW_IN | cut -d: -f$I)

				        if [ $I -le $CACHEW_STOP ] ; then

				                mv $PARSER /etc/logstash/conf.d

				        elif [ $I -gt $CACHEW_STOP  ] ; then

				                ROLLER="D"
				        fi

				        I=$(($I+1))

				done

				I=2
				LOOP="2"
			fi

			#Dar uma esperada pra não floodar a rede
			wait 5
	
		done
	
	elif [ $LOOP == "2" ] ; then	
		
		while [ $LOOP == "2" ]
		do
			ping -c 1 $1
			if [ $? == "0" ] ; then
				#Executa a mudança dos parsers para voltar o envio de logs pela rede e leitura do arquivo de cache
				while [ $ROLLER == "D" ]
                                do

                                        PARSER=$(echo $NET_IN | cut -d: -f$I)

                                        if [ $I -le $NET_STOP ] ; then

                                                mv $PARSER /etc/logstash/conf.d

                                        elif [ $I -gt $NET_STOP  ] ; then

                                                ROLLER="E"
                                        fi

                                        I=$(($I+1))

                                done

				I=2

				while [ $ROLLER == "E" ]
                                do

                                        PARSER=$(echo $CACHEW_OUT | cut -d: -f$I)

                                        if [ $I -le $CACHEW_STOP ] ; then

                                                mv $PARSER /etc/logstash/desativados

                                        elif [ $I -gt $CACHEW_STOP  ] ; then

                                                ROLLER="F"
                                        fi
					I=$(($I+1))

                                done

				I=2

				while [ $ROLLER == "F" ]
                                do

                                        PARSER=$(echo $CACHER_IN | cut -d: -f$I)

                                        if [ $I -le $CACHER_STOP ] ; then

                                                mv $PARSER /etc/logstash/conf.d

                                        elif [ $I -gt $CACHER_STOP  ] ; then

                                                ROLLER="G"
                                        fi

                                        I=$(($I+1))

                                done
			
				I=2
				LOOP="4"
			
			elif [ $? != "0" ] ; then		
			
				#Comando para checar o tamanho do arquivo cache
				FILE_SIZE=$(ls -l ConnectCheck.sh | cut -d' ' -f5)	

				if [ $FILE_SIZE -gt $2  ] ; then

					#Executa a retirada total dos parsers
					mv /etc/logstash/conf.d/* /etc/logstash/desativados
					LOOP="3" 				
	
				fi
			
			fi
			
			wait 5
		
		done 
	
	
	elif [ $LOOP == "3" ] ; then
	
		while [ $LOOP == "3" ]
		do
			
			ping -c 1 $1

			if [ $? == "0" ] ; then
				
				#Colocar o parser para mandar pela rede e pegar logs do arquivo
				while [ $ROLLER == "G" ]
                                do

                                        PARSER=$(echo $NET_IN | cut -d: -f$I)

                                        if [ $I -le $NET_STOP ] ; then

                                                mv $PARSER /etc/logstash/conf.d

                                        elif [ $I -gt $NET_STOP  ] ; then

                                                ROLLER="H"
                                        fi

                                        I=$(($I+1))

                                done

				I=2

				while [ $ROLLER == "H" ]
                                do

                                        PARSER=$(echo $CACHER_IN | cut -d: -f$I)

                                        if [ $I -le $CACHER_STOP ] ; then

                                                mv $PARSER /etc/logstash/conf.d

                                        elif [ $I -gt $CACHER_STOP  ] ; then

                                                ROLLER="D"
                                        fi

                                        I=$(($I+1))

                                done

	
				LOOP="4"
			
			fi
		done
	
	elif [ $LOOP == "4" ] ; then

		while [ $LOOP == "4" ]
		do

			#Tirar o parser de leitura do arquivo, mas, como vou saber que ele terminou de ler?
			PARSER=$()
			
		done

	fi

done
