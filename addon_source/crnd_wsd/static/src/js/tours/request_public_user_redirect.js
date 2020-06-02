odoo.define('crnd_wsd.tour_request_public_user_redirect', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_public_user_redirect', {
        test: true,
        url: '/',
    }, [
        {
            content: "Go to Service desk page",
            trigger: "a:has(span:containsExact('Service Desk'))",
        },
        {
            content: "Enter login",
            trigger: "input#login",
            run:     "text demo-sd-website",
        },
        {
            content: "Enter password",
            trigger: "input#password",
            run:     "text demo-sd-website",
        },
        {
            content: "Press submit",
            trigger: "button[type='submit']",
        },
        {
            content: "Go to Service desk page",
            trigger: "a:has(span:containsExact('Demo Service Desk Websi...'))",
        },
        {
            content: "Click 'Create request' button",
            trigger: "a:containsExact('Create request')",
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
            content: "Write request text",
            trigger: "#request_text",
            run: function () {
                $("#request_text").trumbowyg('html', "New request text");
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
            content: "Check request text",
            trigger: "div:containsExact('New request text')",
        },
    ]);
    return {};
});

