---
title: Updating Global Pip Packages
date: 2018-07-11
---

If you're like me, you have quite a few useful python packages installed
globally. For example ipython, mypy, httpie, flake8, autopep8 the list goes
on...

Occasionally I want to upgrade all such packages at once. Unfortunately unlike
other package managers (i.e. npm) there's no built in flag to update global
dependencies. So here's how I usually do so with pip

```
pip list -o --format=freeze | cut -d "=" -f 1 | pip install - U
```

Lets step through each section and explain what's going on here

- ``pip list -o``

Short for --outdated, lists outdated pip packages

- `--format=freeze`

Displays results in the pip freeze format: e.g. ipython==6.2.1

- `cut -d "=" -f 1`

Splits the field on the "=" delimiter, and selects the first field (1 indexed)

For example, splitting a stance by whitespace and selecting the first word:

```
λ echo "hello world" | cut -d " " -f 1
hello
```

- `pip install -U`

Short for --upgrade, upgrades all specified packages to the newest version

A fairly straightforward little snippet that helps me keep all my fancy Python command line tools up to date.
