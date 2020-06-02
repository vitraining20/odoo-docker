odoo.define('generic_request.field_request_html', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var core = require('web.core');

    var _t = core._t;

    var FieldRequestHtml = require('web_editor.field.html').extend({
        className: 'oe_form_field oe_form_field_html_text request-html-field',

        init: function () {
            var self = this;
            this._super.apply(this, arguments);

            self.visible_text_height = 300;
            self.visible_text_height_diff = 10;
            self.max_init_attempts = 5;
        },
        _renderReadonly: function () {
            var self = this;
            this._super.apply(this, arguments);

            // Generate link
            self.$el.append(
                '<a class="request-html-read-more-link"> ' +
                _t('More') +
                '</a>');
            self.$readmore_link = self.$el.find(
                '>.request-html-read-more-link');
            self.$readmore_link.on('click', function (ev) {
                ev.preventDefault();
                if (self.$readmore_link.hasClass('request-read-less')) {
                    self.do_readless();
                    self.$el.closest('.o_content').animate({
                        scrollTop: self.$content.offset().top - 25,
                    }, 'fast');
                } else if (self.$readmore_link.hasClass('request-read-more')) {
                    self.do_readmore();
                } else {
                    self.toggle_readmore_mode();
                }
            });
            self.initialize_readmore(0);
            $(window).on('resize', _.debounce(function () {
                self.toggle_readmore_mode();
            }, 200));
            self.$content.find('img').on('load', _.debounce(function () {
                self.toggle_readmore_mode();
            }, 300));
        },

        initialize_readmore: function (attempt) {
            var self = this;
            var h = self.$content.height();
            var vheight = self.visible_text_height -
                self.visible_text_height_diff;
            if (h === 0 && attempt < self.max_init_attempts) {
                _.delay(function () {
                    self.initialize_readmore(attempt + 1);
                }, 200);
            } else if (h <= vheight && attempt >= self.max_init_attempts) {
                self.$content.css('max-height', 'none');
            } else {
                self.toggle_readmore_mode();
            }
        },

        toggle_readmore_mode: function () {
            var self = this;
            var vheight = self.visible_text_height -
                self.visible_text_height_diff;
            if (self.$content.height() > vheight) {
                self.do_readless();
            } else if (self.$content.height() <= vheight) {
                self.do_readreset();
            } else {
                self.do_readmore();
            }
        },

        do_readreset: function () {
            var self = this;
            self.$content.css('max-height', '');
            self.$readmore_link.hide();
            self.$readmore_link.removeClass(
                'request-read-less fa fa-chevron-up');
            self.$readmore_link.removeClass(
                'request-read-more fa fa-chevron-down');
        },

        do_readless: function () {
            var self = this;
            self.$content.css('max-height', '');
            self.$readmore_link.text(_t('More'));
            self.$readmore_link.removeClass(
                'request-read-less fa fa-chevron-up');
            self.$readmore_link.addClass(
                'request-read-more fa fa-chevron-down');
            self.$readmore_link.show();
        },
        do_readmore: function () {
            var self = this;
            self.$content.css('max-height', 'none');
            self.$readmore_link.text(_t('Less'));
            self.$readmore_link.removeClass(
                'request-read-more fa fa-chevron-down');
            self.$readmore_link.addClass(
                'request-read-less fa fa-chevron-up');
            self.$readmore_link.show();
        },
    });

    registry.add('request_html', FieldRequestHtml);

    return {
        FieldRequestTextHtml: FieldRequestHtml,
    };

});

