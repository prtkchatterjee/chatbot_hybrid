<?php
	extract($_POST);
	$host = 'localhost';
	$username = 'root';
	$password = '';
	mysql_connect($host, $username, $password) or die(mysql_error());
	mysql_select_db("Chatbot") or die(mysql_error());
	$query = "INSERT INTO personality_replies VALUES ($userId,$msgId,'$msg',0)";
	($queryop = mysql_query($query)) or die(mysql_error());
?>
