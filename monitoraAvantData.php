<?php
//Autor: Rodrigo Vilanova
//AvantData
//Data: 03/05/2017
//versão: 0.1

error_reporting(E_ALL | E_STRICT);
ini_set('display_errors', 'off');

//Monitora o cluster a cada n segundos e armazena o valor no elastic
// echo "\r\n";
// echo "\r\n";

if (sizeof($argv) == 1){
	echo "Está faltando o parâmentro de intervalor de tempo para monitoração!\r\n";
	exit();
}
// echo $argv[1]."\r\n";

//conexão com o Elasticsearch
require 'vendor/autoload.php';

//Fazer função que busca essa informação do banco de dados
$avantdata =
    [
        "192.168.102.5"
    ];   

$avantcluster = Elasticsearch\ClientBuilder::create()
    ->setHosts($avantdata)
    ->build();
	// echo "<pre>";
	// print_r($avantcluster);
	// echo "</pre>";

	//Enumera todos os nos do cluster em um array com o ID de cada um.
	$listaIdNos = array();
	function criaListaIdNos($campo, $chave){
		global $listaIdNos;
		// echo $chave."\r\n";
		array_push($listaIdNos, $chave);
	}

	
while (true){
	
	//procura pelo indice monitora no elastic, caso não encontre cria o indice
	$avantindex = array(                                                            //testa a existência do índice avantdata.
			'index'=>'monitora'
	);

	$existe = $avantcluster->indices()->exists($avantindex);
	//echo $existe;

	if(!($existe)) 
	{
		$createesponse = $avantcluster->indices()->create($avantindex);
	}

	$configtype = array(                                                            //testa a existência do tipo alertas.
		'index' => 'monitora',
		'type'  => 'status'
	 );

	//hora de execução do monitora
	$horaMonitoracao = date("Y/m/d H:i:s");
	// echo $horaMonitoracao;

	//alertas que devem ser salvos a cada n segundos.
	 /*
	GET _nodes/stats
	GET _cluster/health
	GET avantdata/_stats
	
	GET _cluster/state
	GET _nodes
	*/

	// $nos = $avantcluster->nodes();
	// print_r ($nos);


	//======================================================
	//indexa o nodes/stats
	$infoNos = $avantcluster->nodes()->stats();
	//print_r($infoNos);
	// echo (gettype($infoNos)."\r\n");

	$totalNos = $infoNos['_nodes']['total'];
	
	//envia os ids dos nos para o array global $listaIdNos
	array_walk($infoNos['nodes'], 'criaListaIdNos');
	
		
	for ($i=1; $i<=$totalNos; $i++){
		
		$idNoAtual = $listaIdNos[$i-1];
		// Indexa os documentos no indice monitora
		$parametroSalvaResultadoMonitora = [
			'index' => 'monitora',
			'type' => 'nodesStats',
			'body' => [ 
						'horaMonitoracao' => $horaMonitoracao,
						'cluster_name' => $infoNos['cluster_name'],
						'idNo' => $idNoAtual,
						'name' => $infoNos['nodes'][$idNoAtual]['name'],
						'dados' => $infoNos['nodes'][$idNoAtual]
						
						
			]
		];

		// print_r ($parametroSalvaResultadoMonitora);

		// Indexa resultado da execução do alerta no Elastic
		$respostaIndexacao = $avantcluster->index($parametroSalvaResultadoMonitora);
		// echo "\r\nResultado da indexação: \r\n";
		// print_r ($respostaIndexacao);

	}
	//======================================================
	//indexa o cluster/health
	$clusterHealth = $avantcluster->cluster()->health();
	// print_r($clusterHealth);
	// echo (gettype($clusterHealth)."\r\n");
	//Indexa os documentos no indice monitora
	$parametroSalvaResultadoMonitora = [
		'index' => 'monitora',
		'type' => 'clusterHealth',
		'body' => [ 
					'horaMonitoracao' => $horaMonitoracao,
					$clusterHealth
		]
	];

	// print_r ($parametroSalvaResultadoMonitora);

	//Indexa resultado da execução do alerta no Elastic
	$respostaIndexacao = $avantcluster->index($parametroSalvaResultadoMonitora);
	// echo "\r\nResultado da indexação: \r\n";
	// print_r ($respostaIndexacao);

	//======================================================
	//indexa o avantdata/stats
	$params['index'] = 'avantdata';
	$avantdataStats = $avantcluster->indices()->stats($params);
	// print_r($avantdataStats);
	// echo (gettype($avantdataStats)."\r\n");
	//Indexa os documentos no indice monitora
	$parametroSalvaResultadoMonitora = [
		'index' => 'monitora',
		'type' => $params['index']."Stats",
		'body' => [ 
					'horaMonitoracao' => $horaMonitoracao,
					$avantdataStats
		]
	];

	// print_r ($parametroSalvaResultadoMonitora);

	//Indexa resultado da execução do alerta no Elastic
	$respostaIndexacao = $avantcluster->index($parametroSalvaResultadoMonitora);
	// echo "\r\nResultado da indexação: \r\n";
	// print_r ($respostaIndexacao);






	//======================================================
	//indexa o cluster/state
	// $clusterState = $avantcluster->cluster()->state();
	// print_r($clusterState);
	// echo (gettype($clusterState)."\r\n");
	//Indexa os documentos no indice monitora
	// $parametroSalvaResultadoMonitora = [
		// 'index' => 'monitora',
		// 'type' => 'clusterState',
		// 'body' => [ 
					// 'horaMonitoracao' => $horaMonitoracao,
					// $clusterState,
		// ]
	// ];

	// print_r ($parametroSalvaResultadoMonitora);

	//Indexa resultado da execução do alerta no Elastic
	// $respostaIndexacao = $avantcluster->index($parametroSalvaResultadoMonitora);
	// echo "\r\nResultado da indexação: \r\n";
	// print_r ($respostaIndexacao);

	// echo "resultados salvos em: ".$argv[1]."segundos";

	
	sleep($argv[1]);
}
