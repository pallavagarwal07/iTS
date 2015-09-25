this.resize_list = []
cmd_number = 0
cmd = []
prev_out = ""
marker = null
curRunning = null
time = 1000
scale = 1
input_processed = 0
prev_scale = 1
speed =
    0  : 5000
    1  : 10
    2  : 7
    3  : 4
    4  : 2
    5  : 1
    6  : 0.5
    7  : 0.25
    8  : 0.14
    9  : 0.1
    10 : 0

$(->
    $('#slider').slider(
        animate: true
        value: 5
        max: 10
        change: -> (scale = speed[$('#slider').slider("value")])
    )
)


setCodeFromURL = ->
    code = window.atob(getQuery('code'))
    inp  = window.atob(getQuery('input'))
    $('#stdin').text(inp)
    editor.setValue(code)


$(setCodeFromURL)


getQuery = (variable) ->
    query = window.location.search.substring(1)
    vars = query.split('&')
    for term in vars
        pair = term.split('=')
        if pair[0] == variable
            return pair[1]
    return ''


$(->$('#pause').change(->
    if $('#pause').prop('checked') == true
        $('#pause_label span').text("Play")
        $('#slider').slider("disable")
        $('#submit-btn').prop('disabled', false)
        $('#submit-btn').text('Step forward >>')
        prev_scale = scale
        window.clearTimeout(curRunning)
    else
        $('#submit-btn').prop('disabled', true)
        $('#pause_label span').text("Pause")
        $('#slider').slider("enable")
        scale = prev_scale
        window.clearTimeout(curRunning)
        simulate()
))

pause_simulation = ->
    $('#pause').prop('checked', true)
    $('#pause').button('refresh')
    $('#pause_label span').text("Play")
    $('#slider').slider("disable")
    $('#submit-btn').prop('disabled', false)
    $('#submit-btn').text('Step forward >>')
    prev_scale = scale
    window.clearTimeout(curRunning)


$(->
    $('#stdout').text("")
    $('#stdin_highlight').hide()
    $('#pause_label').css('height', $('#reset').css('height'))
)


user_error = (b64error) ->
    error = window.atob(b64error)
    $('#modal-msg').html(error)
    $('#myModal').modal('show')
    scale = 5000


stdout_print = (b64str) ->
    $('#stdout').css('background-color', '#CE6')
    setTimeout(->
        $('#stdout').css('background-color', '#FFF')
    , 40)
    stdoutStr = window.atob(b64str)
    final_out = $('#stdout').val()+stdoutStr
    $('#stdout').val(final_out)
    $('#stdout').animate(
        scrollTop: $('#stdout')[0].scrollHeight - $('#stdout').height()
    , 500)
    time = 1000


stdin_write = (n)->
    s = $('#stdin_highlight').html()
    if input_processed == 0
        s = "<samp><span id='highlight_input'>" + s.substr(6)
        s = s.substr(0, n + 33) + "</span>" + s.substr(n + 33)
    else
        s = s.replace("</span>", "")
        s = s.substr(0, input_processed + n + 33) + "</span>" + s.substr(input_processed + n + 33)
    input_processed += n
    $('#stdin_highlight').html(s)
    $('#stdin_highlight').animate(
        scrollTop: (($('#highlight_input').text().match(/\n/g)||[]).length)*parseInt($('#highlight_input').css('line-height'))
    , 500)
    time = 1000


define_variable = (type, scp, name, val, mem) ->
    id = scp+"-"+name
    panel = '<div class="panel panel-success" id="'+id+'" style="display:none;"><div class="panel-heading">
        <h3 class="panel-title">'+name+"\t|\t"+type+'</h3></div>
        <div id="'+id+'-body" class="panel-body '+mem+'-mem">'+val+'</div></div>'
    $('#'+scp+'-body').append(panel)
    $('#'+id).show(400)
    time = 1000


highlight_line = (line_num) ->
    console.log(marker)
    editor.getSession().removeMarker(marker)
    require(["ace/range"], (range) ->
        marker = editor.getSession().addMarker(new
            range.Range(line_num, 0, line_num, 2000), "highlight-line", "line", true)
    )
    time = 10

red = "red"
green = "green"
custom_highlight = (line_num, color) ->
    console.log(marker)
    editor.getSession().removeMarker(marker)
    require(["ace/range"], (range) ->
    if color == green
        marker = editor.getSession().addMarker(new
            range.Range(line_num, 0, line_num, 2000), "highlight-green", "line", true)
    else if color == red
        marker = editor.getSession().addMarker(new
            range.Range(line_num, 0, line_num, 2000), "highlight-red", "line", true)
    )
    time = 400


reset = ->
    # Actions if paused
    $('#pause_label span').text("Pause")
    $('#slider').slider("enable")
    scale = prev_scale

    # Reset Submit Button
    $('#submit-btn').prop('disabled', false)
    $('#submit-btn').text('Submit')

    # Button color change
    $('#reset').switchClass('btn-primary', 'btn-success')
    $('#reset').text('Success')
    window.setTimeout(->
        $('#reset').switchClass('btn-success', 'btn-primary', 700)
        $('#reset').text('Reset')
    , 2000)

    # Reset simulation
    cmd_number = 0
    editor.getSession().removeMarker(marker)
    window.clearTimeout(curRunning)

    # Enable STDin, STDout, editor etc.
    $('#stdin').prop('disabled', false)
    $('#stdin').show()
    $('#stdin_highlight').hide()
    editor.setReadOnly(false)
    $('#stdout').val(prev_out)

    # Clear simulation
    delete_scope('global')

$(reset)


update_variable = (id, val) ->
    variable = $('#'+id+'-body')
    variable.text(val)
    variable = $('.'+id+'-mem')
    variable.text(val)
    time = 1000

create_scope = (scp, id) ->
    l = $('.var').length
    panel = '<div class="panel panel-warning" id="'+id+'" style="display:none;">
        <div class="panel-heading"><h3 class="panel-title">'+id+'</h3></div>
        <div class="panel-body" id="'+id+'-body"></div></div>'
    $('#'+scp+'-body').append(panel)
    $('#'+id).show(400)
    time = 1000

delete_scope = (id) ->
    $('#'+id).hide('slow', -> $('#'+id).remove())
    time = 1000

$('#ace1').ready(->
    editor.resize(true)
    editor.setTheme("ace/theme/dawn")
    editor.getSession().setMode("ace/mode/c_cpp")
    editor.setAutoScrollEditorIntoView(true)
    editor.setHighlightActiveLine(true)
    editor.setShowPrintMargin(false)
    editor.setOptions(
        fontFamily: "Source Code Pro", "monospace"
    )
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
        window.setTimeout(->
            cmd_number = 0
            editor.getSession().removeMarker(marker)
            $('#stdin').prop('disabled', false)
            editor.setReadOnly(false)
            $('#stdin').show()
            $('#stdin_highlight').hide()
        , time*scale)
    else
        curRunning = window.setTimeout(simulate, time*scale)


step_forward = ->
    flag = 1
    while 1
        exe = cmd[cmd_number]
        cmd_number += 1
        if cmd_number == cmd.length
            cmd_number = 0
            window.setTimeout(->
                editor.getSession().removeMarker(marker)
                $('#stdin').prop('disabled', false)
                editor.setReadOnly(false)
                $('#stdin').show()
                $('#stdin_highlight').hide()
            , time*scale)
            break

        if flag and exe.indexOf('highlight_line') == 0
            flag = 0
            console.log('Evaluating ' + exe)
            eval(exe)
        else
            console.log("Here " + exe)
            if exe.indexOf('highlight_line') == -1
                console.log('Evaluating ' + exe)
                eval(exe)
            else
                cmd_number -= 1
                break


start_sim = (obj) ->
    cmd_number = 0
    if obj.gcc_error
        createAlert("GCC ERROR: ", obj.gcc_error, "danger")
        editor.setReadOnly(false)
    else
        if obj.gcc_warning
            createAlert("GCC Warning: ", obj.gcc_warning, "warning")
        if obj.gcc_out == obj.its_out
            createAlert("", "Simulation made successfully!", "success")
            cmd = obj.its_cmd.split("\n")
            console.log(cmd)
            simulate()
        else
            createAlert("", "GCC output, and the interpreter output were not the same.",\
                "warning")
            cmd = obj.its_cmd.split("\n")
            console.log(cmd)
            simulate()


compile = ->
    if $('#submit-btn').text().trim() == 'Step forward >>'
        step_forward()
    if $('#submit-btn').text().trim() == 'Submit'
        clearAll()
        $('#submit-btn').text('Loading...')
        $('#submit-btn').addClass('active')
        $('#stdin').prop('disabled', true)
        editor.setReadOnly(true)

        code = editor.getValue()
        input = $('#stdin').val()
        $('#stdin').hide()
        $('#stdin_highlight').show()
        $('#stdin_highlight').height($('#stdout').height())
        $('#stdin_highlight').html("<samp>"+input+"</samp>")
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
                prev_out = obj.gcc_out
                console.log(obj)
                start_sim(obj)
        )

$(->$("#pause").button())
        #primary: "ui-icon-play"
        #secondary: "ui-icon-pause"
      #}))

#$("#pause").button(
      #text: false,
      #icons:
        #primary: "ui-icon-play"
    #).click(->
        #if $(this).text() == "play"
            #options = label: "pause", icons: primary: "ui-icon-pause"
        #else
            #options = label: "play", icons: primary: "ui-icon-play"
        #$(this).button("option", options)
    #)global
