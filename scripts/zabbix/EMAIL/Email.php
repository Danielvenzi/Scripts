<?php

#$data = date("Y-m-d H:i:s");
#$data = date_default_timezone_set()
#$msg = "Executado tempopesquisa no DEV ".$data;

$email = mail("gomesvenzi@gmail.com.br","Executado TempoPesquisa","Banana");

print_r($email);

?>
