(function($) {
    $.fn.modalForm = function() {
        this.each(function(){
            var self = $(this);
            var body = $('.modal-body:first', self);
            var submit_btn = $('.btn-success:first', self);

            // merge default settings
            var opts = $.extend( {
                'title_tag' : 'h3',
                'title' : '',
                'data_url': self.attr('data-url')
            }, {
                'title_tag' : self.attr('data-title-tag'),
                'title' : self.attr('data-title')
            });

            // load form helper
            self.submit = function(method) {
                var form = body.find('form:first');
                form.hide();

                // show ajax loader
                body.append($('#ajax-load').clone().show().wrap('<div></div>').parent().html());

                var data = form.serialize();
                if (!method) {
                    method = 'POST'
                }

                submit_btn.addClass('disabled');

                $.ajax({
                    url: opts.data_url,
                    type: method,
                    data: data,
                    cache: false,
                    success: function (data) {
                        body.html(data);

                        var form = $('form:first', body);

                        // submit fields on enter
                        $('input', form).bind('keypress', function(e) {
                            if(e.keyCode == 13) { // enter code
                                self.submit();
                                return false;
                            }
                        });

                        submit_btn.removeClass('disabled');

                        // set focus on first input fields
                        $('input:visible:first', form).focus();

                        // trigger init func
                        self.trigger('initiated');

                        $('#ajax-load', body).remove();
                        form.show();
                    },
                    error: function() {
                        submit_btn.removeClass('disabled');

                        $('#ajax-load', body).remove();
                        form.show();
                    }
                });
            };

            // bind submit button
            submit_btn.click(function(){
                self.submit();
            });

            self.on('show', function() {
                self.submit('GET');
                return self;
            });

            // init
            $(opts.title_tag+':first', self).html(opts.title);
            submit_btn.addClass('disabled');
        });
    };
})(jQuery);