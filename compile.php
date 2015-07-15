<?php
    $code = base64_decode($_GET["code"]);
    $mycode = fopen("code.c", "w");
    fwrite($mycode, $code);
    fclose($mycode);
    $input = base64_decode($_GET["input"]);
    $myinput = fopen("input.in", "w");
    fwrite($myinput, $input);
    fclose($myinput);
    exec('./iTS/its -c code.c -i input.in -o output.txt');
    echo file_get_contents('output.txt');
?>
