<?php
    $randkey = md5(microtime() . rand());
    $code = base64_decode($_GET["code"]);
    $mycode = fopen($randkey.".c", "w");
    fwrite($mycode, $code);
    fclose($mycode);
    // c File written


    $input = base64_decode($_GET["input"]);
    $myinput = fopen($randkey.".in", "w");
    fwrite($myinput, $input);
    fclose($myinput);
    // Input File written


    $ret_val = array("gcc_error"=>"", "gcc_warning"=>"",
        "gcc_out"=>"", "out_ret"=>"", "its_out"=>"", "its_cmd"=>"");

    exec('gcc -Wall -o '.$randkey.'.out '.$randkey.'.c 2>&1', $gcc_stdout, $return_code);

    if($return_code != 0) {
        $ret_val["gcc_error"] = str_replace($randkey, 'code', $gcc_stdout);
    } else {

        if(sizeof($gcc_stdout) != 0) {
            $ret_val["gcc_warning"] = str_replace($randkey, 'code', implode("\n", $gcc_stdout));
        }

        exec('timeout --kill-after=2s 2s ./'.$randkey.'.out <'.$randkey.'.in 2>&1 1>'.$randkey.'.key', $gcc_out, $out_ret);

        if($out_ret == 124 || $out_ret == 137){
            $ret_val["gcc_out"] = "Time Limit Exceeded in GCC executable..";
        } else {
            $ret_val["gcc_out"] = file_get_contents($randkey.'.key');
        }
        $ret_val["out_ret"] = $out_ret;
    }
    // GCC outputs end here



    exec('../iTS/its -c '.$randkey.'.c -i '.$randkey.'.in -o '.$randkey.'.txt -e '.$randkey.'.its');
    $ret_val['its_out'] = file_get_contents($randkey.'.txt');
    $ret_val['its_cmd'] = file_get_contents($randkey.'.its');
    echo json_encode($ret_val);
    exec('rm '.$randkey.'.c '.$randkey.'.txt '.$randkey.'.in '.$randkey.'.out '.$randkey.'.key '.$randkey.'.its');
?>
