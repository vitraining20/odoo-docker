Generic Requests
================

.. |badge2| image:: https://img.shields.io/badge/license-OPL--1-blue.png
    :target: https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps
    :alt: License: OPL-1

.. |badge3| image:: https://img.shields.io/badge/powered%20by-yodoo.systems-00a09d.png
    :target: https://yodoo.systems
    
.. |badge5| image:: https://img.shields.io/badge/maintainer-CR&D-purple.png
    :target: https://crnd.pro/
    
.. |badge4| image:: https://img.shields.io/badge/docs-Generic_Request-yellowgreen.png
    :target: https://crnd.pro/doc-bureaucrat-itsm/11.0/en/


|badge2| |badge4| |badge5|

Generic Request module is an independent application which also operates as a part of Bureaucrat application. It is a managing system for logging, recording, tracking, addressing, handling and archiving issues that occur in daily routine.

It is designed to be the single channel for submitting all the events that prevent normal business operation.

Generic requests allows any organisation to understand own technical support requirements and define an incident managing process. The operator of the Generic Request module is responsible for following each event through its escalation process and ensure the fastest way for its resolution.

Generic Request allows accumulating the information about incidents and developing knowledgebase for their quick work around, handling and resolution.

All the incidents are documented and tracked until they are resolved. Information about incidents is coordinated for faster and easier resolution. Reports generated while managing the incidents allow defining the problem areas and create the ways for their preventing.

Following idea is used:
'''''''''''''''''''''''

- *There are different categories of requests*
- *Each category have list of request types*
- *Each request have a type*
- *Each request type have list of request stages, and links to start stage and done stage*
- *Request can move across stages defined in request type*
- *Each request type can also define Stage routes,
  that are simply pairs for from_stage and to_stage,
  with optional server action to run on move,
  and optional restrictions based on user or group for move by this route.*
- *Each request type can have bound list of request fields, user must fill before
  request could be saved (sent)*


Read the `Generic Request <https://crnd.pro/doc-bureaucrat-itsm/11.0/en/>`__ Module Guide for more information.


The Generic Request module is part of the Bureaucrat ITSM project. 
You can try it by the references below.

Launch your own ITSM system in 60 seconds:
''''''''''''''''''''''''''''''''''''''''''

Create your own `Bureaucrat ITSM <https://yodoo.systems/saas/template/bureaucrat-itsm-demo-data-95>`__ database

|badge3| 

Bug Tracker
===========

Bugs are tracked on `https://crnd.pro/requests <https://crnd.pro/requests>`_.
In case of trouble, please report there.


Maintainer
''''''''''
.. image:: https://crnd.pro/web/image/3699/300x140/crnd.png

Our web site: https://crnd.pro/

This module is maintained by the Center of Research & Development company.

We can provide you further Odoo Support, Odoo implementation, Odoo customization, Odoo 3rd Party development and integration software, consulting services. Our main goal is to provide the best quality product for you. 

For any questions `contact us <mailto:info@crnd.pro>`__.
