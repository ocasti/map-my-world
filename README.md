# Map My World API

## API Documentation

[OpenAPI](http://127.0.0.1:8000/docs)


## Requirements

* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Local development

### Run

To run from python virtual environment

```shell
fastapi dev app/main.py
```

### Dependencies

Create the python virtual environment

```shell
python -m venv .venv
```

Initialize the python virtual environment

```shell
source .venv/bin/activate
```

The dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

Install all the dependencies with:

```shell
poetry install
```

### Poetry

Install dependencies

```shell
poetry install
```

Add dependency

```shell
poetry add fastapi
```

Add dev dependency

```shell
poetry add pytest --group dev
```
