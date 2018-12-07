Scripts para atualização via WEB do AvantData.

Os scripts existentes são:

	serverCipher.sh - Cifra o conteúdo do repositório AvantData e cria um tar.gz dentro do repositório. Dentro do script existe uma variável que determina o caminho do repositório no servidor.
			  Se o caminho for diferente de /var/www/html será necessário mudar a variável.
	clientSet.sh    - Cria a estrutura de armazenamento no cliente, tal estrutura comporta a mais nova versão do código e a versão imediatamente anterior que estava no servidor.
	clientDownload.sh - Download da última versão do repositório AvantData. Passar como parâmetro o nome do arquivo.
	clientInstall.sh - Após o termino do download ele instala o tar.gz no sistema.
	clientUndo.sh - Desfaz a instalação da nova versão do AvantData e retorna a versão instalada anteriormente.
