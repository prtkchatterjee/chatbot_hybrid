<?php
	extract($_POST);
	chdir('chatbot1_v4');
	$f = fopen('driver_inp.txt','w');
	fwrite($f,$input);

	sleep(35);

	$size1 = filesize("driver_op.txt");
	while(true) {
		sleep(2);
		$size2 = filesize("driver_op.txt");
		if($size1 != $size2)
			$size1 = $size2;
		else
			break;
	}
	$f1 = fopen('driver_op.txt','r');
	$output = fread($f1,filesize("driver_op.txt"));
	fclose($f1);
	echo($output);
?>
