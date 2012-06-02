(function($) {
    $.fn.mindmapMapComponent = function(opts) {
        var self = this;

        // clone component from tpl
        self = $('#component-tpl').clone()
            .attr('id', 'mindmap-component-'+opts.id)
            .css('display', 'block');

        self.last_sent_dragg_pos = [0, 0];
        self.cross_shift_offset_total = [0, 0];
        self.cross_shift_offset_current = [0, 0];

        self.toggleSelect = function() {
            $('#mindmap-map .component').removeClass('component-selected');
            self.toggleClass('component-selected');
        }

        var title = $('.component-title:first', self);
        title.attr('value', opts.title);
        title.on('click', function(){
            title.focus();
            title.on('keydown', function(e) {
                if (e.keyCode == 13 || e.keyCode == 9) { // on enter or tab
                    title.blur();
                    return false;
                }
            });
        });
        self.css({
            left: opts.left,
            top: opts.top
        });

        self.get_compontent_id = function(id) {
            return 'mindmap-component-'+id;
        }

        self.get_components_except_myself = function() {
            return $('.component:not(#'+self.get_compontent_id(opts.id)+')');
        }

        // root component get special color
        if(opts.level == 0) {
            self.addClass('component-root');
        }

        self.attr('data-parent-component-pk', opts.parent_id);
        self.attr('data-component-pk', opts.id);

        var map_pk = $('#mindmap-map').attr('data-map-pk');

        jsPlumb.ready(function () {
            // make compontent draggable
            jsPlumb.draggable(self, {
                scroll: true,
                stop: function () {
                    var pos = self.position();
                    // send last pos to client
                    $().mindmapSockjs.send('update_component_pos', {
                        map_pk: map_pk,
                        component_pk: opts.id,
                        pos: pos
                    });

                    // update last pos in db
                    var url = bm_globals.mindmap.map_component_update_pos_url.replace('#1#', map_pk).replace('#2#', opts.id);
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: {
                            'pos_left': pos.left,
                            'pos_top': pos.top
                        },
                        cache: false
                    });

                    // save crosshift offset
                    if (self.cross_shift_offset_total[0] || self.cross_shift_offset_total[1]) {
                        var url = bm_globals.mindmap.map_components_add_offset.replace('#1#', map_pk);
                        $.ajax({
                            url: url,
                            type: 'POST',
                            data: {
                                'offset_left': self.cross_shift_offset_total[0],
                                'offset_top': self.cross_shift_offset_total[1],
                                'component_exclude_pk': opts.id
                            },
                            cache: false
                        });
                        self.cross_shift_offset_total = [0, 0];
                    }

                    // "flush" cross_shift_offset_current (send to client)
                    if (self.cross_shift_offset_current[0] || self.cross_shift_offset_current[1]) {
                        console.log('flush');
                        $().mindmapSockjs.send('add_components_offset_except_one', {
                            map_pk: map_pk,
                            except_component_pk: opts.id,
                            offset_left: self.cross_shift_offset_current[0],
                            offset_top: self.cross_shift_offset_current[1]
                        });
                        self.cross_shift_offset_current = [0, 0];
                    }
                },
                drag: function() {
                    var pos = self.position();

                    // send pos update
                    // get length ->last_pos to ->current-pos
                    var length = Math.sqrt(
                        Math.pow(self.last_sent_dragg_pos[0]-pos.left, 2) + Math.pow(self.last_sent_dragg_pos[1]-pos.top, 2)
                    );

                    // special shift: shift all other components down/right if dragged comp. crosses top/left border
                    if (pos.left < 0 || pos.top < 0) {
                        var cross_shift = 10;

                        if (pos.left < 0) {
                            self.cross_shift_offset_current[0] += cross_shift;
                            self.cross_shift_offset_total[0] += cross_shift;
                        }
                        if (pos.top < 0) {
                            self.cross_shift_offset_current[1] += cross_shift;
                            self.cross_shift_offset_total[1] += cross_shift;
                        }

                        self.get_components_except_myself().each(function(){
                            console.log(this);
                            var comp_to_move = $(this),
                                comp_to_move_pos_left = comp_to_move.position().left + cross_shift,
                                comp_to_move_pos_top = comp_to_move.position().top + cross_shift;

                            if (pos.left < 0) {
                                comp_to_move.css({left: comp_to_move_pos_left});
                            }
                            if (pos.top < 0) {
                                comp_to_move.css({top: comp_to_move_pos_top});
                            }
                            jsPlumb.repaint(comp_to_move);
                        });

                        if (length > 20) {
                            $().mindmapSockjs.send('add_components_offset_except_one', {
                                map_pk: map_pk,
                                except_component_pk: opts.id,
                                offset_left: self.cross_shift_offset_current[0],
                                offset_top: self.cross_shift_offset_current[1]
                            });

                            self.cross_shift_offset_current = [0, 0];
                        }

                        self.last_sent_dragg_pos = [pos.left, pos.top];
                    }
                    // regular shift
                    else if (length > 100) {
                        console.log('update_component_pos');
                        $().mindmapSockjs.send('update_component_pos', {
                            map_pk: map_pk,
                            component_pk: opts.id,
                            pos: pos
                        });

                        self.last_sent_dragg_pos = [pos.left, pos.top];
                    }
                }
            });
            opts.container.append(self);

            if (opts.parent_id) {
                var parent = $('#'+self.get_compontent_id(opts.parent_id));
                jsPlumb.connect({
                    source: parent,
                    target: $('#'+self.get_compontent_id(opts.id)),
                    anchor: "AutoDefault",
                    paintStyle: {
                        lineWidth: 0.5,
                        strokeStyle: "gray",
                        outlineWidth: 1,
                        outlineColor: "white"
                    },
                    endpoint: "Blank",
                    connector:[ "Bezier", { curviness: 13 } ]
                });
            }

            self.on('click', '.btn-component-add', function () {
                var modal = $('#mindmap-component-new');
                modal.modal('show');
                $('#id_parent', modal).attr('value', self.attr('data-component-pk') || '');
                $('#id_pos_left', modal).attr('value', 250);
                $('#id_pos_top', modal).attr('value', 90);
            });

            self.on('click', function() {
               self.toggleSelect();
            });
        });

        return self;
    };
})(jQuery);