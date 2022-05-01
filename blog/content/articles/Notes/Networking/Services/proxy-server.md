---
title: Setting up a proxy server
date: 01.05.2021
category: Networking
tags: proxy,server,kwm,linux,services,notes
---

A proxy server is a server on your network that computers connect to to access the internet.

NAT now replaces the proxy servers.

## Why?

Why don't we just connect to the router? **cache**

When 1 computer wants to download a file, the other computers don't need to download it again. **Improved bandwidth**.

- Caching Microsoft updates

ACL (Access Control Lists)

- Restricting

**The computers had to connect to the proxy server**

## Setting up a proxy server inside a virtual machine

I'm using virt-manager and my connection is KWM/QEMU

1. Install the prerequisites

```
$ sudo apt install squid
```

To view the access log

```
tail -f /var/log/squid/access.log
```

## Syntax

To allow select machines, add `acl` before deny all.

```
acl manjaro src 192.168.8.100

http_access allow localhost
http_access allow manjaro  # This should be before deny all

http_access deny all
```

To block websites add a deny before `http_access deny deny_websites`

```
acl manjaro src 192.168.8.100

http_access allow localhost
http_access allow manjaro

acl deny_websites dstdomain "/etc/squid/bad-sites.acl"
http_access deny deny_websites

http_access deny all
http_port 3128
```
