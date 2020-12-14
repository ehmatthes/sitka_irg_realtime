Account Management
===

This document explains how accounts are managed in this project.

## Overview

Accounts are managed using the `django-allauth` app.

## Quick shortcuts:

- [Basic documentation](https://django-allauth.readthedocs.io/en/latest/index.html)
- [Source code](https://github.com/pennersr/django-allauth)
  - [templates](https://github.com/pennersr/django-allauth/tree/master/allauth/templates/account)
  - [views](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)
  - [forms](https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py)
  - [urls](https://github.com/pennersr/django-allauth/blob/master/allauth/account/urls.py)

## Overriding templates

Default templates are [here](https://github.com/pennersr/django-allauth/tree/master/allauth/templates/account). These are in an `allauth/templates/account/` template directory. So allow overriding them, I have my `accounts` app listed before allauth in settings, and I have my own `accounts/templates/account/` directory. Notice the template directory name is not the same as the app name.

## Overriding forms

This can be done in settings. See <https://django-allauth.readthedocs.io/en/latest/configuration.html>, and look for `ACCOUNT_FORMS`.