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

update_variable = (id, val) ->
	variable = $('#'+id)
	variable.children('.tagBot').html(val)

create_scope_groups = (scp, id) ->
	l = $('.var').length
	max = 0
	for i in [0..(l-1)]
		a = $('#'+scp+' .var')[i]
		h = parseInt($(a).css('margin-bottom'))+parseInt($(a).css('height'))+parseInt($(a).css('margin-top'))+parseInt($(a).css('top'))+30
		console.log(($(a).css('margin-bottom')))
		if (h > max)
			max = h
	h2=(parseInt($('#'+scp).css('height')) - max)
	$('#'+scp).append('<div id="'+id+'"></div>')
	$('#'+id).css('width','100%')
	$('#'+id).css('height', h2+'px')
	$('#'+id).css('border', 'solid 1px black')
	$('#'+id).css('border-radius', '2%')
	$('#'+id).css('display', 'flex')
	$('#'+id).css('flex-wrap', 'wrap')
	$('#'+id).css('margin', '5px')

delete_scope_groups = (id) ->
	$('#'+id).remove()

$(->define_variable('int', 'global', 'a', 32, 'global_a'))
$(->define_variable('int', 'global', 'b', 32, 'global_b'))
$(->update_variable('global_a', 69))
$(->setTimeout((->create_scope_groups('global','global_15')),1000))


add = ->
    define_variable($('#getT').val(), $('#getS').val(), $('#getN').val(), $('#getV').val(), $('#getI').val())
