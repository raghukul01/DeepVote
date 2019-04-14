<?php 
    $pollno=$_POST['pollno']
    $fileName = __FILE__;
    $newFile = substr($fileName, 0, -10);
    shell_exec("python3 reveal.py ".$pollno) 
?>

