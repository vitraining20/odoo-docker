odoo.define('crnd_wsd.discussion', function (require) {
    'use strict';

    var trumbowyg = require('crnd_wsd.trumbowyg');
    var portal_chatter = require('portal.chatter');
    var publicWidget = require('web.public.widget');
    var webPublicRoot = require('web.public.root');


    // Extend mail thread widget
    var RequestChatter = portal_chatter.PortalChatter.extend({

        start: function () {
            var self = this;
            var defs = [];
            defs.push(this._super.apply(this, arguments));
            return Promise.all(defs).then(function () {
                self.$(
                    '.o_portal_chatter_composer textarea[name="message"]'
                ).each(function () {
                    var $textarea = $(this);
                    $textarea.trumbowyg(trumbowyg.trumbowygOptions);
                });
                self.$(
                    '.o_portal_chatter_composer ' +
                    'form.o_portal_chatter_composer_form'
                ).each(function () {
                    $(this).attr('action', '/mail/request_chatter_post');
                });
            });
        },
    });

    var requestChatter = publicWidget.Widget.extend({

        /**
         * @override
         */

        start: function () {
            var self = this;
            var defs = [this._super.apply(this, arguments)];
            var chatter = new RequestChatter(this, this.$el.data());
            defs.push(chatter.appendTo(this.$el));
            return Promise.all(defs).then(function () {
                // Scroll to the right place after chatter loaded
                if (window.location.hash === '#' + self.$el.attr('id')) {
                    $('html, body').scrollTop(self.$el.offset().top);
                }
            });
        },
    });
    webPublicRoot.publicRootRegistry.add(
        requestChatter, '.request_comments_chatter');

    return {
        RequestChatter: RequestChatter,
        requestChatter: requestChatter,
    };

});
