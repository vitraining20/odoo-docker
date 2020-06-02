# Changelog

## Version 1.39.0

- Fixed bug when with incorrect display of images in request text,
  when request was created by email.
- Added `lessc` to external dependencies, to avoid confusion for users that
  have not installed `lessc` compiler. It become optional for 12.0+ installations.


## Version 1.37.0

Fix Readmore feature: update state when images (that are in request text) loaded


## Version 1.35.0

Implemented Readmore / Readless functionality for request text and request response



## Version 1.34.0

Added categories for request event types


## Version 1.32.0

- Change UI of request form view to be consistent with frontend and other places.
  This change allows to select category before request type on request creation.
- Move *Request Events* stat-buttons to separate *Technical* page


## Version 1.31.0

Added graph view for requests


## Version 1.30.0

Merge `generic_request_priority` into core (`generic_request`)


## Version 1.29.0

- Module `generic_request_kind` merged into `generic_request`
- Added demo request with long description and images
- [FIX] display of images in request body


## Version 1.28.0

- Added ability to add comment in assign wizard for request
- Added button *Assign to me* on request


## Version 1.24.0

Request name in title displayed as `h2` instead of `h1` as before


## Version 1.20.0

Add global settings:
- 'Automatically remove events older then',
- 'Event Live Time',
- 'Event Live Time Uom'


## Version 1.17.0

- Make it possible to change request category for already created request
- New request event *Category Changed*
- Show *Requests* stat-button on user's form


## Version 1.16.4

#### Version 1.16.4
Add security groups user_see_all_requests and user_write_all_requests and rules for this groups


## Version 1.16.2

#### Version 1.16.2
Added generic_request_survey to request settings list.


## Version 1.16.1

#### Version 1.16.1
Added dynamic_popover widget to description field on request tree view.


## Version 1.16.0

Added `active` field to Request Stage


## Version 1.15.6

More information in error messages


## Version 1.13.11

#### Version 1.13.11
Added the ability to include request and response texts to mail notifications.


## Version 1.13.5

#### Version 1.13.5
- Automatically subscribe request author to request


