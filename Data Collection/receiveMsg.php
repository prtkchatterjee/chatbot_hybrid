<?php
	extract($_POST);
	$host = 'localhost';
	$username = 'root';
	$password = '';
	mysql_connect($host, $username, $password) or die(mysql_error());
	mysql_select_db("Chatbot") or die(mysql_error());
	$query = "SELECT MAX(msgId) AS msgId FROM personality_inputs WHERE userId=$userId";
	($queryop = mysql_query($query)) or die(mysql_error());
	if($row = mysql_fetch_assoc($queryop)) {
		$msgId = $row["msgId"]+1;
	}
	else
		$msgId = 1;
	$query = "INSERT INTO personality_inputs VALUES ($userId,$msgId,'$msg',0)";
	($queryop = mysql_query($query)) or die(mysql_error());
?>
