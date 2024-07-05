Changelog
=========

0.6.0 (2024-07-04)
------------------

**New features**

* Use the callback class from mozilla-django-oidc-db to allow for a custom error view

0.5.0 (2024-06-27)
------------------

**New features**

* Add password to ``AXES_SENSITIVE_PARAMETERS``
* Use stricter ``django-axes`` settings
    * ``AXES_FAILURE_LIMIT`` changed from ``10`` to ``5``
    * ``AXES_COOLOFF_TIME`` changed from ``1`` to ``5`` minutes
* Make more ``log-outgoing-requests`` settings configurable
    * ``LOG_OUTGOING_REQUESTS_EMIT_BODY`` (default ``True``)
    * ``LOG_OUTGOING_REQUESTS_DB_SAVE_BODY`` (default ``True``)
* Add base template to display current version in admin

**Bugfixes**

* Remove FIXTURE_DIRS setting and add root level app to INSTALLED_APPS

**Other**

* Move documentation to readthedocs

0.4.2 (2024-06-20)
------------------

**Bugfixes**

* Add missing settings for ``TWO_FACTOR_WEBAUTHN``

0.4.1 (2024-06-13)
------------------

**Bugfixes**

* Add ``ordered_model`` to ``INSTALLED_APPS`` (required for ``django-admin-index``)
* Add ``two_factor.plugins.webauthn`` to ``INSTALLED_APPS`` (required for ``maykin_2fa``)

0.4.0 (2024-06-06)
------------------

**New features**

* Add django-setup-configuration to deps
* Add ELASTIC_APM_TRANSACTION_SAMPLE_RATE

0.3.0 (2024-05-17)
------------------

**New features**

* [#14] Add django-log-outgoing-requests to deps
* [open-zaak/open-zaak#1629] Add generic base settings file


0.2.0 (2024-03-22)
------------------

**New features**

* Add support for python 3.10
* Upgrade to Django 4.2
* Add maykin-2fa


0.1.0 (2024-01-30)
------------------

* Initial release as a metapackage to pin several dependencies
