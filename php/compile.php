<?php
    $randkey = md5(microtime() . rand());
    $code = base64_decode($_GET["code"]);
    $mycode = fopen($randkey.".c", "w");
    fwrite($mycode, $code);
    fclose($mycode);
    $input = base64_decode($_GET["input"]);
    $myinput = fopen($randkey.".in", "w");
    fwrite($myinput, $input);
    fclose($myinput);
    exec('../iTS/its -c '.$randkey.'.c -i '.$randkey.'.in -o '.$randkey.'.txt');
    echo file_get_contents($randkey.'.txt');
    exec('rm '.$randkey.'.c '.$randkey.'.txt '.$randkey.'.in');
?>
