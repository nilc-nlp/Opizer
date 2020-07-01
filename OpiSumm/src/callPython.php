<?php
  if($_POST){
  exec('python main_web.py '.$_POST['summarizer']." ".$_POST['items']." ".$_POST['aspects'], $retorno);
  $response['corrected_sentence'] = $retorno;
  echo(json_encode($response));
  }	
  else echo('Not posting!');
  exit();
?>
