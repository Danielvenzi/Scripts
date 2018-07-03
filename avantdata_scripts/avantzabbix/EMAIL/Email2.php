<?php
$to      = 'gomesvenzi@gmail.com';
$subject = 'the subject';
$message = 'To criando o email certinha';
$headers = 'From: gomesvenzi@gmail.com' . "\r\n" .
    'Reply-To: gomesvenzi@gmail.com' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();

mail($to, $subject, $message, $headers);
?>
