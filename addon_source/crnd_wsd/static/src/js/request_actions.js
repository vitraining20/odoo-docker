odoo.define('crnd_wsd.request_actions', function (require) {
    'use strict';

    var trumbowyg = require('crnd_wsd.trumbowyg');

    var Dialog = require("web.Dialog");

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var blockui = require('crnd_wsd.blockui');

    var _t = core._t;

    var snippet_animation = require('website.content.snippets.animation');
    var snippet_registry = snippet_animation.registry;

    ajax.loadXML('/crnd_wsd/static/src/xml/templates.xml', qweb);

    var WDialog = Dialog.extend({
        init: function (parent, options) {
            var opts = options || {};
            this._super(parent, _.extend({}, {
                buttons: [
                    {
                        text: opts.save_text || _t("Save"),
                        classes: "btn-primary o_save_button",
                        click: this.save,
                    },
                    {
                        text: _t("Discard"), close: true,
                    },
                ],
                technical: false,
            }, opts));

            this.destroyAction = "cancel";

            var self = this;
            this.opened().then(function () {
                self.$('input:first').focus();
            });
            this.on("closed", this, function () {
                this.trigger(this.destroyAction, this.final_data || null);
            });
        },
        save: function () {
            this.destroyAction = "save";
            this.close();
        },
    });


    var RequestActionHelper = snippet_animation.Class.extend({
        selector: '.wsd_request',

        init: function () {
            var self = this;
            this._super.apply(this, arguments);

            self.visible_request_text_height = 500;
            self.visible_request_text_height_diff = 10;
        },

        start: function () {
            var self = this;

            self.request_id = self.$target.data('request-id');
            self.$target.removeData('request-id');

            self.$request_body_text = self.$target.find("#request-body-text");
            self.$request_text_content = self.$request_body_text.find(
                "#request-body-text-content");

            self.readmore_buttons = {
                'readmore': self.$request_body_text.find(
                    '> .request-readmore-button'),
                'readless': self.$request_body_text.find(
                    '> .request-readless-button'),
            };

            // Register handlers for request actions
            self.$target.find("#request-head-actions a.request-action").on(
                'click', function () {
                    self.on_request_action($(this));
                });

            self.$request_body_text.find("> span.open-editor").on(
                'click', function () {
                    self.on_request_editor_open();
                });

            // Bind handlers for readmore / readless
            self.readmore_buttons.readmore.on('click', function (ev) {
                ev.preventDefault();
                self.do_readmore();
            });
            self.readmore_buttons.readless.on('click', function (ev) {
                ev.preventDefault();
                self.do_readless();
                $('html,body').animate({
                    scrollTop: self.$request_body_text.offset().top - 25,
                }, 'fast');
            });
            $(window).on('resize', _.debounce(function () {
                self.do_readreset();
                self.toggle_readmore_mode();
            }, 500));

            self.toggle_readmore_mode();
        },

        toggle_readmore_mode: function () {
            var self = this;
            var vheight = self.visible_request_text_height -
                self.visible_request_text_height_diff;
            if (self.$request_text_content.height() > vheight) {
                self.do_readless();
            }
        },

        do_readreset: function () {
            var self = this;
            self.$request_text_content.css('height', '');
            self.$request_text_content.css('max-height', '');
            self.readmore_buttons.readmore.hide();
            self.readmore_buttons.readless.hide();
        },

        do_readless: function () {
            var self = this;
            var vheight = self.visible_request_text_height;
            self.$request_text_content.height(vheight);
            self.$request_text_content.css('max-height', '');
            self.readmore_buttons.readmore.show();
            self.readmore_buttons.readless.hide();
        },
        do_readmore: function () {
            var self = this;
            self.$request_text_content.css('height', '');
            self.$request_text_content.css('max-height', 'none');
            self.readmore_buttons.readmore.hide();
            self.readmore_buttons.readless.show();
        },

        on_request_editor_open: function () {
            var self = this;

            self.$editor_content = $(
                qweb.render('crnd_wsd.request_text_editor', {
                    'request_text': self.$request_text_content.html(),
                })
            );

            self.$request_body_text.append(self.$editor_content);
            self.$editor = self.$editor_content.find("> textarea");
            self.$editor.trumbowyg(trumbowyg.trumbowygOptions);

            // Hide original content
            self.$request_text_content.hide();
            self.do_readreset();

            // Bind editor events
            self.$editor_content.find(".btn-cancel").on('click', function () {
                self.on_request_editor_cancel();
            });
            self.$editor_content.find(".btn-save").on('click', function () {
                self.on_request_editor_save();
            });

            self.$request_body_text.find(".open-editor").hide();

        },

        on_request_editor_cancel: function () {
            var self = this;
            self.$editor_content.remove();
            self.$request_text_content.show();
            self.$request_body_text.find(".open-editor").show();
            self.do_readreset();
            self.toggle_readmore_mode();
        },

        on_request_editor_save: function () {
            var self = this;

            var request_text = self.$editor.val();
            blockui.blockUI();
            ajax.jsonRpc(
                '/crnd_wsd/api/request/update-text',
                'call', {
                    'request_text': request_text,
                    'request_id': self.request_id,
                }
            ).then(function (result) {
                blockui.unblockUI();
                if (result.error) {
                    return Dialog.alert(null, result.error, {
                        title: _t("Error"),
                    });
                }
                self.$request_text_content.html(result.request_text);
                self.$editor_content.remove();
                self.$request_text_content.show();
                self.$request_body_text.find(".open-editor").show();
                self.do_readreset();
                self.toggle_readmore_mode();

            }, function (error) {
                blockui.unblockUI();
                return Dialog.alert(null, error.message, {
                    title: _t("Error"),
                });
            });
        },

        _do_request_action: function (action_id, response_text) {
            var self = this;
            blockui.blockUI();
            ajax.jsonRpc(
                '/crnd_wsd/api/request/do-action',
                'call', {
                    'request_id': self.request_id,
                    'action_id': action_id,
                    'response_text': response_text,
                }
            ).then(function (result) {
                blockui.unblockUI();
                if (result.error) {
                    return Dialog.alert(null, result.error, {
                        title: _t("Error"),
                    });
                }
                if (result.extra_action === 'redirect_to_my') {
                    window.location.href = '/requests/my';
                } else {
                    window.location.reload(true);
                }
            }, function (error) {
                blockui.unblockUI();
                return Dialog.alert(null, error.message, {
                    title: _t("Error"),
                });
            });

        },

        on_request_action: function (act) {
            var self = this;
            var action_id = act.data('action-id');
            var require_response = act.data('require-response');

            if (require_response === "True") {
                var $response_content = $('<div/>').html(
                    '<textarea id="dialog-response-text"/>');
                var response_dialog = new WDialog(self, {
                    title: _t("Please, fill response text!"),
                    $content: $response_content,
                });
                response_dialog.on('save', self, function () {
                    self._do_request_action(action_id, $response_content.find(
                        'textarea').val());
                });
                response_dialog.opened(function () {
                    $response_content.find('textarea').trumbowyg(_.extend(
                        trumbowyg.trumbowygOptions, {
                            btns: [
                                ['undo', 'redo'],
                                ['formatting'],
                                ['strong', 'em', 'del'],
                                ['foreColor', 'backColor'],
                                ['link'],
                                ['uploadFile'],
                                ['justifyLeft', 'justifyCenter',
                                    'justifyRight', 'justifyFull'],
                                ['unorderedList', 'orderedList'],
                                ['table'],
                            ],
                        }));
                });
                response_dialog.open();
            } else {
                self._do_request_action(action_id, false);
            }
        },


    });

    snippet_registry.RequestActionHelper = RequestActionHelper;

    return {
        RequestActionHelper: RequestActionHelper,
    };

});
