$(document).ready(function(){
    $('#mindmap-new').on('show', function() {
        $('#id_root_component_pos_left', this).attr('value', parseInt($(window).width() / 2 - 50));
        $('#id_root_component_pos_top', this).attr('value', parseInt($(window).height() / 2 - 9));
    });
});