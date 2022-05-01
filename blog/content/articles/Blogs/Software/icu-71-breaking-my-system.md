---
title: Updating to latest icu and breaking bunch of things in process
date: 01.05.2022
category: Software
tags: linux,arch,packages,blog
---

Small notes about the problems I encountered in doing this.

TLDR. Broke the system by updating select few packages along with the latest (71.1-1) icu package and fixed it with `sudo pacman -Syyu`.

## Start
I wanted to install the latest `obsidian` version on my system, once it was done, I ran it and...

![electron-icu-71-fail.png](images/electron-icu-71-fail.png)

Ok. I think I had something like this, I can fix it.

![icu-breaks-dependency.png](images/icu-breaks-dependency.png)

## I can fix it
Ok, then let's update all of those packages so icu 71.1-1 could be installed.

Adding all of the packages to the "to be installed" list so there are no conflicts

![update-all-packages-with-breaking-dependencies.png](images/update-all-packages-with-breaking-dependencies.png)

No issues now, yes!

![pacman-update-icu.png](images/pacman-update-icu.png)

Installing electron, because it still didn't work

![electron-update-fail.png](images/electron-update-fail.png)

This point helped be solve an issue that I previously had with keyrings, the fix was single, just update the keyring

![pacman-update-archlinux-keyring.png](images/pacman-update-archlinux-keyring.png)

After going through that, the moment of thruth.

![electron-missing-icu-70.png](images/electron-missing-icu-70.png)

Excuse me?

Maybe flatpak can fix this! Let's install it.

![flatpak-missing-icu-70.png](images/flatpak-missing-icu-70.png)

🙂

Let's build it from source, opening the README.md with vim

![vim-missing-icu-70.png](images/vim-missing-icu-70.png)

Here was the point where, a bunch of things broke, my terminals weren't opening (`terminator`, `konsole`), but at least `guake` was still running.

## The actual fix

Now, I was thinking, should I revert or should I try a super secret technique I was saving for the last ditch attempt.

I used it. The system update. `sudo pacman -Syyu`.

It went through. Let's recheck everything.

Terminator

![terminator-run-success.png](images/terminator-run-success.png)

Obsidian

![obisdian-run-success.png](images/obisdian-run-success.png)

Everything works again!

I was pretty surprised that it worked out, because I had issues, where even this step failed, but now it was my savior.

Morale of the story, make sure to regularly update your system or just update it when you manage to break your system.