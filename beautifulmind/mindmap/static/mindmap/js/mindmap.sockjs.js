(function($) {
    $.mindmapSockjs = function() {
        var self = this;
        self.socket = new SockJS(bm_globals.mindmaptornado.server);

        self.socket.onopen = function() {
            // fetch and init map
            $('#mindmap-map').mindmapMap();

            // register client as map participant if we are currently on a map
            var map_pk = $('#mindmap-map').attr('data-map-pk');
            if(map_pk) {
                self.send('register_myself_as_map_participant', {
                    map_pk: map_pk
                });
            }
        };

        self.socket.onmessage = function(e) {
            var client_methods = {
                'add_component': function(data) {
                    data.left = data.pos_left;
                    data.top = data.pos_top;
                    data.pk = data.component_pk;
                    $('#mindmap-map').data('mindmapMap').addComponent(data);
                },

                'update_component_pos': function(data) {
                    var component = $('.component[data-component-pk="'+data.component_pk+'"]:first');
                    component.css({left: data.pos_left, top: data.pos_top});
                    jsPlumb.repaint(component);
                },

                'update_component_title': function(data) {
                    var component = $('.component[data-component-pk="'+data.component_pk+'"]:first');
                    $('.component-title:first', component).attr('value', data.title);
                },

                'add_components_offset_except_one': function(data) {
                    $('.component:not([data-component-pk="'+data.except_component_pk+'"])').each(function(){
                        var component = $(this);
                        var pos = component.position();
                        component.css({
                            left: pos.left + data.offset_left,
                            top: pos.top + data.offset_top
                        });
                    });
                    jsPlumb.repaintEverything();
                }
            }

            var data = $.parseJSON(e.data);
            if (!data.hasOwnProperty('method'))
                return;

            if (!client_methods.hasOwnProperty(data.method))
                return;

            client_methods[data.method](data);
        };

        self.socket.onclose = function() {
            this.socket = null;
        };

        self.send = function(method, data) {
            data.method = method;
            self.socket.send(JSON.stringify(data))
        };

        return self;
    }();
})(jQuery);
