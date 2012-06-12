$(document).ready(function(){
    $('.modal-form').modalForm();

    $('.simple-tooltip').tooltip();

    // make django csrf workable with ajax posts
    $.ajaxSetup({
        beforeSend:function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

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
});