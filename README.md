# lektor-seantis-website

The seantis website generated with [Lektor](https://github.com/lektor/lektor).

## Development Installation

```
git clone git@github.com:seantis/lektor-seantis-website.git
cd lektor-seantis-website
pipenv install --python python3 Flask==1.1.4 Lektor
pipenv run lektor plugins reinstall
pipenv run lektor server
```

## Build status
[![Build Status](https://travis-ci.org/seantis/lektor-seantis-website.svg?branch=master)](https://travis-ci.org/seantis/lektor-seantis-website)
