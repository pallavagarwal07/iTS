
$('#ace1').ready(function(){
    editor = ace.edit("editor");
    editor.resize(true);
    editor.setTheme("ace/theme/tomorrow_night_bright");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.setReadOnly(true);
    editor.setAutoScrollEditorIntoView(true);
    editor.setHighlightActiveLine(true);
    str =  editor.getValue();
    k = hljs.highlightAuto(str);
});

function compile(){
    code = editor.getValue();
    input = $('#stdin').val();
    code = window.btoa(code);
    input = window.btoa(input);
    $.get("test.php", {
        "code": code,
        "input": input
    }, function(obj){
        alert(obj);
    });
}
