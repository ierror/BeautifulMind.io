(function($) {
    $.fn.mindmapMap = function() {
        var self = this;
        self.component_spacing = 25;

        self.init = function() {
            $.ajax({
                url: self.attr('data-components-url'),
                type: 'POST',
                data: {},
                cache: false,
                success: function (data) {
                    $($.parseJSON(data)).each(function(){
                        data = this;
                        // merge data.fields into data
                        for (var attrname in data.fields) {
                            data[attrname] = data.fields[attrname]; }
                        data.fields = undefined;

                        self.add_component(data);
                    });
                },
                error: function() {

                }
            });
        }

        self.add_component = function(data) {
            var component = $().mindmapMapComponent({
                id: data.pk,
                title: data.title,
                container: self,
                left: data.pos_left,
                top: data.pos_top,
                parent_id: data.parent,
                level: data.level
            });

            // set focus on title input
            if (data.set_focus_on_title_field) {
                $('.component-title:first', component).focus();
            }

            if (data.do_collide_check) {
                while (true) {
                    var disrupters = component.collidesWith('.component');
                    if (disrupters.length > 0) {
                        var disrupter = $(disrupters[0]);
                        var disrupters_pos = disrupter.position();

                        if (data.type == 'child') {
                            component.css({
                                left: disrupter.outerWidth() + disrupters_pos.left + self.component_spacing
                            });
                        } else {
                            component.css({
                                top: disrupter.outerHeight() + disrupters_pos.top + self.component_spacing
                            });
                        }
                    } else {
                        break;
                    }
                }
                //jsPlumb.redraw(component);
            }
            return component;
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

        $(document).on('keydown', function(e) {
            // remove focus from input fields
            $('.component-title-input:hidden', self).blur();

            if(e.keyCode == 13 || e.keyCode == 9) { // on enter or tab key
                var parent_component = $('.component-selected:first', self);
                if (!parent_component.length) return true;

                var parent_component_pos = parent_component.position();
                var pos_left, pos_top, type;

                if (e.keyCode == 13) { // enter => sibling
                    type = 'sibling';
                    pos_left = parent_component_pos.left;
                    pos_top = parent_component_pos.top + parent_component.outerHeight() + self.component_spacing;
                } else { // tab => child
                    type = 'child';
                    pos_left = parent_component_pos.left + parent_component.outerWidth() + self.component_spacing;
                    pos_top = parent_component_pos.top;
                }

                self.add_component({
                    pk: 'tmp-'+parseInt(Math.random()*1000000).toString(),
                    title: 'neu',
                    pos_left: pos_left,
                    pos_top: pos_top,
                    parent: parent_component.attr('data-component-pk'),
                    do_collide_check: true,
                    type: type,
                    set_focus_on_title_field: true
                }).toggleSelect();

                return false;
            }
        });

    };
})(jQuery);