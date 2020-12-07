Running Locally
===

This document explains how to run the project on your local system.

## Setting up

Clone the project, make a venv, migrate, and run the project:

```
$ git clone https://github.com/ehmatthes/sitka_irg_realtime.git
$ cd sitka_irg_realtime
$ python3 -m venv rt_env
$ source rt_env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

At this point the project should be running locally on your system, with stale data.

To pull in fresh data, run the following command:

```
$ python refresh_data.py
```

Keep in mind this hits the USGS data source. If you are working on a visualization and don't need actual fresh data, please set `USE_FRESH_DATA=False`.

## Open questions

- Current data is flat and uninteresting. How do I see what the project would look like during a critical or near-critical event?