# Python library to crawl user notes from sharkey instances

[![Latest Version on PyPI](https://img.shields.io/pypi/pyversions/sharkey-crawler?style=flat-square)](https://pypi.org/project/sharkey-crawler)
[![GitHub Tests Action Status](https://img.shields.io/github/actions/workflow/status/hexafuchs/sharkey-crawler/run-tests.yml?branch=main&label=tests&style=flat-square)](https://github.com/hexafuchs/sharkey-crawler/actions?query=workflow%3Arun-tests+branch%3Amain)
[![GitHub Code Style Action Status](https://img.shields.io/github/actions/workflow/status/hexafuchs/sharkey-crawler/fix-python-code-style-issues.yml?branch=main&label=code%20style&style=flat-square)](https://github.com/hexafuchs/sharkey-crawler/actions?query=workflow%3A"Fix+Python+code+style+issues"+branch%3Amain)
[![Total Downloads](https://img.shields.io/pypi/dm/sharkey-crawler.svg?style=flat-square)](https://pypi.org/project/sharkey-crawler)

Python wrapper for the `/users/notes` endpoint of Sharkey (and probably also Misskey). You can use this to crawl the 
public posts of a user.

## Installation

You can install the package via poetry (or another tool of your choosing):

```bash
poetry add sharkey-crawler
```

## Usage

```python
from sharkey_crawler import SharkeyServer

SharkeyServer('example.org').user_notes(
    user_id='xxxxxxxxxx',
    allow_partial=True, 
    with_channel_notes=True,
    with_renotes=False,
    with_replies=False,
    with_files=False,
    limit=10,
    since_id=None,
    since_date=None,
    until_id=None,
    until_date=None
)
```

Checkout the docstring for more usage information.

## Testing

```bash
# All
./venv/bin/pytest -m ""

# Unit
./venv/bin/pytest -m "unit"

# Integration
./venv/bin/pytest -m "integration"

# Unit and Integration
./venv/bin/pytest -m "integration or unit"
```

## Development

### Installing new dependencies

Either add the dependency to the optional dependencies, or create a new dependency within the `[project]` namespace, e.g.:

```toml
[project]
...
dependencies = [
    "requests==2.32.3"
]
```

Then, install dependencies with flit:

```bash
./venv/bin/flit install --only-deps --deps develop
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.