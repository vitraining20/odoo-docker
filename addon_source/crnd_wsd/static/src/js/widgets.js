odoo.define('crnd_wsd.widgets.date-moment', function (require) {
    'use strict';

    var core = require('web.core');
    var time = require('web.time');

    var snippet_animation = require('website.content.snippets.animation');
    var snippet_registry = snippet_animation.registry;

    var _t = core._t;

    // Display date in format '2 hours ago', '3 days ago', etc
    var RequestDateMoment = snippet_animation.Class.extend({
        selector: '.date-moment',

        start: function () {
            var self = this;
            self.text_date = self.$target.text();
            self.$target.text(moment(
                self.text_date, time.getLangDateFormat() + ' ' +
                time.getLangTimeFormat()).fromNow());
        },

    });

    // Handle display of short info for related requests.
    // (on clieck on (i) icon in list of related requests
    var RequestShortInfo = snippet_animation.Class.extend({
        selector: '.request-short-info-link',

        start: function () {
            var self = this;
            self.$sinfo = self.$target.find('.request-short-info');

            self.$target.on('click', function () {
                self.info_toggle();
            });
            self.$target.on('mouseleave', function () {
                self.info_hide();
            });
            self.$sinfo.on('mouseleave', function () {
                self.info_hide();
            });
        },

        info_hide: function () {
            var self = this;
            self.$sinfo.removeClass('active');
        },

        info_toggle: function () {
            var self = this;
            self.$sinfo.toggleClass('active');
        },

    });

    // Readmore implementation for short lines (request text sample)
    var RequestReadMoreChars = snippet_animation.Class.extend({
        selector: '.request-text-read-more',

        start: function () {
            var self = this;

            // Max length of text (chars)
            self.text_length = 100;
            self.text_long = $.trim(self.$target.html());

            if (self.text_long.length > self.text_length) {
                self.enable_readmore();
            }
        },

        toggle_readmore: function () {
            var self = this;

            if (self.readmore_mode === 'less') {
                // Then show more text
                self.$target.html(self.text_long);
                self.generate_link(_t('less'));
                self.readmore_mode = 'more';
            } else if (self.readmore_mode === 'more') {
                self.$target.text(self.text_short);
                self.generate_link('...');
                self.readmore_mode = 'less';
            }
        },

        generate_link: function (label) {
            var self = this;

            if (self.$readmore_link && self.$readmore_link.length > 0) {
                self.$readmore_link.remove();
            }
            self.$target.append(
                '<a class="request-text-read-more-link"> ' + label + '</a>');
            self.$readmore_link = self.$target.find(
                'a.request-text-read-more-link');
            self.$readmore_link.on('click', function (ev) {
                ev.preventDefault();
                self.toggle_readmore();
            });
        },

        enable_readmore: function () {
            var self = this;

            // Save short text
            self.text_short = $.trim(self.$target.text()).substring(
                0, self.text_length);

            self.$target.text(self.text_short);
            self.generate_link('...');
            self.readmore_mode = 'less';
        },
    });

    snippet_registry.RequestReadMoreChars = RequestReadMoreChars;
    snippet_registry.RequestDateMoment = RequestDateMoment;
    snippet_registry.RequestShortInfo = RequestShortInfo;

    return {
        RequestReadMoreChars: RequestReadMoreChars,
        RequestDateMoment: RequestDateMoment,
        RequestShortInfo: RequestShortInfo,
    };
});
