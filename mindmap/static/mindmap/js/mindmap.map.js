(function($) {
    $.fn.mindmapMap = function() {
        var self = this;

        self.init = function() {
            $.ajax({
                url: self.attr('data-components-url'),
                type: 'POST',
                data: {},
                cache: false,
                success: function (data) {
                    $($.parseJSON(data)).each(function(){
                        $().mindmapMapComponent({
                            id: this.pk,
                            title: this.fields.title,
                            container: self,
                            left: this.fields.pos_left,
                            top: this.fields.pos_top,
                            parent_id: this.fields.parent,
                            level: this.fields.level
                        });
                    });
                },
                error: function() {

                }
            });
        }

        jsPlumb.ready(function () {
            jsPlumb.DefaultDragOptions = {
                cursor:"pointer", zIndex:2000
            };

            jsPlumb.importDefaults({
                DragOptions:{ cursor:'wait', zIndex:20 },
                Connector:[ "Bezier", { curviness:25 } ]
            });

            var connectorStrokeColor = "rgba(50, 50, 200, 1)",
                connectorHighlightStrokeColor = "rgba(180, 180, 200, 1)",
                hoverPaintStyle = { strokeStyle:"#7ec3d9" };

            self.init();
        });

    };
})(jQuery);