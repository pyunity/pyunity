# Contributing to PyUnity
We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `develop`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions will be understood under the same [MIT License](https://docs.pyunity.x10.bz/en/latest/license.html) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/pyunity/pyunity/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/pyunity/pyunity/issues/new); it's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can. Please try to provide a [minimal reproducible example](https://stackoverflow.com/help/minimal-reproducible-example).
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Use a Consistent Coding Style

* 4 spaces for indentation rather than tabs
* Adhere to our naming convention (it's a little different to Python's standard one):

  - PascalCase for class names and exported functions
  - camelCase for all variables (even local variables), all module names
    and all internal functions not to be used by the user

    - If you want to export an entire submodule, import it as `from . import module as Module` in the package `__init__.py` file. For example, `Logger` is exported as `from . import logger as Logger`.

* Add comments wherever needed, to explain what your changes do

## License
By contributing, you agree that your contributions will be licensed under its MIT License.

## References
This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md).
