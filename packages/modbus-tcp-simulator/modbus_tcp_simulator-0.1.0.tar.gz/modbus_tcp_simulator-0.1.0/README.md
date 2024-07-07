# modsim

[![Release](https://img.shields.io/github/v/release/top-maker/modsim)](https://img.shields.io/github/v/release/top-maker/modsim)
[![Build status](https://img.shields.io/github/actions/workflow/status/top-maker/modsim/main.yml?branch=main)](https://github.com/top-maker/modsim/actions/workflows/main.yml?query=branch%3Amain)
[![License](https://img.shields.io/github/license/top-maker/modsim)](https://img.shields.io/github/license/top-maker/modsim)

A Simple Modbus TCP Device Simulator used for modpoll tool

-   **Github repository**: <https://github.com/top-maker/modsim/>
-   **Documentation** <https://top-maker.github.io/modsim/>

## Getting started with your project

First, set up tool chain by using [asdf](https://github.com/asdf-vm/asdf) tool, add necessary plugins if not installed, run the following commands in project folder,

```bash
cd modsim
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
git remote add origin git@github.com:top-maker/modsim.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks,

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

## Releasing a new version

-   Install [tm-infra-robot](https://github.com/apps/tm-infra-robot) or Create/register your own Github App.
-   Add a Github variable for `tm-infra-robot` APP ID with the name `TM_INFRA_ROBOT_APP_ID` by visiting [this page](https://github.com/top-maker/modsim/settings/variables/actions/new).
-   Add a Github secret for `tm-infra-robot` private key with the name `TM_INFRA_ROBOT_PRIVATE_KEY` by visiting [this page](https://github.com/top-maker/modsim/settings/secrets/actions/new).
