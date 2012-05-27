(function($) {
    $.fn.mindmapSockjs = function() {
        var self = this;
        console.log('init');

        self.socket = new SockJS(bm_globals.mindmaptornado_server);

        self.socket.onopen = function () {
            //update_ui();
        };

        self.socket.onmessage = function (e) {
            var data = $.parseJSON(e.data);
            console.log({left: data.pos.left, top: data.pos.top});
            $('#makeunique').css({left: data.pos.left, top: data.pos.top});
            jsPlumb.repaint($('#makeunique'));
        };

        self.socket.onclose = function () {
            this.socket = null;
        };

        self.send = function(payload) {
            self.socket.send(payload);
        }

        return self;
    }();
})(jQuery);
