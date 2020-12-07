User Permissions
===

This document explains how to manage users in the project.

## Regular users

To create a regular user:

```
$ python manage.py shell_plus
>>> user = CustomUser.objects.create_user('new_username', 'nu@example.com`, 'my_password')
```

## Groups

There is only one named group at the moment, `Site Admins`. Members of this group can manage users and create notifications.

## Creating groups

To create groups, run `python make_groups.py` at the project root level.

## Adding users to the group

In shell plus:

```
$ python manage.py shell_plus
>>> user = CustomUser.objects.get(username='new_admin')
>>> site_admins = Group.objects.get(name='Site Admins')
>>> site_admins.user_set.add(user)
```