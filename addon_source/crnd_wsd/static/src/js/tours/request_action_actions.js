odoo.define('crnd_wsd.tour_request_actions_ok', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_actions_ok', {
        test: true,
        url: '/requests/open',
    }, [
        {
            content: "Search for requests of type 'Generic Question'",
            trigger: ".wsd_requests form#wsd-request-search" +
                " input[name='search']",
            run:     "text Generic Question",
        },
        {
            content: "Click on 'search' button",
            trigger: ".wsd_requests form#wsd-request-search" +
                " button[type='submit']",
        },
        {
            content: "Wait Generic Question found",
            trigger: ".wsd_requests .wsd_request:first " +
                ".content_info:has(span:containsExact('Generic Question'))",
        },
        {
            content: "Click on first selected request",
            trigger: ".wsd_requests .wsd_request:first a.request-name",
        },
        {
            content: "Check if it's type is 'Generic Question'",
            trigger: "#request-head #request-type " +
                "span:containsExact('Generic Question')",
        },
        {
            content: "Check if it's stage is 'Draft'",
            trigger: "#request-head #request-type" +
                " span:containsExact('Generic Question')",
        },
        {
            content: "Click on action Send",
            trigger: "#request-head-actions" +
                " .request-action:containsExact('Send')",
        },
        {
            content: "Check that stage changed to 'Send'",
            trigger: "#request-top-head-stage:containsExact('Sent')",
        },
        {
            content: "Click on action Close",
            trigger: "#request-head-actions" +
                " .request-action:containsExact('Close')",
        },
        {
            content: "Enter response text",
            trigger: "#dialog-response-text",
            run: function () {
                $("#dialog-response-text").trumbowyg(
                    'html', "<p>Response text</p>");
            },
        },
        {
            content: "Click on Save button",
            trigger: ".modal-dialog:has('#dialog-response-text')" +
                " .modal-footer .o_save_button",
        },
        {
            content: "Check that stage changed to 'Closed'",
            trigger: "#request-top-head-stage:containsExact('Closed')",
        },
        {
            content: "Check that request has response text",
            trigger: "#request-response-content >" +
                " p:containsExact('Response text')",
        },
    ]);
    return {};
});

