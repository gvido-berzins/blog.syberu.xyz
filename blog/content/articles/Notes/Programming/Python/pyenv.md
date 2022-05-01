---
title: Notes on PyEnv
date: 30.04.2022
category: Programming
tags: python,version-management,notes
---

- https://github.com/pyenv/pyenv-installer
- https://github.com/pyenv/pyenv/wiki#suggested-build-environment

## Installation
### Installation on CentOS 9

```bash
curl https://pyenv.run | bash
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
exec $SHELL
```

Installing a python version with configuration options
```bash
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.2
```

### Installation on fresh Ubuntu 22.04 LTS
Install dependencies
```bash
$ sudo apt update; sudo python-is-python3 curl make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

- `python-is-python3` to link python3 to python
- `curl` because ubuntu doesn't have it
- The rest of the packages, because otherwise, it's not possible to compile the python installations

Setup & install pyenv
```bash
curl https://pyenv.run | bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
```

- adds pyenv binaries to path
- initializes pyenv to have shims/virtual environments found

### Usage

Example of installing python and switching to it
```bash
ync@office:~$ pyenv install 3.11-dev
Cloning https://github.com/python/cpython...
Installing Python-3.11-dev...
Installed Python-3.11-dev to /home/ync/.pyenv/versions/3.11-dev

ync@office:~$ pyenv versions
* system (set by /home/ync/.pyenv/version)
  3.11-dev
ync@office:~$ pyenv global 3.11-dev
ync@office:~$ pyenv versions
  system
* 3.11-dev (set by /home/ync/.pyenv/version)
```

## Debugging & Troubleshooting

### pyenv not working, command not found
Add initializers and restart the terminal or re-source current shell profile

### Getting detailed build output for installations
```bash
MAKE_OPTS="--trace" pyenv install -v 3.6.15
```

### Python 3.6.15 install fails on Arch
Installing `clang` fixed the problem

```bash
sudo pacman -Sy clang
CC=clang pyenv install 3.6.15
```
