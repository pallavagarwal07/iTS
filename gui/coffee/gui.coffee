define_variable = (type, scp, name, val, id) ->
    scope = $('#'+scp)
    scope.append('<div id=\''+id+'\'></div>')
    variable = $('#'+id)
    variable.append('<div class=\'tagTop\'></div>')
    variable.append('<div class=\'tagBot\'></div>')
    variable.children('.tagBot').html(val)
    variable.children('.tagTop').append('<div class="name"></div>')
    variable.children('.tagTop').append('<div class="type"></div>')
    variable.children('.tagTop').children('.name').html(name)
    variable.children('.tagTop').children('.type').html(type)
    variable.addClass('newborn')
    setTimeout((->variable.addClass('var').removeClass('newborn')), 10)

$(->define_variable('int', 'global', 'a', 32, 'global_a'))
$(->define_variable('int', 'global', 'b', 32, 'global_b'))

add = ->
    define_variable($('#getT').val(), $('#getS').val(), $('#getN').val(), $('#getV').val(), $('#getI').val())
