# Changelog

## Version 1.26.0

Changed views, to show author as creator.
Before, on request page, only creator of request was shown.
After this update, in case when request was created on behalf of someone,
both, author and cretor, will be displayed on request page.


## Version 1.25.0

Fix layout regression on *fill request data* page introduced in release 1.14.0 or 1.14.1


## Version 1.22.0

- Added ability to redirect user to *My Requests* page after
  user clicked on website action (route).
  Added field *Website Extra Action* to request route model.
- Show on 'My Requests' filter requests that have current
  user as author but not creator
- Fix toolbar for texteditor in dialog, when response on request is required:
    - show buttons to change colors
    - show single button for *upload file*
      (instead of dropdown with *insert image* and *upload file*)
    - remove button for *horizontal rule* and *remove format*
    - remove buttons for *subscript* and *superscript*


## Version 1.21.0

[FIX] Use correct configuration for dialogs: make it possible to customize
colors of buttons via website theme.


## Version 1.19.0

- Show requests on user portal page


## Version 1.18.0

- WYSIWYG: Updated editor to newer version
- Added buttons to change font colors


## Version 1.17.0

- Added implementation of readmore feature for request page.
  If request takes more then 500px height,
  then it will be limited with this height and link 'Read more' will be shown.
- Trumbowyg: removed tool-button *Insert Image* that is confusing for users.
- Added extra tooltips for request type, category and kind.


## Version 1.15.0

- Added wsd public ui visibility to request's settings that allows to select whether to redirect unauthorized users to
login page or to show all request creation steps.


## Version 1.14.0

- Public (unregistered) users can see website UI of service desk.
  All steps of request creation are visible.
  On the final stage of request submission, all control items are disabled until the user is registered.
  Additional link for registration is displayed on the screen.


## Version 1.13.0

- Update text editor (trumbowyg) to 2.18.0 version
- Remove 'superscript' and 'subscript' buttons from text editor's toolbar.
  These buttons seems to be unused.


## Version 1.12.1

Fix display of avatars for portal users


## Version 1.12.0

- Added group for portal users that can see all requests
- Updated UA translations


