---
title: SSH possibilities
date: 02.04.2021
category: Networking
tags: ssh,services,notes
---

## What can I do with SSH?

The main purpose for ssh is to open a shell on a remote computer and that is simply done by `ssh user@host`, this will land you in a terminal on a remote machine.

## Opening GUI applications

To be able to do that you need to enable `X11Forwading` on the server.

## Security

If you want to protect against brute-force attacks, disable password authentication.

First you need to generate a key pair with `ssh-keygen`

```bash
$ ssh-keygen -b 4096
```

Secondly, send your public key to the remote machine.

```bash
$ ssh-copy-id host@server
```

Or if you have a different public key file

```bash
$ ssh-copy-id -i path/to/key.pub host@server
```

For automatic login use `ssh-add` and provide path to private key

```bash
$ ssh-add /path/to/private/key
```

Now you can automatically log into your server with your keys `ssh host@server`.

And finally disable password

`/etc/ssh/sshd_config`

```bash
PasswordAuthentication no
```

## Useful links
- https://wiki.archlinux.org/index.php/OpenSSH
- https://wiki.archlinux.org/index.php/SSH_keys#Copying_the_public_key_to_the_remote_server
