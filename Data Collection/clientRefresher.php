<?php
	extract($_GET);
	$host = 'localhost';
	$username = 'root';
	$password = '';
	mysql_connect($host, $username, $password) or die(mysql_error());
	mysql_select_db("Chatbot") or die(mysql_error());
	$query = "SELECT * FROM personality_replies WHERE userId=$userId and acknowledgeStatus=0";
	($queryop = mysql_query($query)) or die(mysql_error());
	$arr = array();
	$flag = false;
	while($row = mysql_fetch_assoc($queryop)) {
		$flag = true;
		$query1 = "UPDATE personality_replies set acknowledgeStatus=1 WHERE userId=".$row["userId"]." and msgId=".$row["msgId"];
		($queryop1 = mysql_query($query1)) or die(mysql_error());
		$arr[$row["userId"].",".$row["msgId"]] = $row["reply"];
	}
	if($flag)
		echo json_encode($arr);
	else
		echo "Nothing";
?>
