#!/bin/bash

if [ $1 != "-h" ] ; then

	echo "Wrong usage of command, WebChk.sh -h [HOST]"

elif [ $1 == "-h" ] ; then

	if [ -n $2 ] ; then
	
		response=$(curl --write-out %{http_code} --silent --output /dev/null $2)
		#echo "$response"

		if [ $response == "100" ] ; then
		
			STATUS="Continuar"

		elif [ $response == "101" ] ; then

			STATUS="Mudando protocolos"

		elif [ $response == "102" ] ; then

			STATUS="Processamento (WebDAV)(RFC 2518)"

		elif [ $response == "122" ] ; then

			STATUS="Pedido-URI muito longo"

		elif [ $response == "200" ] ; then

			STATUS="OK"

		elif [ $response == "201" ] ; then

			STATUS="Criado"
		
		elif [ $response == "202" ] ; then

			STATUS="Aceito"

		elif [ $response == "203" ] ; then

			STATUS="Não-autorizado"

		elif [ $response == "204" ] ; then

			STATUS="Nenhum conteúdo"

		elif [ $response == "205" ] ; then

			STATUS="Reset"

		elif [ $response == "206" ] ; then

			STATUS="Conteúdo parcial"

		elif [ $response == "207" ] ; then

			STATUS="Status Multi (WebDAV)(RFC 4918)"
		
		elif [ $response == "300" ] ; then

			STATUS="Múltipla escolha"

		elif [ $response == "301" ] ; then

			STATUS="Movido"

		elif [ $response == "302" ] ; then

			STATUS="Encontrado"

		elif [ $response == "304" ] ; then

			STATUS="Não modificado"

		elif [ $response == "305" ] ; then

			STATUS="Use Proxy"

		elif [ $response == "306" ] ; then

			STATUS="Proxy Switch"

		elif [ $response == "307" ] ; then

			STATUS="Redirecionamento temporário"

		elif [ $response == "400" ] ; then

			STATUS="Requisição inválida"

		elif [ $response == "401" ] ; then

			STATUS="Não autorizado"

		elif [ $response == "402" ] ; then

			STATUS="Pagamento necessário"

		elif [ $response == "403" ] ; then

			STATUS="Proibido"

		elif [ $response == "404" ] ; then

			STATUS="Não encontrado"

		elif [ $response == "405" ] ; then

			STATUS="Método não permitido"
		
		elif [ $response == "406" ] ; then
		
			STATUS="Não aceitável"

		elif [ $response == "407" ] ; then

			STATUS="Autenticação de proxy necessária"

		elif [ $response == "408" ] ; then

			STATUS="Tempo de requisição esgotou"

		elif [ $response == "409" ] ; then

			STATUS="Conflito"

		elif [ $response == "410" ] ; then

			STATUS="Gone"

		elif [ $response == "411" ] ; then

			STATUS="Comprimento necessário"

		elif [ $response == "412" ] ; then

			STATUS="Pré-condição falhou"

		elif [ $response == "413" ] ; then

			STATUS="Entidade de solicitação muito grande"

		elif [ $response == "414" ] ; then

			STATUS="Pedido-URI muito grande"

		elif [ $response == "415" ] ; then

			STATUS="Tipo de mídia não suportado"

		elif [ $response == "416" ] ; then

			STATUS="Solicitada de faixa não satisfatória"

		elif [ $response == "417" ] ; then

			STATUS="Falha na expectativa"

		elif [ $response == "418" ] ; then

			STATUS="Eu sou um bule de chá"

		elif [ $response == "422" ] ; then

			STATUS="Entidade improcessável (WebDAV)(RFC 4918)"

		elif [ $response == "423" ] ; then

			STATUS="Fechado (WebDAV)(RFC 4918)"

		elif [ $response == "424" ] ; then

			STATUS="Falha de dependência (WebDAV)(RFC 4918)"

		elif [ $response == "425" ] ; then

			STATUS="Coleção não ordenada"

		elif [ $response == "426" ] ; then

			STATUS="Upgrade obrigatório (RFC 2817)"

		elif [ $response == "450" ] ; then

			STATUS="Bloqueados pelo controle de pais do windows"

		elif [ $response == "499" ] ; then

			STATUS="Cliente fechou pedido"

		elif [ $response == "500" ] ; then

			STATUS="Erro interno do servidor"
		
		elif [ $response == "501" ] ; then

			STATUS="Não implementado"
	
		elif [ $response == "502" ] ; then

			STATUS="Bad Gateway"
		
		elif [ $response == "503" ] ; then

			STATUS="Serviço indisponível"

		elif [ $response == "504" ] ; then

			STATUS="Gateway Timeout"

		elif [ $response == "505" ] ; then

			STATUS="Versão HTTP não suportada"
	
		fi

		DATE=$(date +%s%3N)
		
		echo "$response;$STATUS;$DATE;$2"	
	
	elif [ -z $2 ] ; then

		echo "Wrong usage of command, WebChk.sh -h [HOST]"

	fi

fi
