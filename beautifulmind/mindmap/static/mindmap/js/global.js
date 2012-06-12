$(document).ready(function(){
    $('#mindmap-new').on('initiated', function() {
        // write component pos based on window size
        $('#id_root_component_pos_left', this).attr('value', parseInt($(window).width() / 2 - 50));
        $('#id_root_component_pos_top', this).attr('value', parseInt($(window).height() / 2 - 9));

        // remove focus from selected component
        $('.component-selected').each(function(){
            $(this).data('mindmapMapComponent').deselect();
        })
    });
});