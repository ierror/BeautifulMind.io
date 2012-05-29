(function($) {
    $.fn.mindmapSockjs = function() {
        var self = this;
        console.log('init');

        self.socket = new SockJS(bm_globals.mindmaptornado.server);

        self.socket.onopen = function() {
            // register client as map participant if we are on a currently on a mindmap
            var map_pk = $('#mindmap-map').attr('data-map-pk');
            if(map_pk) {
                self.send('register_myself_as_map_participant', {
                    map_pk: map_pk
                });
            }
        };

        self.socket.onmessage = function(e) {
            var data = $.parseJSON(e.data);
            var component = $('.component[data-component-pk="'+data.component_pk+'"]:first');
            $(component).css({left: data.pos.left, top: data.pos.top});
            jsPlumb.repaint($(component));
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
