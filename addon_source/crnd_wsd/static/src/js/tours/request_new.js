/* eslint-disable no-use-before-define */
odoo.define('crnd_wsd.tour_request_new', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_new', {
        test: true,
        url: '/requests/new',
    }, [
        {
            content: "Check that we in request creation process on step 'type'",
            trigger: ".wsd_request_new form#request_category",
        },
        {
            content: "Select request category SaAS / Support",
            trigger: "h4:has(span:containsExact('SaAS / Support'))" +
                " input[name='category_id']",
        },
        {
            content: "Click 'Next' button",
            trigger: "button[type='submit']",
        },
        {
            content: "Check that we in request creation process on step 'type'",
            trigger: ".wsd_request_new form#request_type",
        },
        {
            content: "Check category selected",
            trigger: "#request-selection-box #request-category" +
                " span:containsExact('SaAS / Support')",
        },
        {
            content: "Select request type Generic Question",
            trigger: "h4:has(span:containsExact('Generic Question'))" +
                " input[name='type_id']",
        },
        {
            content: "Click 'Next' button",
            trigger: "button[type='submit']",
        },
        {
            content: "Check category selected",
            trigger: "#request-selection-box #request-category" +
                " span:containsExact('SaAS / Support')",
        },
        {
            content: "Check type selected",
            trigger: "#request-selection-box #request-type" +
                " span:containsExact('Generic Question')",
        },
        {
            content: "Write request text (that raises creation User Error)",
            trigger: "#request_text",
            run: function () {
                $("#request_text").trumbowyg(
                    'html', "<p>create_user_error</p>");
            },
        },
        {
            content: "Click 'Create' button",
            trigger: "button[type='submit']",
        },
        {
            content: "Check that error message shown",
            trigger: "#request-error-list" +
                " ul > li:containsExact('Test user_error')",
        },
        {
            content: "Close error message",
            trigger: "#request-error-list button.close",
        },
        {
            content: "Write request text (that raises creation Exception)",
            trigger: "#request_text",
            run: function () {
                $("#request_text").trumbowyg('html', "<p>create_error</p>");
            },
        },
        {
            content: "Click 'Create' button",
            trigger: "button[type='submit']",
        },
        {
            content: "Check that error message shown",
            trigger: "#request-error-list ul > li:containsExact('Unknown" +
                " server error. See server logs.')",
        },
        {
            content: "Close error message",
            trigger: "#request-error-list button.close",
        },
        {
            content: "Write request text",
            trigger: "#request_text",
            run: function () {
                $("#request_text").trumbowyg(
                    'html', "<h1>Test generic request</h1>");
            },
        },
        {
            content: "Click 'Create' button",
            trigger: "button[type='submit']",
        },
        {
            content: "Wait for congratulation page loaded",
            trigger: "#wrap:has(h2:contains('Congratulation'))",
        },
        {
            content: "Click on request name ot open it",
            trigger: ".wsd_request a.request-name",
        },
        {
            content: "Wait for request page loaded",
            trigger: "#wrap:has(h3:contains('Req-'))",
        },
        {
            content: "Open request text eitor",
            trigger: "div#request-body-text > span.open-editor",
        },
        {
            content: "Check editor is opened",
            trigger: "#request-body-text > #request-body-text-editor",
        },
        {
            content: "Modify request text",
            trigger: "#request-body-text-editor-box",
            run: function () {
                $("#request-body-text-editor-box").trumbowyg(
                    'html', "<h1>Test generic request (modified)</h1>");
            },
        },
        {
            content: "Click on Save button",
            trigger: "#request-body-text-editor > .editor-control > .btn-save",
        },
        {
            content: "Test that request text was modified",
            trigger: "#request-body-text-content:containsExact(" +
                "'<h1>Test generic request (modified)</h1>')",
        },
        {
            content: "Click on Send action",
            trigger: "#request-head-actions" +
                " .request-action:containsExact('Send')",
        },
        {
            content: "Check that stage changed to 'Send'",
            trigger: "#request-top-head-stage:containsExact('Sent')",
        },
    ]);
    return {};
});
