---
title: TLS and SSL
date: 28.03.2021
category: Networking
tags: security,encryption,notes
---

## Transport Layer Security (TLS)

Both TLS and SSL are protocols designed to ensure a secure communication across the network.

- TLS provides privacy and integrity, between communicating computer applications.
- Client needs to indicate to start a TLS communication either with STARTTLS request or through port like 443 (HTTPS).
- TLS stateful connection is established by a handshake procedure with an asymmetric cypher and further communication uses a symmetric cypher.
- During the handshake various parameters are set, like, a cypher, a digital certificate (server name and a trusted certificate authority or CA) and session keys are generated.
- TLS sits on the higher layers on OSI model like presentation layer, however applications generally use it on TCP layer.
- Symmetric encryption is generated uniquely for each connection and identities identified by public/private keys.
- Only TLS 1.3 is considered secure.

## Secure Socket Layer (SSL)

Versions 1.0, 2.0 contained serious flaws thus version 3.0 was developed, but it is still insecure.

- SSL 3.0 is vulnerable to POODLE.
