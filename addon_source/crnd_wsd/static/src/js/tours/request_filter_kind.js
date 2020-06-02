odoo.define('crnd_wsd_kind.tour_request_kind_filter', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_kind_tour_request_kind_filter', {
        test: true,
        url: '/requests/my',
    }, [
        {
            content: "Check that we have Generic Question on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Generic Question'))",
        },
        {
            content: "Check that we have Upgrade request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Upgrade request'))",
        },
        {
            content: "Check that we have Printer Request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Printer Request'))",
        },
        {
            content: "Filter only demo requests",
            trigger: "#wsd-request-search-kind a:containsExact('Demo')",
        },
        {
            content: "Check that we have Printer Request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Printer Request'))",
        },
        {
            content: "Check that we have no Generic Question on page",
            trigger: ".wsd_requests:not(:has(.wsd_request " +
                ".content_info:has(span:containsExact('Generic Question'))))",
        },
        {
            content: "Check that we have no Upgrade request on page",
            trigger: ".wsd_requests:not(:has(.wsd_request" +
                " .content_info:has(span:containsExact('Upgrade request'))))",
        },
        {
            content: "Filter only WSD requests",
            trigger: "#wsd-request-search-kind a:containsExact('WSD')",
        },
        {
            content: "Check that we have Generic Question on page",
            trigger: ".wsd_requests .wsd_request " +
                ".content_info:has(span:containsExact('Generic Question'))",
        },
        {
            content: "Check that we have Upgrade request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Upgrade request'))",
        },
        {
            content: "Check that we have Printer Request on page",
            trigger: ".wsd_requests:not(:has(.wsd_request " +
                ".content_info:has(span:containsExact('Printer Request'))))",
        },
        {
            content: "Show all requests",
            trigger: "#wsd-request-search-kind a:containsExact('All')",
        },
        {
            content: "Check that we have Generic Question on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Generic Question'))",
        },
        {
            content: "Check that we have Upgrade request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Upgrade request'))",
        },
        {
            content: "Check that we have Printer Request on page",
            trigger: ".wsd_requests .wsd_request .content_info:has(" +
                "span:containsExact('Printer Request'))",
        },
    ]);
    return {};
});
