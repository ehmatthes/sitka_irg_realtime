Updating dependencies
===

This document explains how to update the project's dependencies.

### Updating all dependencies in one step

It's often simplest to try updating all dependencies at once, instead of trying to update each one individually:

- Destroy the existing `rt_env` virtual environment: `sudo rm -rf rt_env/`
- Recreate a new virtual environment: `python3 -m venv rt_env`
- Activate the new environment: `source rt_env/bin/activate`
- Reinstall the latest version of each existing dependency: `pip install -r rebuild_requirements.txt`
- Load env vars: `export $(cat .env_local)`
- Run tests: `pytest`
- Resolve any errors and warnings
- Regenerate requirements.txt: `pip freeze > requirements.txt`
- Repeat on the live server.

### Adding a new dependency

- Add entry to rebuild_requirements.txt, with no specific version number.
- Use cli pip install command with no specific version number.
- Run `pip freeze > requirements.txt` to save the specific version of the new dependency, and any new subdependencies, without changing any existing dependency.
