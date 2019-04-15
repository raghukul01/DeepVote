<?php
if ($_GET['run']) {
  $fileName = __FILE__;
  $newFile = substr($fileName, 0, -9);
  shell_exec($newFile . "script.sh");
}
?>
<html>
<head><link href="../poll.css" rel="stylesheet"></head>
<body ><div id="main" style="text-align:center;">
<div id="first" >
<!-- This link will add ?run=true to your URL, myfilename.php?run=true -->
<br><br><br>
<a href="?run=true" >Fetch Polls</a>
<br><br><br><br>
<a href="list.html">See all Polls</a>
<br><br><br><br>
<!-- <a href="listR.html">See all Reveal Pages</a>
<br> -->
<a href="keyGen.php">Generate Key Pair</a>
<br><br><br><br>
</div></div>
<body>
</html>
