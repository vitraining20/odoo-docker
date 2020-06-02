odoo.define('crnd_wsd.tour_request_actions_redirect', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_actions_redirect', {
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
            content: "Check that list of my requests opened",
            trigger: ".wsd_requests > .nav > li.active > " +
                "a[href='/requests/my']",
        },
    ]);
    return {};
});

