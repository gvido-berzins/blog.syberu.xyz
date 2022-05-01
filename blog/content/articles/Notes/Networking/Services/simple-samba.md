---
title: Simple samba server on a Linux machine
date: 31.03.2021
category: Networking
tags: file-server,file-sharing,samba,services,notes
---

## Setting up a simple samba server

Pre-requisites

```bash
$ sudo apt install ntfs-3g samba samba-comon-bin
```

You're almost done here. Now you need to setup the config at `/etc/samba/smb.conf`.

Add these lines to the end of the file based upon your needs.

```
[MySambaName]
comment = Samba server comment
writeable = yes
browseable = yes
path = /home/drive
create mask = 0777
directory mask = 0777
public = yes
```

And now restart the samba service with `sudo /etc/init.d/samba restart`

You should be all set up now. To connect to it type into your file explorer `smb://<server-domain>/MySambaName`. If you don't use a file explorer and are on a Linux Distro (most likely both), then mount the drive described in the next session.

## Mounting the samba server on a Linux machine

Pre-requisites

```bash
$ sudo apt install cifs-utils
```

First find out if you can see the samba server, with the command bellow. This will list all available shares.

```bash
$ smbclient -L <server-domain> -U%
```

Note down the Sharename and mount it with the following command.

```bash
$ sudo mount -t cifs -o user=username //<server-domain>/Sharename <path to mount to>
```

You're all done. Now you can access your samba share.
