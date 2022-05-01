---
title: Port Knocking
date: 14-07-2021
category: Security
tags: port-knocking,networking,defense,blog
---

# Port Knocking

Port knocking is a simple, low resource solution for protecting your server for unintended access, yet powerful enough if implemented properly, thus with a possibility to reducing successful attacks to near 0.

## What is port knocking

Port knocking in its esence is security through obscurity, at the first stage all of the systems ports are closed and only when the correct sequence of knocks is given, the configured ports are opened up to the client.

You can think of the sequence of knocks as pinging specific ports in a sequential manner (also can be at specific time intervals), e.g. a client knocks on ports 1000 --> 5001 --> 9001 and by providing the combination, the server opens the SSH port (22) for communication to the user. Just by implementing this makes the server a lot more secure, because just from these 3 combinations the attacker would need to brute-force all 3-digit port combinations (1-65535), which would be ~141 trillion packets to determine the correct port numbers.

## Where can it go wrong?

There are a few ways an attacker might exploit it. One of them is a MITM attack, but this will only be useful if the packets sent to the ports are not encrypted, otherwise an attacker can just figure out which ports are getting knocked on and repeat the same sequence.

Another method is by compromising the client machine, where the attacker can inspect the logs and find the correct sequence that way.

Lastly there is one more attack that will not give access, but will perform a DoS (Denial of Service) is IP spoofing, if the server has has added user IPs which are white-listed and attacker can spoof the IPs and start knocking on random ports, thus preventing access to users, by not allowing them to do the sequence (e.g. you inputting your bank PIN and some jackass pressing on the keypad at the same time).

Implementing port knocking on a high latency network could also be problematic, which could cause the packets to arrive at the wrong order or not at all, this could be the client and the server network at fault.

## Protections

Proper authentication and encryption is important in implementing port knocking properly, you want to disable the ability for attackers to perform replay, MITM and other attacks.

For good practice port knocking should be combined with other forms of authentication, like using TCP, UDP and ICMP protocols and using cryptographic hashes to defeat IP spoofing, in result the users won't be affected by brute-force attacks, that might be happening in parallel.

## Summarized Concerns

In general it is difficult to protect against replay attacks, asymmetric ciphers and HMAC schemes aren't usually possible to implement and it is trivial for an attacker to perform a DoS attack to a vulnerable server.

## Implementation

A simple program which can be used on a linux server is [knockd](https://linux.die.net/man/1/knockd), for which I have prepared a quick tutorial [here]().


# SPA (Single Packet Authorization)

SPA is an authorization scheme for strong service concealment, which is simply next level port knocking, as it addresses it's flaws, but retains the benefits, it requires a single packet which is encrypted, no-replayable and can be leveraged to make exploitation of vulnerabilities (0-day and unpatched code) more difficult.

## How does it work?

First of all a client needs to use a SPA + SSH client in order to connect (at least for SSH), when the client attempts an SSH connection an SPA packet is sent along-side the connection, the SPA packet first arrives at the "entrance" (club door), the SPA daemon validates the packet with the given keys (Rijndael key and HMAC, GPG, symmetric or other asymmetric key) and only when the authentication is successful, your SSH connection is passed to the server.

It is advised to use HMAC, because only then the authentication will be cryptographically strong and would have protection against cryptanalytic CBC-mode padding oracle attacks such as Vaudenay attack, but other protocols can also be used such as GnuPG, symmetric or other asymmetric keys.

It is also possible to implement this in cloud services such as AWS.

## Implementation

For implementing this protocol [fwknop](https://github.com/mrash/fwknop) can be used and I will be giving a quick tutorial on that which can be accessed [here](Link to tutorial).

# Read more

- [Port knocking on Wikipedia](https://en.wikipedia.org/wiki/Port_knocking)
- [fwknop by mrash on GitHub](https://github.com/mrash/fwknop)
- [knockd port-knock server](https://linux.die.net/man/1/knockd)








