# Overview
This library contains useful wrappers around the Tonic Textual API

## Usage

Instantiate the API wrapper using the following code:

```
from tonic_textual.redact_api import TonicTextual

# Do not include trailing backslash in TONIC_URL
api = TonicTextual(TONIC_TEXTUAL_URL, API_KEY)
```

Once instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.

## Build and package

Update the version in pyproject.toml.  Ensure you are in the python_sdk/ folder in the repo root for the following instructions.

Update build and twine

```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

Clean out dist folder

```
rm dist/ -rf
```

Now build

```
python -m build
```

And ship

```
python -m twine upload .\dist\*
```

The username is __token__ and the pw is your token including the 'pypi-'

## Sphinx docs

To build the sphinx docs locally run `make html` from the `docs` subdirectory.

The Sphinx docs for prod are [https://textual.tonic.ai/docs/index.html](https://textual.tonic.ai/docs/index.html).

### Docstrings

Docstrings should follow numpy style (https://numpydoc.readthedocs.io/en/latest/format.html), so that they render nicely in the auto generated sphinx docs.
Here's a simple example of how to write correctly formatted docstrings.
```python
def foo(x: int, y: str) -> Dict[str, int]:
    """Turns a string and an int into a dictionary.
    
    Parameters
    ----------
    x: int
        The integer that is the value of the dictionary.
    y: str
        The string that is the key of the dictionary.

    Returns
    -------
    Dict[str, int]
        A dictionary with y as key and x as value.
    """
    return {y: x}
```