<?php
    $vote = $_POST['vote'];
    $pubkey = $_POST['pubkey'];
    $privkey = $_POST['prikey'];
    $pollno = $_POST['pollno'];
  if(empty($vote)||empty($pubkey)||empty($privkey)||empty($pollno))
  {
    echo("Incomplete Voting. Please Revote.");
  }
  else
  {
    $nonce = substr(md5(mt_rand()), 0, 7);
    $data = $vote + $nonce;
    $datahash = hash("sha256", $data);
    file_put_contents("nonce.txt", $nonce);
    file_put_contents("datahash.txt", $datahash);
    file_put_contents("pubkey.txt", $pubkey);
    file_put_contents("privkey.txt", $privkey);
    file_put_contents("pollno.txt", $pollno);

    shell_exec("python3 linkable_ring_signature.py");


  }
?>
