<?php
	set_time_limit(0);
	extract($_POST);
	chdir('chatbot1_v4');
	$f = fopen('driver_inp.txt','w');
	fwrite($f,$input);
	fclose($f);

	$size1 = filesize("driver_op.txt");
	while(true) {
		sleep(2);
		clearstatcache();
		$size2 = filesize("driver_op.txt");
		if($size2 == 0)
			continue;
		if($size1 != $size2)
			$size1 = $size2;
		else
			break;
	}
	$f1 = fopen('driver_op.txt','r');
	clearstatcache();
	$output = fread($f1,filesize("driver_op.txt"));
	fclose($f1);
	$f1 = fopen('driver_op.txt','w');
	fwrite($f,"");
	fclose($f1);
	echo($output);
	
?>
