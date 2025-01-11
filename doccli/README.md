# doccli

doccli is a folder that contains code that can/will use in the different module of the project (CLI, backend...)

## How to build it

- uv build --wheel

## How to add the package into a module

- uv pip install path/to/dist/doccli-*.whl 

## Run

- uv run -- .\doccli\__main__.py search /Test --exclude bar,.txt