odoo.define('crnd_wsd.tour_request_mail_login_portal', function (require) {
    'use strict';

    var tour = require('web_tour.tour');

    tour.register('crnd_wsd_tour_request_mail_login_portal', {
        test: true,
    }, [
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
            content: "Check we are logged in Portal UI and see request page",
            trigger: ".wsd_request #request-top-head-name",
        },
    ]);
    return {};
});


