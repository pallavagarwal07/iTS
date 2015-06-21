this.resize_list = []

define_variable = (type, scp, name, val, id) ->
    scope = $('#'+scp+" .scp")
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

create_scope = (scp, id) ->
	l = $('.var').length
	$('#'+scp).append('<div id="'+id+'" class="scope"></div>')
	$('#'+id).append('<div class="banner">'+id+'</div>')
	$('#'+id).append('<div class="scp"></div>')
	$('#'+id).css('border', 'solid 1px black')
	$('#'+id).css('border-radius', '10px')

delete_scope = (id) ->
	$('#'+id).remove()