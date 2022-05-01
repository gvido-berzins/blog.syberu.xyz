---
title: What are and why use Virtual Environments
date: 27.03.2021
category: Programming
tags: python,venv,notes
---

## About Virtual Environments

Virtual environments are used to install Python packages specific to the app in development.

Installing packages in the venv doesn't install them together with the ones in the system.

## Why should I care?

Simple. Version management. If your app requires a specific version of a package you can have 5 different versions across 5 different projects, because if you're gonna use a package installed in your system then the same version will be used for all packages and that would brake some apps if the version is not compatible.

## Using Virtual Environments

To install it use pip in the terminal

```
$ pip install virtualenv
```

After that simply create it in the desired project directory

```
$ python3 -m venv env
```

Activation & Deactivation

```
$ source env/bin/activate
(env) $ deactivate
```

## For a more detailed look, check RealPython
- https://realpython.com/python-virtual-environments-a-primer/
