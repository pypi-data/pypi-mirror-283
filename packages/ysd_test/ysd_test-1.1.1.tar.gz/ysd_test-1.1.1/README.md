# ysd-test

[![Release](https://img.shields.io/github/v/release/top-maker/ysd-test)](https://img.shields.io/github/v/release/top-maker/ysd-test)
[![Build status](https://img.shields.io/github/actions/workflow/status/top-maker/ysd-test/main.yml?branch=main)](https://github.com/top-maker/ysd-test/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/top-maker/ysd-test/branch/main/graph/badge.svg)](https://codecov.io/gh/top-maker/ysd-test)
[![License](https://img.shields.io/github/license/top-maker/ysd-test)](https://img.shields.io/github/license/top-maker/ysd-test)

test

- **Github repository**: <https://github.com/top-maker/ysd-test/>
- **Documentation** <https://top-maker.github.io/ysd-test/>

## Getting started with your project

First, set up tool chain by using [asdf](https://github.com/asdf-vm/asdf) tool, add necessary plugins if not installed, run the following commands in project folder,

```bash
cd {{cookiecutter.project_name}}
asdf plugin add python
asdf plugin add poetry
asdf plugin add pre-commit
asdf install
```

Create a repository on GitHub with the same name as this project, and then run the following commands,

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks,

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

## Releasing a new version

- Install [tm-infra-robot](https://github.com/apps/tm-infra-robot) or Create/register your own Github App.
- Add a Github variable for `tm-infra-robot` APP ID with the name `TM_INFRA_ROBOT_APP_ID` by visiting [this page](https://github.com/top-maker/ysd-test/settings/variables/actions/new).
- Add a Github secret for `tm-infra-robot` private key with the name `TM_INFRA_ROBOT_PRIVATE_KEY` by visiting [this page](https://github.com/top-maker/ysd-test/settings/secrets/actions/new).

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/top-maker/ysd-test/settings/secrets/actions/new).

