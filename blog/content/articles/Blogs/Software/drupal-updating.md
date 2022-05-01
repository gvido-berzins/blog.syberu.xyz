---
title: Updating Drupal (9.x)
date: 22-07-2021
category: Software
tags: cms,drupal,blog
---

# Updating Drupal

## Context

Today I received a warning that I need to update drupal to fix some security issue (9.2.1 -> 9.2.2), I read the release notes and the security risk that was fixed and luckly this wasn't a big issue (as in the way it was explained), but when I read the CVE from [here](https://www.cybersecurity-help.cz/vdb/SB2021072221), I discovered that its an RCE in the Backdrop Archive_Tar pear library, in simpler terms, the attacker can upload an archive file and the application won't properly check, if it's a symbolic link on the system, thus the attacker can provide a maliciously crafter file and compromise the system. 

It is mentioned that its exploited in the wild, but I couldn't find a publicly available exploit.

Ok, enough background.

## Updating Drupal to a minor version via Composer

There were no issues for me when doing it with composer, everything went as expected. A huge help was the [documentation](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer), which I followed, so here's the process.

Change directory to the site folder

```bash
cd /var/www/swb/
```

Check what kind of drupal is installed

```bash
composer show drupal/core-recommended
```

- If the recommended version is not installed you will get "package not found"

Then check for outdated packages and after that upgrade (this line is for `core-recommended`, check the docs for other)

```bash
composer outdated "drupal/*"
composer update drupal/core "drupal/core-*" --with-all-dependencies
```

Now it should be updated, re-check just in case

```bash
composer show drupal/core-recommended
composer outdated "drupal/*"
```

## Installing Drush and updating the database

### Installing drush

Now I need to update the database and rebuild the cache so Drupal doesn't bug me and drush (Drupal Shell) is a very useful utility, not just in updates ([see the docs](https://docs.drush.org/en/9.x/install/))

```bash
composer require drush/drush
```

- This will install drush into the project path `vendor/bin/drush`

I want to access it globally, so I will download and install the [launcher](https://github.com/drush-ops/drush-launcher)

```bash
wget -O drush.phar https://github.com/drush-ops/drush-launcher/releases/latest/download/drush.phar
chmod +x drush.phar 
sudo mv drush.phar /usr/local/bin/drush
```

Now let's check if it's installed

```bash
drush list
```

### Finally updating the database

Let's finally update the database and rebuild the cache

```bash
drush updatedb
drush cache:rebuild
```

See? Easy. That's all I got for this blog, hope this was useful.
