# Extrusion Profile Quotes

## Background
I stumbled upon a technical challenge from Plethora here: https://gist.github.com/mrivlin/4bd6f29bedaec07b8e36

I didn't apply to Plethora, but the challenge interested me. I decided to tackle the challenge.

## What it does

This takes a definition of a profile in JSON format and returns a quote of the costs which involves machine and material costs.

## Requirements

Python 3.6+

## Installation

Clone this repo:

```
git clone https://github.com/yoongkang/extrusion_profile.git
cd /path/to/repo
python setup.py install
```

## Usage

This is provided as a library, so it can be used from the Python shell or any Python script as follows:

```python
from extrusion_profile import estimate_cost

estimate_cost('SomeFile.json')  # e.g. "14.01 dollars"
```

## Development

To run tests:

```
python setup.py test
```
