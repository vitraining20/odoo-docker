odoo.define('crnd_wsd.new_request', function (require) {
    'use strict';

    // Require Trumbowyg to be loaded.
    var trumbowyg = require('crnd_wsd.trumbowyg');
    var snippet_animation = require('website.content.snippets.animation');
    var snippet_registry = snippet_animation.registry;

    var blockui = require('crnd_wsd.blockui');

    var RequestCreateWidget = snippet_animation.Class.extend({
        selector: '#form_request_text',

        start: function () {
            this.load_editor();
            this.$target.submit(function () {
                blockui.blockUI();
            });

        },
        load_editor: function () {
            this.$form_request_text = this.$target.find('#request_text');
            this.$form_request_text.trumbowyg(trumbowyg.trumbowygOptions);
        },
    });

    snippet_registry.RequestCreateWidget = RequestCreateWidget;

    return {
        RequestCreateWidget: RequestCreateWidget,
    };

});
