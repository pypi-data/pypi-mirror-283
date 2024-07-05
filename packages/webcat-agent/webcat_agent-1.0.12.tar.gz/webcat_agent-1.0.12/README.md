# WebCat Agent

Copyright (C) Clouden Oy 2024

## Overview

This is the WebCat system agent daemon. It collects basic system information
and submits it to the user's WebCat systems database using an API key.

## Building and publishing this package

Get PyPI API token: https://test.pypi.org/manage/account/#api-tokens

On Linux:

    python3 -m pip install --upgrade build
    python3 -m pip install --upgrade twine
    rm -rf dist
    python3 -m build
    python3 -m twine upload --repository testpypi dist/*
