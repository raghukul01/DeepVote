<?php
if ($_GET['run']) {
  $fileName = __FILE__;
  $newFile = substr($fileName, 0, -9);
  shell_exec($newFile . "script.sh");
}
?>
<html>
<!-- This link will add ?run=true to your URL, myfilename.php?run=true -->
<a href="?run=true">Fetch Polls</a>
<br>
<a href="list.html">See all Polls</a>
<br>
<!-- <a href="listR.html">See all Reveal Pages</a>
<br> -->
<a href="keyGen.php">Generate Key Pair</a>
</html>
