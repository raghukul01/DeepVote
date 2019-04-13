<?php
if ($_GET['run']) {
  shell_exec("/var/www/html/local/script.sh");
}
?>
<html>
<!-- This link will add ?run=true to your URL, myfilename.php?run=true -->
<a href="?run=true">Fetch Polls</a>
<br>
<a href="list.html">See all Polls</a>
</html>
