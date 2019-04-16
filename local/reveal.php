<?php 
    $pollno=$_POST['pollno'];
    $fileName = __FILE__;
    $newFile = substr($fileName, 0, -10);
    shell_exec("python3 reveal.py ".$pollno);
    echo "Your vote will be revealed it the current time is greater than the end of voting time and less than the end of reveal period.";
?>

