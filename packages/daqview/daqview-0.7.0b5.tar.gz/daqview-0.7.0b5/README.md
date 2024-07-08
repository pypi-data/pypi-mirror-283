# DAQview

DAQview is a desktop application for viewing live and historic DAQ data.

It connects to a DAQd server which can stream it live data from a DAQ system,
or make a list of historic datasets available for download and viewing.

Written in Python using PyQt5 and pyqtgraph.

Licensed under the GPL 3.0 license.

## Installation

The recommended way to install is to use `pipx` to install from the published
version on PyPI:

```
pipx install daqview
```

To run after installation:

```
daqview
```

## Development Environment

First ensure poetry is installed:

```
pip install --user poetry
```

Then you should be able to install all dependencies using:

```
poetry install
```

Run using:
```
poetry run python -m daqview
```

Run tests with:
```
poetry run pytest
```

Run linters with:
```
poetry run flake8 daqview
poetry run pylint --rcfile=pylint.rc daqview
```

Generally flake8 should always pass cleanly, while pylint is much
harsher and its output should be checked over for any useful suggestions.

## Release

When ready to cut a release, ensure `daqview/__init__.py` has the correct
version number at the top, and then make a commit to master. Tag the commit
with `release-VERSION`, e.g. `release-0.1.0`, and push the commit and the
tag to GitLab, which will trigger a release build.
