odoo.define('crnd_wsd.trumbowyg', function (require) {
    'use strict';

    var utils = require('web.utils');
    var ajax = require('web.ajax');
    var core = require('web.core');

    require('crnd_wsd.trumbowyg.upload-file');

    // Fix trumbowyg svg icons path
    $.trumbowyg.svgPath = "/crnd_wsd/static/lib/trumbowyg/dist/ui/icons.svg";


    // Simple plugin to enable image loading
    $.extend(true, $.trumbowyg, {
        plugins: {
            uploadImage: {
                init: function (trumbowyg) {
                    trumbowyg.pasteHandlers.push(function (pasteEvent) {
                        var clipboardData = (
                            pasteEvent.originalEvent || pasteEvent
                        ).clipboardData;

                        $.each(clipboardData.files, function (index, file) {
                            if (file.type.match(/^image\//)) {
                                ajax.post('/crnd_wsd/file_upload', {
                                    'upload': file,
                                    'is_image': true,
                                }).done(function (result) {
                                    var data = JSON.parse(result);
                                    if (data.status === 'OK') {
                                        trumbowyg.execCmd(
                                            'insertImage',
                                            data.attachment_url, null, true);
                                        var $img = $(
                                            'img[src="' + data.attachment_url +
                                            '"]:not([width])', trumbowyg.$box);
                                        $img.css('max-width', '100%');
                                        trumbowyg.syncCode();
                                    }
                                    // TODO: handle status not ok
                                });
                            }
                        });

                    });
                },
            },
        },
    });


    var trumbowyg_options = {
        autogrow: true,
        resetCss: true,
        btns: [
            ['viewHTML'],
            ['undo', 'redo'],
            ['formatting'],
            ['strong', 'em', 'del'],
            ['foreColor', 'backColor'],
            ['link'],
            ['uploadFile'],
            ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
            ['unorderedList', 'orderedList'],
            ['table'],
            ['horizontalRule'],
            ['removeformat'],
            ['fullscreen'],
        ],
        plugins: {
            uploadFile: {
                serverPath: '/crnd_wsd/file_upload/',
                fileFieldName: 'upload',
                isImageFieldName: 'is_image',
                urlPropertyName: 'attachment_url',
                data: [
                    {
                        name: 'csrf_token',
                        value: core.csrf_token,
                    },
                ],
            },
            table: {
                styler: "table table-bordered table-stripped",
            },
        },
    };

    var lang_parts = (utils.get_cookie(
        'website_lang') || $('html').attr('lang') || 'en_US').toLowerCase();
    if (lang_parts.indexOf('_') >= 0) {
        lang_parts = lang_parts.split('_');
    } else if (lang_parts.indexOf('-') >= 0) {
        lang_parts = lang_parts.split('-');
    } else {
        lang_parts = [lang_parts];
    }

    if ($.trumbowyg.langs[lang_parts[0]]) {
        trumbowyg_options.lang = lang_parts[0];
    } else if ($.trumbowyg.langs[lang_parts[1]]) {
        trumbowyg_options.lang = lang_parts[1];
    }


    return {
        trumbowygOptions: trumbowyg_options,
    };

});
