Testing
===

This document explains how tests are organized in the project, and how to run tests.

## Overview

Testing is done using [pytest-django](). Testing is minimal at the moment, really just a skeletal approach to testing so it will be easier to add tests as needed. The first tests focus on the home page, which is the most critical page in the project.

## Running tests

To run tests:

```
$ source rt_env/bin/activate
$ export $(cat .env_local)
$ pytest
```

This should run all current tests.

