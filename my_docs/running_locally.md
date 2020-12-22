Running Locally
===

This document explains how to run the project on your local system.

## Setting up

Clone the project, make a venv, and migrate:

```
$ git clone https://github.com/ehmatthes/sitka_irg_realtime.git
$ cd sitka_irg_realtime
$ python3 -m venv rt_env
$ source rt_env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```

Now make a file called `.env_local`. Add the following line to this file:

```
PRODUCTION_ENVIRONMENT='local'
```

Now export this setting, and you should be able to run the project:

```
$ export $(cat .env_local)
$ python manage.py runserver
```

At this point the project should be running locally on your system, with stale data. But you won't be able to see that yet until you have a user account. Run a couple scripts to get some sample users:

```
$ python make_groups.py
$ python make_sample_users.py
```

Now you have three users:

- `sample_user`, with no special permissions.
- `sample_su`, with superuser permissions.
- `sample_admin`, which is a member of `Site Admins`. This user can make notifications.

The password for each account is its username, ie `sample_user` has the password `sample_user`. Log in as any one of these users, and you can see the full home page with the stale data.

Make a place to store data and plot images, and then run pull in fresh data:

```
$ mkdir current_data
$ mkdir -p media/plot_images
$ python refresh_data.py
```

Keep in mind this hits the USGS data source. If you are working on a visualization and don't need actual fresh data, please set `USE_FRESH_DATA=False`.

## Open questions

- Current data is flat and uninteresting. How do I see what the project would look like during a critical or near-critical event?