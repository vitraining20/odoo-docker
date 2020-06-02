/* eslint-disable max-len */
odoo.define('crnd_wsd.trumbowyg.upload-file', function (require) {
    'use strict';

    require('web.core');

    var defaultOptions = {
        serverPath: '',
        fileFieldName: 'fileToUpload',
        fileNameFieldName: 'filename',
        isImageFieldName: 'is_image',

        // Additional data for ajax [{name: 'key', value: 'value'}]
        data: [],

        // Additional headers
        headers: {},

        // Additional fields
        xhrFields: {},

        // How to get url from the json response (for instance 'url' for {url: ....})
        urlPropertyName: 'file',

        // How to get status from the json response
        statusPropertyName: 'success',

        // Success callback: function (data, trumbowyg, $modal, values) {}
        // eslint-disable-next-line no-undefined
        success: undefined,

        // Error callback: function () {}
        // eslint-disable-next-line no-undefined
        error: undefined,
    };

    function getDeep (object, propertyParts) {
        // Copied from original upload plugin for Trumbowyg
        var mainProperty = propertyParts.shift(),
            otherProperties = propertyParts;

        if (object !== null) {
            if (otherProperties.length === 0) {
                return object[mainProperty];
            }

            if (typeof object === 'object') {
                return getDeep(object[mainProperty], otherProperties);
            }
        }
        return object;
    }

    function addXhrProgressEvent () {
        // Avoid adding progress event multiple times
        if (!$.trumbowyg.addedXhrProgressEvent) {
            var originalXhr = $.ajaxSettings.xhr;
            $.ajaxSetup({
                xhr: function () {
                    var req = originalXhr(),
                        that = this;

                    // eslint-disable-next-line no-undefined
                    if (req && typeof req.upload === 'object' &&
                        that.progressUpload !== undefined) {
                        req.upload.addEventListener('progress', function (e) {
                            that.progressUpload(e);
                        }, false);
                    }

                    return req;
                },
            });
            $.trumbowyg.addedXhrProgressEvent = true;
        }
    }

    addXhrProgressEvent();

    // Pluging to enable file upload in trumbowyg
    $.extend(true, $.trumbowyg, {
        langs: {
            en: {
                uploadFile: 'Upload File',
                file: 'File',
            },
            ua: {
                uploadFile: 'Завантажити файл',
                file: 'Файл',
            },
            ru: {
                uploadFile: 'Загрузить файл',
                file: 'Файл',
            },
        },
        plugins: {
            uploadFile: {
                // Based on original upload plugin for trumbowyg
                // Modified to be able to upload regular files or images
                // TODO: create PR for trumbowyg to enable file upload
                init: function (trumbowyg) {
                    trumbowyg.o.plugins.uploadFile = $.extend(
                        true, {}, defaultOptions,
                        trumbowyg.o.plugins.uploadFile || {});

                    var btnDef = {
                        ico: "upload",
                        fn: function () {
                            trumbowyg.saveRange();

                            var file = null,
                                fileName = null,
                                fileType = null,
                                prefix = trumbowyg.o.prefix;

                            var fields = {
                                file: {
                                    type: 'file',
                                    required: true,
                                    attributes: {
                                        // Accept: 'image/*'
                                    },
                                },
                                alt: {
                                    label: 'description',
                                    value: trumbowyg.getRangeText(),
                                },
                            };

                            var $modal = trumbowyg.openModalInsert(
                                // Title
                                trumbowyg.lang.uploadFile,

                                // Fields
                                fields,

                                // Callback
                                function (values) {
                                    var data = new FormData();
                                    data.append(
                                        trumbowyg.o.plugins.uploadFile.fileFieldName, file);

                                    trumbowyg.o.plugins.uploadFile.data.forEach(
                                        function (cur) {
                                            data.append(cur.name, cur.value);
                                        });

                                    if (!values.alt && fileName) {
                                        values.alt = fileName;
                                    }

                                    $.map(values, function (curr, key) {
                                        if (key !== 'file') {
                                            data.append(key, curr);
                                        }
                                    });
                                    if (fileName) {
                                        data.append(
                                            trumbowyg.o.plugins.uploadFile.fileNameFieldName,
                                            fileName);
                                    }
                                    if (fileType.split('/')[0] === 'image') {
                                        data.append(
                                            trumbowyg.o.plugins.uploadFile.isImageFieldName,
                                            true);
                                    }

                                    if ($('.' + prefix + 'progress', $modal).length === 0) {
                                        $('.' + prefix + 'modal-title', $modal)
                                            .after(
                                                $('<div/>', {
                                                    'class': prefix + 'progress',
                                                }).append(
                                                    $('<div/>', {
                                                        'class': prefix + 'progress-bar',
                                                    })
                                                )
                                            );
                                    }

                                    // Disable confirm button
                                    $modal.find('.trumbowyg-modal-submit').attr('disabled', 'disabled');

                                    $.ajax({
                                        url: trumbowyg.o.plugins.uploadFile.serverPath,
                                        headers: trumbowyg.o.plugins.uploadFile.headers,
                                        xhrFields: trumbowyg.o.plugins.uploadFile.xhrFields,
                                        type: 'POST',
                                        data: data,
                                        cache: false,
                                        dataType: 'json',
                                        processData: false,
                                        contentType: false,

                                        progressUpload: function (e) {
                                            $('.' + prefix + 'progress-bar').css('width', Math.round(e.loaded * 100 / e.total) + '%');
                                        },

                                        success: function (success_data) {
                                            if (trumbowyg.o.plugins.uploadFile.success) {
                                                trumbowyg.o.plugins.uploadFile.success(success_data, trumbowyg, $modal, values);
                                                return;
                                            }

                                            if (getDeep(success_data, trumbowyg.o.plugins.uploadFile.statusPropertyName.split('.'))) {
                                                var url = getDeep(success_data, trumbowyg.o.plugins.uploadFile.urlPropertyName.split('.'));

                                                if (fileType.split('/')[0] === 'image') {
                                                    trumbowyg.execCmd('insertImage', url, false, true);
                                                    var $img = $('img[src="' + url + '"]:not([alt])', trumbowyg.$box);
                                                    $img.attr('alt', values.alt);
                                                    $img.css('max-width', '100%');
                                                } else {
                                                    var link = $(['<a href="', url, '">', values.alt || values.url, '</a>'].join(''));
                                                    trumbowyg.range.insertNode(link[0]);
                                                    trumbowyg.syncCode();
                                                    trumbowyg.$c.trigger('tbwchange');
                                                }

                                                setTimeout(function () {
                                                    trumbowyg.closeModal();
                                                }, 250);
                                                trumbowyg.$c.trigger('tbwuploadsuccess', [trumbowyg, success_data, url]);
                                            } else {
                                                trumbowyg.addErrorOnModalField(
                                                    $('input[type=file]', $modal),
                                                    trumbowyg.lang[success_data.message]
                                                );
                                                trumbowyg.$c.trigger('tbwuploaderror', [trumbowyg, success_data]);
                                            }
                                        },

                                        error: trumbowyg.o.plugins.uploadFile.error || function () {
                                            trumbowyg.addErrorOnModalField(
                                                $('input[type=file]', $modal),
                                                trumbowyg.lang.uploadError
                                            );
                                            trumbowyg.$c.trigger('tbwuploaderror', [trumbowyg]);
                                        },
                                    });
                                }
                            );

                            $('input[type=file]').on('change', function (e) {
                                try {
                                    // If multiple files allowed, we just get the first.
                                    file = e.target.files[0];
                                } catch (err) {
                                    // In IE8, multiple files not allowed
                                    file = e.target.value;
                                }
                                fileName = file.name;
                                fileType = file.type;
                            });
                        },
                    };

                    trumbowyg.addBtnDef('uploadFile', btnDef);
                },
            },
        },
    });


});
