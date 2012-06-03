/*!
 * jQuery lightweight plugin boilerplate
 * Original author: @ajpiano
 * Further changes, comments: @addyosmani
 * Licensed under the MIT license
 */

;
(function ($, window, document, undefined) {
    var version = '0.1',
        defaults = {
            component_spacing:20
        };

    function MindMap(element, options) {
        var self = this;
        self.element = $(element);
        self.options = $.extend({}, defaults, options);
        self.pk = self.element.data('map-pk');
        self._defaults = defaults;
        jsPlumb.ready(function () {
            self.init();
        });
    }

    MindMap.prototype.init = function () {
        var self = this;

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

        // load initial components
        $.ajax({
            url:self.element.data('components-url'),
            type:'POST',
            data:{},
            cache:false,
            success:function (data) {
                $($.parseJSON(data)).each(function () {
                    data = this;
                    // merge data.fields into data
                    for (var attrname in data.fields) {
                        data[attrname] = data.fields[attrname];
                    }
                    data.fields = undefined;
                    data.parent_pk = data.parent;
                    self.addComponent(data);
                });
            },
            error:function () {

            }
        });

        $(document).on('keydown', function (e) {
            // remove focus from input fields
            $('.component-title-input:hidden', self.element).blur();

            if (e.keyCode == 13 || e.keyCode == 9) { // on enter or tab key
                var parent_component = $('.component-selected:first', self.element);
                if (!parent_component.length) return true;

                var parent_component_pos = parent_component.position();
                var pos_left, pos_top, type;

                if (e.keyCode == 13) { // enter => sibling
                    type = 'sibling';
                    pos_left = parent_component_pos.left;
                    pos_top = parent_component_pos.top + parent_component.outerHeight() + self.options.component_spacing;
                } else { // tab => child
                    type = 'child';
                    pos_left = parent_component_pos.left + parent_component.outerWidth() + self.options.component_spacing;
                    pos_top = parent_component_pos.top;
                }

                // add tmp pk, save will replace it by created db component pk
                var component = self.addComponent({
                    pk:'tmp-' + parseInt(Math.random() * 1000000).toString(),
                    title:'neu',
                    pos_left:pos_left,
                    pos_top:pos_top,
                    parent:parent_component.attr('data-component-pk'),
                    do_collide_check:true,
                    type:type,
                    set_focus_on_title_field:true,
                    save:true
                });

                component.toggleSelect();
                return false;
            }
        });
    };

    MindMap.prototype.addComponent = function (data) {
        var self = this;

        var component = $.mindmapMapComponent({
            pk:data.pk,
            container:self.element,
            title:data.title,
            left:data.pos_left,
            top:data.pos_top,
            parent_pk:data.parent_pk,
            level:data.level
        });

        // set focus on title input
        if (data.set_focus_on_title_field) {
            $('.component-title:first', component.element).focus();
        }

        if (data.do_collide_check) {
            while (true) {
                var disrupters = component.element.collidesWith('.component');
                if (disrupters.length > 0) {
                    var disrupter = $(disrupters[0]);
                    var disrupters_pos = disrupter.position();

                    if (data.type == 'child') {
                        component.element.css({
                            left:disrupter.outerWidth() + disrupters_pos.left + self.component_spacing
                        });
                    } else {
                        component.element.css({
                            top:disrupter.outerHeight() + disrupters_pos.top + self.component_spacing
                        });
                    }
                } else {
                    break;
                }
            }
        }

        jsPlumb.repaint(component.element);

        if (data.save) {
            var pos = component.element.position();
            var url = bm_globals.mindmap.map_component_add.replace('#1#', self.pk).replace('#2#', 'json');
            $.ajax({
                url:url,
                type:'POST',
                dataType:'json',
                data:{
                    title:data.title,
                    pos_left:pos.left,
                    pos_top:pos.top,
                    parent:data.parent                    },
                cache:false,
                success:function (response_data) {
                    component.setId(response_data.form.instance_pk);
                    $.mindmapSockjs.send('addComponent', {
                        map_pk:self.pk,
                        title:data.title,
                        component_pk:response_data.form.instance_pk,
                        pos:pos,
                        parent_pk:data.parent
                    });
                },
                error:function () {
                    component.element.remove();
                }
            });
        }

        return component;
    };

    $.fn.mindmapMap = function (options) {
        return this.each(function () {
            if (!$.data(this, 'plugin_mindmapMap')) {
                $.data(this, 'plugin_mindmapMap',
                    new MindMap(this, options));
            }
        });
    }

})(jQuery, window, document);
