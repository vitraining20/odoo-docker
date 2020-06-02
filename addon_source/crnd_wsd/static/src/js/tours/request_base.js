odoo.define('crnd_wsd.tour_request_base', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_base', {
        test: true,
        url: '/',
    }, [
        {
            content: "Click 'Requests' account menu",
            trigger: "a[href='/requests']",
        },
        {
            content: "Wait for page loaded",
            trigger: ".wsd_requests",
        },
        {
            content: "Go to opened requests",
            trigger: ".wsd_requests a[href='/requests/open']",
        },
        {
            content: "Search for requests of type 'Printer Request'",
            trigger: ".wsd_requests form#wsd-request-search" +
                " input[name='search']",
            run:     "text Printer Request",
        },
        {
            content: "Click on 'search' button",
            trigger: ".wsd_requests form#wsd-request-search " +
                "button[type='submit']",
        },
        {
            content: "Wait Printer Request found",
            trigger: ".wsd_requests .wsd_request:first" +
                " .content_info:has(span:containsExact('Printer Request'))",
        },
        {
            content: "Click on first selected request",
            trigger: ".wsd_requests .wsd_request:first a.request-name",
        },
        {
            content: "Wait for request page loaded",
            trigger: "#wrap:has(h3:contains('RSR-'))",
        },
        {
            content: "Check if it's type is 'Printer Request'",
            trigger: "#request-head #request-type" +
                " span:containsExact('Printer Request')",
        },
        {
            content: "Type some text in discussion below request",
            trigger: "#discussion textarea[name='message']",
            run: function () {
                $("#discussion textarea[name='message']").trumbowyg(
                    'html', "<h1>Test comment</h1>"
                );
            },
        },
        {
            content: "Click on button 'Send'",
            trigger: "#discussion form.o_portal_chatter_composer_form " +
                "button[type='submit']:containsExact('Send')",
        },
        {
            content: "Check that message added to request",
            trigger: "#discussion .media[id^='message-'] " +
                ".media-body h1:containsExact('Test comment')",
        },
        {
            content: "Click on create request button",
            trigger: "a[href='/requests/new']",
        },
        {
            content: "Check that request creation process started",
            trigger: "div.wsd_request_new",
        },
    ]);
    return {};
});
