odoo.define('crnd_wsd.blockui', function (require) {
    'use strict';
    var core = require('web.core');
    var Widget = require('web.Widget');

    var _t = core._t;

    var messages_by_seconds = function () {
        return [
            [0, _t("Loading...")],
            [20, _t("Still loading...")],
            [60, _t("Still loading...<br />Please be patient.")],
            [120, _t("Don't leave yet,<br />it's still loading...")],
            [300, _t(
                "You may not believe it, <br/>" +
                " but the application is actually loading...")],
            [420, _t(
                "Take a minute to get a coffee," +
                "<br />because it's loading...")],
            [3600, _t(
                "Maybe you should consider reloading" +
                " the application by pressing F5...")],
        ];
    };

    var Throbber = Widget.extend({
        template: "crnd_wsd.Throbber",
        start: function () {
            this.start_time = new Date().getTime();
            this.act_message();
        },
        act_message: function () {
            var self = this;
            setTimeout(function () {
                if (self.isDestroyed()) {
                    return;
                }
                var seconds = (new Date().getTime() - self.start_time) / 1000;
                var mes = null;
                _.each(messages_by_seconds(), function (el) {
                    if (seconds >= el[0]) {
                        mes = el[1];
                    }
                });
                self.$(".oe_throbber_message").html(mes);
                self.act_message();
            }, 1000);
        },
    });

    /** Setup blockui */
    if ($.blockUI) {
        $.blockUI.defaults.baseZ = 1100;
        $.blockUI.defaults.message =
            '<div class="openerp oe_blockui_spin_container" ' +
            'style="background-color: transparent;">';
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
    }

    var throbbers = [];

    function blockUI () {
        var tmp = $.blockUI.apply($, arguments);
        var throbber = new Throbber();
        throbbers.push(throbber);
        throbber.appendTo($(".oe_blockui_spin_container"));
        $(document.body).addClass('o_ui_blocked');
        return tmp;
    }

    function unblockUI () {
        _.invoke(throbbers, 'destroy');
        throbbers = [];
        $(document.body).removeClass('o_ui_blocked');
        return $.unblockUI.apply($, arguments);
    }
    return {
        blockUI: blockUI,
        unblockUI: unblockUI,
    };
});
