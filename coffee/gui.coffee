this.resize_list = []
cmd_number = 0
cmd = []

define_variable = (type, scp, name, val, id = scp+"-"+name) ->
    #scope = $('#'+scp+" .scp")
    #console.log(scope)
    #scope.append('<div id=\''+id+'\'></div>')
    #variable = $('#'+id)
    #console.log(variable)
    #variable.append('<div class=\'tagTop\'></div>')
    #variable.append('<div class=\'tagBot\'></div>')
    #variable.children('.tagBot').html(val)
    #variable.children('.tagTop').append('<div class="name"></div>')
    #variable.children('.tagTop').append('<div class="type"></div>')
    #variable.children('.tagTop').children('.name').html(name)
    #variable.children('.tagTop').children('.type').html(type)
    #variable.addClass('newborn')
    #setTimeout((->variable.addClass('var').removeClass('newborn')), 10)
    panel = '<div class="panel panel-success" id="'+id+'" style="display:none;"><div class="panel-heading">
        <h3 class="panel-title">'+name+"\t|\t"+type+'</h3></div>
        <div class="panel-body" id="'+id+'-body">'+val+'</div></div>'
    $('#'+scp+'-body').append(panel)
    $('#'+id).show(1000)


update_variable = (id, val) ->
    variable = $('#'+id+'-body')
    variable.text(val)

create_scope = (scp, id) ->
    l = $('.var').length
    panel = '<div class="panel panel-warning" id="'+id+'" style="display:none;"><div class="panel-heading">
        <h3 class="panel-title">'+id+'</h3> </div>
        <div class="panel-body" id="'+id+'-body"></div></div>'
    $('#'+scp+'-body').append(panel)
    $('#'+id).show(1000)

delete_scope = (id) ->
    $('#'+id).remove()

$('#ace1').ready(->
    editor.resize(true)
    editor.setTheme("ace/theme/dawn")
    editor.getSession().setMode("ace/mode/c_cpp")
    editor.setAutoScrollEditorIntoView(true)
    editor.setHighlightActiveLine(true)
    editor.setShowPrintMargin(false)
)

createAlert = (name, str, type) ->
    err = '<div class="alert alert-'+type+' '+'
    alert-dismissible fade in" role="alert"> <button type="button"
    class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span></button> <strong>
    '+name+'\n</strong>'+str+'</div>'
    $('#sbt-row').after(err)

clearAll = ->
    $('#stdout').val("")
    $('.alert').alert('close')


simulate = ->
    eval(cmd[cmd_number])
    cmd_number += 1
    if cmd_number == cmd.length
        cmd_number = 0
    else
        window.setTimeout(simulate, 1000)


start_sim = (obj) ->
    cmd_number = 0
    if obj.gcc_error
        createAlert("GCC ERROR: ", obj.gcc_error, "danger")
    if obj.gcc_warning
        createAlert("GCC Warning: ", obj.gcc_warning, "warning")
    if obj.gcc_out == obj.its_out
        createAlert("", "Simulation made successfully!", "success")
        $('#stdout').val(obj.gcc_out)
        cmd = obj.its_cmd.split("\n")
        console.log(cmd)
        simulate()


compile = ->
    clearAll()
    $('#submit-btn').text('Loading...')
    $('#submit-btn').addClass('active')

    code = editor.getValue()
    input = $('#stdin').val()
    code = window.btoa(code)
    input = window.btoa(input)
    $('#sbt_row .btn').button('toggle')
    $.get("php/compile.php"
        "code": code
        "input": input
    (json_text)->
        $('#submit-btn').text('Submit')
        $('#submit-btn').removeClass('active')
        obj = JSON.parse(json_text)
        start_sim(obj)
    )
