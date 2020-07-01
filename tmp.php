<?php
// Create a temporary file in the temporary 
// files directory using sys_get_temp_dir()

function write_tmp_file($content1, $content2){
	$temp_file = tempnam(sys_get_temp_dir(), 'Tux');
	$fp = fopen($temp_file,"w");
	fwrite($fp,$content1."\n");
	fwrite($fp,$content2);
	fclose($fp);
	return $temp_file;
	#echo $temp_file;
}
?>
