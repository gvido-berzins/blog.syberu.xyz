---
title: CyberShock CTF 2022 Write-Up
date: 09-10-2022
category: Write-Ups
tags: write-up,ctf,cybershock
---

![CyberShock 2022 banner](images/cybershock-2022-banner.png)

![](images/cybershoch-2022-ctf-details.png)

## Overview

CyberShock 2022 was a CTF hosted by [CybExer](https://cybexer.com/) &
[CTF Tech](https://www.ctftech.com/) along with [CyberChess](https://cyberchess.lv/)
conference, organized by [CERT.lv](https://cert.lv/lv/) on October 4th of 2022, where the
participation was remote.

Compared to the last year's performance, our team "TheGoodGuys" scored a lot higher,
from 13th to 6th out of 36 competitors, this was without losing any points (taking
hints, closing challenges).

We couldn't complete the last challenges (cryptography related):

![CTF mission board](images/cs2022-mission-board.png)

And you can see us here on the leaderboard:

![CTF leaderboard](images/cs2022-leaderboard.png)

At our level, there was close competition and if we hadn't completed a single challenge
we could have landed 9th or 10th, but in the last few minutes we completed the "Minecraft"
challenge (300pts) which boosted us to the 6th place.

![CTF leaderboard closer](images/cs2022-leaderboard-2.png)

Overall CTF had an interesting theme along with some defense/hardening tasks
which were checked by an automated script that I really liked, like adding a password on
an apache server and hardening an SSH server with pubkey authentication.

## Challenges

In total, there were 28 tasks split into 3 categories, "Smart Home",
"Smart City" and "Smart Airspace".

Rules:

- Only 5 challenges can be open at the same time.
- Closing a challenge reduces points.
- Taking hints reduces points.

The challenges were access by remote kali virtual machines.

- [Kali In The Browser (Guacamole)](https://www.kali.org/docs/general-use/guacamole-kali-in-browser/)

### Smart Home

#### NETWORK FIX

```md
Description
It has been an ordinary day for you, but suddenly all of the IoT devices in your home have stopped working due to your router resetting itself to default settings.
You cannot even enter your home as the smart door lock does not have connectivity.
Luckily the router is accessible from the WiFi.
Question
You remember that you had documented down the old routing table output.
Analyze it and find out which IP address must be configured as a gateway for the devices in network 10.5.7.0/24

r2# show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
T - Table, v - VNC, V - VNC-Direct, A - Babel, D - SHARP,
F - PBR, f - OpenFabric,

- selected route, *- FIB route, q - queued route, r - rejected route
B>* 0.0.0.0/0 [20/0] via 10.101.32.7, eth0, 09w4d08h
O 10.5.0.0/24 [110/10] is directly connected, eth1, 16w5d14h
C>*10.5.0.0/24 is directly connected, eth1, 16w5d14h
O>* 10.5.1.0/24 [110/20] via 10.5.0.4, eth1, 16w5d14h
O>*10.5.2.0/24 [110/20] via 10.5.0.4, eth1, 16w5d14h
O>* 10.5.3.0/24 [110/20] via 10.5.0.4, eth1, 16w5d14h
O>*10.5.4.0/22 [110/20] via 10.5.0.5, eth1, 16w5d14h
O>* 10.5.18.0/24 [110/20] via 10.5.0.1, eth1, 09w4d08h
O>*10.101.31.16/30 [110/5000] via 10.5.0.1, eth1, 09w4d08h
C>* 10.101.32.16/30 is directly connected, eth0, 16w5d14h
O>* 172.16.15.0/24 [110/20] via 10.5.0.10, eth1, 16w5d14h
```

#### IT'S ALWAYS DNS

```md
DESCRIPTION
After fixing the routing configuration, your smart door starts functioning again but something in the network is still not functioning as intended.
To be exact, pinging the IP addresses works, but names do not resolve.
QUESTION
Investigate your DNS server Pi-hole
and find a way to read the log file at /var/log/dnserror.log
Pi-Hole: <http://env263.target03/admin>
Password: admin
```

#### COOL VIDEO

```md
DESCRIPTION
A friend asks for help with recent movie that was downloaded from torrents: something is wrong with player.
The video is available at <https://static.ctftech.io/challs/Horror_stories_2k21-720p.zip>
QUESTION
What is the address of C&C of the malware?
The answer is expected in usual format for an Internet address - <IP>:<PORT>
```

#### STUCK

```md
DESCRIPTION
Earlier, while you were stuck outside your younger brother also tried to fix the network.
By following an online guide he managed to open a text file in a command-line application.
He now seems to be totally stuck in this program, but the deadline for his schoolwork is fast approaching.
QUESTION
Help your brother so he can get the schoolwork from
/home/billy/schoolwork

Billy's workstation can be accessed over SSH:
Hostname: env263.target03
Port: 2223
Username: billy
Password: fortnitepro123
```

#### FRIDGE

```md
DESCRIPTION
Your mom brings in the package, where you find a large amount of soda.
In the package there is also a letter.
The letter reads, that the smart fridge had sent out the order to restock itself.
You are certain that you have not ordered the products and neither has your family.
QUESTION
Access your smart fridge management console to investigate what is happening
Connect to: env263.target03
Port: 2333
The answer can be found in the /etc/apt/ folder
```

#### MAILBOX

```md
DESCRIPTION
Once your brother managed to submit his homework, you get a notification that a package has been delivered to your smart mailbox.
You look outside the window and see your mother already opening the mailbox.
Out of the corner of your eye you notice a guy shoulder surfing while your mother is entering the PIN.
You decide to change the pin, but for this you need the admin pin code which you encrypted in a safe container when you initially got the mailbox.
Problem is that you don't remember the cipher you used for encryption.
QUESTION
You only remember the following details:
Tool: openssl
Password: Kh39.3e12kleZs-po7
Encrypted file
<https://static.ctftech.io/challs/pin.enc?_gl=1>*1i0w9rs*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDg5MjE3NC42LjEuMTY2NDg5MjI3OC4wLjAuMA..
```

#### MINECRAFT

```md
DESCRIPTION
You have been hosting a Minecraft server for your friends for a long time.
All has been running smoothly and you have learned a lot in the process. Friends are happy as well 🙂
One day suddenly you read news about all kinds of vulnerabilities and how everything is insecure.
You start to wonder if your server is also affected.
QUESTION
Find the vulnerability from your system.
When you have found it, get the flag from /flag.

Minecraft server:
Hostname: env263.target02
Port: 25565
Server is running in offline mode.
```

#### INFECTION

```md
Your mother comes to you complaining that her work computer is sometimes acting weirdly.
She also has been getting emails about failed logins to her Admirals account. Luckily MFA stopped the logins.
QUESTION
You have reason to think that the computer is infected with malware.
If you can find the malware, analyze it to figure out how it works.

Mom's computer:
Hostname: env263.target04
Protocol: RDP
Username: Administrator
Password: Cool2Pass
```

#### HOMEWORK

```md
DESCRIPTION
Help your brother Billy with his homework.
He has been complaining that it is too difficult.
QUESTION
Solve the homework to reveal the answer in flag.txt
Homework
```

#### EMOJI ANALYSIS

```md
DESCRIPTION
You find a strange note from your backpack.
PS! There is also a post-it-note on the backside of the paper where are written the following numbers 32 54 80 46 155.
QUESTION
Figure out what the note means and find the flag.
strange note: <https://static.ctftech.io/challs/encoded_story.html?_gl=1>*1oieq6w*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDk0OTc0MC4xMS4xLjE2NjQ5NDk3NDEuMC4wLjA.
```

#### Smart City

#### HEALTH CHECK

```md
DESCRIPTION
The city has set up a website to test the availability of different services.
The admins are seeing icmp request from the application to internal networks.
This is really strange as it should be able to ping only public IP addresses.
QUESTION
Help them to figure out what is going on.
They have assigned you an internal IP address of 172.20.10.2 to make the ping requests against from the application.
<http://env263.target03:1343/>
```

#### HARDEN

```md
DESCRIPTION
During regular systems audits, it was discovered that one of the DEV jumphosts does not meet the security baseline.
Therefore this system must be hardened.
TASK
Harden the SSH configuration so that it meets the baseline.
- Make sure that root login is disabled
- disable password authentication
Add this public key so that the user: sysadmin is able to log in with their private key

SSH access:
Hostname: env263.target02
Port: 2224
Username: sysadmin
Password: Cool2Pass
```

#### NEXIF

```md
DESCRIPTION
Test the security of this online Exiftool service.
QUESTION
Can you find the vulnerability and exploit it?
You can find the flag from the home folder.
<http://env263.target02:8082/>
```

#### SMART BIKE

```md
After making it to the council you speak with the local IT administrators.
They are impressed with your skills and want your help in a security audit.
An exposed API endpoint could be exposing some sensitive information on the city's new Smart Bike infrastructure.
Can you take a look and see if there are any security issues that can be fixed?
QUESTION
Find a way to abuse the functionality of an exposed API endpoint and retrieve the flag from /var/flag.txt
The only thing we know is the exposed IP address.
```

#### SELF-DRIVING-CAR

```md
DESCRIPTION
For your efforts, the city council has decided to award you with a free flight to a holiday destination.
Just as you have finished packing you get another call.
A company building self-driving cars has been experiencing an odd after-effect from the recent attacks against the city.
The city council has forwarded the company representative to you and after discussing the details you find out that they had a city guide application API integrated into their self-driving cars.
QUESTION
The company has provided you with SSH credentials and information that they use Robot Operating System for their self-driving cars.
You must find the status message of the active instance and help debugging the vehicle.
SSH:
Hostname: env263.target03
Port: 2222
Username: jack
Password: autonomous1337vehicles
```

#### BUS STOP

```md
DESCRIPTION
Your help is also needed for another task.
The previous developer for the bus stop digital signage servers has disappeared into thin air, but information still needs to be updated throughout the city.
QUESTION
You have been asked to help.
Find out if there is some vulnerability, backdoor, misconfiguration, etc. that would allow you to access the system.
Digital Signage Management Interface
Flag will be given when correct login credentials are used.

<http://env263.target03:8888/>
```

#### MAPS

```md
You manage to trace the origin of the malware back to the city guide website.
You attempt to report your findings to the city council, but all of the phone lines are down.
You decide to take matters into your own hands.
QUESTION
Find a vulnerability in the city guide application and for POC, read the flag from /var/flag.txt

<http://env263.target03:8111/>
```

#### REGISTRY

```md
DESCRIPTION
Now you must be a master of Windows registry. Set of files were recovered from backup of a Windows machine.
They are at <https://static.ctftech.io/challs/registry.tar.xz>.
You have to dig deep into the files and prove that you can process every piece of data that is in there.
The files can be broken or incomplete, but this just adds fun for a proper forensic engineer, right?
QUESTION
What is SHA-256 hash of the registry cell that contains value of HKLM\SYSTEM\ControlSet001\Control\Lsa\LimitBlankPasswordUse?
Submit the answer in hex-printed from, lower-case letters, without any separators.
```

#### ONE TIME PAD

```md
DESCRIPTION
SOC has managed to acquire two encrypted messages and a plain text message, that corresponds to one of the encrypted messages.
QUESTION
Identify the encryption key and recover the other plaintext.
Get the files from HERE
<https://static.ctftech.io/challs/captured_files.zip?_gl=1>*1t9e0jc*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDk0OTc0MC4xMS4xLjE2NjQ5NDk3NDEuMC4wLjA.
```

#### Smart Airspace

#### AUTOMATED

```md
Description
You find a paper with the following details:

Join CTF-Tech Discord.
Find Bot.
Write !minictf to the bot's DMs.

Good luck.
Question
Here is the invite to the server <https://discord.com/invite/cboe>
```

#### BOARDING PASS

```md
DESCRIPTION
After fixing the problems you want to finally complete your check-in, but all the airport systems still haven't recovered from the attacks.
The airline is unable to generate you a valid boarding pass.
Security is tight and they don't allow you into the security area if you don't pass the gates.
QUESTION
You get a brilliant idea. You still have an old ticket from your previous flight in your bag.
Maybe you can change some fields and gain access using this method?

New flight information:
Booking reference(PNR): CTF123
From: Tartu Airport
To: Sydney Airport
Airline: Nordica
Flight number: 0777
Ticket format: E-ticket
Change only these values!

Submit the new barcode data as an answer.
```

#### ATIS

```md
You have a suspicion that in addition to the ransomware, data is also exfiltrated out of the ATC networks.
All outbound traffic is monitored but new data is still appearing in the dark web
From when the attacks started, ATIS has been getting continuous phone calls.
Maybe it's worth investigating?
QUESTION
Investigate the ATIS call to see if you can find anything odd!
```

#### FLIGHT-PLAN

```md
DESCRIPTION
After everything is cleared you start to wonder about the origin of this attack.
When inspecting the logs, a correlation between the start of the compromise and a pdf file arriving to the ATC can be made.
QUESTION
Inspect the flight plan, find out if there is anything malicious hidden in it.
Flag format: uuid v4
<https://static.ctftech.io/challs/flight-plan.pdf?_gl=1>*18nguau*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDkxMjAyOC43LjEuMTY2NDkxMjAyOS4wLjAuMA..
```

#### WEATHER DATA

```md
DESCRIPTION
A pilot calls and complains that the weather is visibly different to what is noted in the report.
Without the correct data landing could be very difficult.
METAR is a format for reporting weather information.
A METAR weather report is predominantly used by aircraft pilots to assist in weather forecasting

During the ransomware attacks the METAR data was corrupted.
Data analysts discovered that the METAR file was split into two different files.
Every other row was moved to the second file.
Row 1 >> split1.csv
Row 2 >> split2.csv
Row 3 >> split1.csv
And so on...
QUESTION
Help the data analysts to combine the files back into one file
Answer is the md5sum of the combined file
```

#### TOP-SECRET

```md
DESCRIPTION
Management found out that the highly sensitive and top secret documents are accessible to all!
They must be hidden ASAP!
TOP-SECRET web page
TASK
You must protect this apache web server with authentication!
Configure basic authentication to protect the page
Use these credentials for auth:
Username: mulder
Password: Scully-th3-b3st!

SSH access:
Hostname: env263.target02 Port: 2222
Username: user
Password: Cool2Pass
```

#### BACKDOORED IMAGE

```md
DESCRIPTION
Developers have noticed that latest version of a SSH jumphost which they are using for remote access is acting weirdly.
When inspecting logs, they notice logins from strange accounts that should not be there.
Their own dev account password also seems to be compromised, as logins are coming from unknown IP addresses. Sysadmins have recreated the jumphost container from the latest image but with no luck.
Same activity is still seen. Could the Docker repository be hacked? Could the hackers have tampered with the image? You must find out!
QUESTION
What flag is stored in the backdoor?
Pull the jumphost image from docker.io/cybexer/ctf-jumphost:latest and find out how the image was compromised.
```

#### LEAKED DATA

```md
DESCRIPTION
You have managed to acquire an encrypted message from the exfiltrated data together with set of RSA public keys that belong to employees of the airport.
The keys are already extracted from certificates and saved to files with random names, thus anonymous.
It is known that the message is encrypted with one of those keys.
QUESTION
Find out what data was extracted from the network by decrypting it.
Recovered files
<https://static.ctftech.io/challs/output.zip?_gl=1>*1oed30*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDg4NzYwMC41LjAuMTY2NDg4NzYwMC4wLjAuMA..
```

#### ATC

```md
DESCRIPTION
A teller at the airport informs you that they are currently under a ransomware attack and therefore it is not possible to complete your check-in.
You offer to help and start looking for anything useful.
While visiting the air traffic control tower, you see a ransom message appear on the radar screens.
Seems that the radars somehow still work.
Maybe not everything has been encrypted yet.
QUESTION
Investigate if you can still recover some unencrypted files from the system.
ATC Radar
```

## Links

- [Winning team's "EVOSEC" write-up](https://arthepsy.eu/ctf/cybershock2022/)
- [CyberShock page](https://cybershock.lv/#ctf)
