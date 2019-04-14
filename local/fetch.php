<?php
if ($_GET['run']) {
  shell_exec("/home/yash/Downloads/CS731/blockchain_project/local/script.sh");
}
?>
<html>
<!-- This link will add ?run=true to your URL, myfilename.php?run=true -->
<a href="?run=true">Fetch Polls</a>
<br>
<a href="list.html">See all Polls</a>
</html>
