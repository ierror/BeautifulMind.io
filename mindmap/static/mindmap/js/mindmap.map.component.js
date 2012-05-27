(function($) {
    $.fn.mindmapMapComponent = function(opts) {
        var self = this;

        self.get_id = function(id) {
            return 'mindmap-component-'+id;
        }

        jsPlumb.ready(function () {
            // clone component from tpl
            var component = $('#component-tpl').clone()
                .attr('id', self.get_id(opts.id))
                .css('display', 'block');

            component.find('.component-title').html(opts.title);
            component.css({
                left: opts.left,
                top: opts.top
            });

            // root component get special color
            if(opts.level == 0) {
                component.addClass('component-root');
            }

            // make compontent draggable
            jsPlumb.draggable(component, {
                stop: function () {
                    $().mindmapSockjs.send(JSON.stringify({pos: component.position()}));
                },
                drag: function() {
                    var left = component.position().left / 2,
                        top = component.position().top / 2;

                    $('.component').each(function(){
                        var self = $(this);
                        if (left < 0) {
                            self.css({left: self.position().left+left*-1});
                        }
                        if (top < 0) {
                            self.css({top: self.position().top+top*-1});
                        }
                        jsPlumb.repaintEverything();
                    });
                },
                scroll: true
            });
            opts.container.append(component);

            if (opts.parent_id) {
                var parent = $('#'+self.get_id(opts.parent_id));
                var parent_pos = parent.position();
                //component.offset({top:parent_pos.top + 100, left:parent_pos.left + 650});
                jsPlumb.connect({
                    source: parent,
                    target: $('#'+self.get_id(opts.id)),
                    anchor: "AutoDefault",
                    paintStyle: {
                        lineWidth: 0.5,
                        strokeStyle: "gray",
                        outlineWidth: 1,
                        outlineColor: "white"
                    },
                    endpoint: "Blank"
                });
            }

            self.on('click', '.component-add', function () {
                //var parent = $(this).parent().parent();
                //add_box({ title:'Window Main-10', id:'makeunique2', parent:parent });
            });
        });

    };
})(jQuery);