<?php
    $vote = $_POST['vote'];
    $pollno = $_POST['pollno'];
  if(is_null($vote))
  {
    echo("Incomplete Voting. Please Revote.");
  }
  else
  {
      $nonce = substr(md5(mt_rand()), 0, 31);





    shell_exec("python3 hash.py ".$vote." ".$nonce." ".$pollno); 
    /* $data = $nonce.$vote; */
    /* echo $nonce,"\n"; */
    /* echo $vote,"\n"; */
    /* echo $data,"\n"; */
    /* $datahash = hash("sha256", $data); */
    file_put_contents($pollno."vote.txt", $vote);
    file_put_contents($pollno."nonce.txt", $nonce);
    /* file_put_contents($pollno."datahash.txt", $datahash); */

    shell_exec("python3 linkable_ring_signature.py ".$pollno);
    echo "Your vote will be recorded subject to verification.";

  }
?>
