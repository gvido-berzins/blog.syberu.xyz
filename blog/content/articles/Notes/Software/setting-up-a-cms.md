---
title: Setting up a CMS on a linux server
date: 31.03.2021
category: Software
tags: apache,cms,linux,notes
---

## Pre-requisites

First of all we need to install the LAMP stack. (Linux Apache, MySQL, PHP).

## Content Management Systems

### Drupal

## All you need to know for switching CMSs

For each CMS it is advised to create a separate database and it's user if you're testing which one you like.

```bash
$ sudo mysql -u root
```

```sql
CREATE DATABASE cms_name;
CREATE USER 'cms_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON database_name.* TO 'database_user'@'localhost';
SHOW GRANTS FOR 'database_user'@'localhost';
FLUSH PRIVILEGES;
quit
```

Configure CMS to work with database.

Create a new folder in `/var/www/`.

Assign new owner to the folder and privilages.

```bash
$ sudo chown -R $USER:$USER /var/www/your_domain
$ sudo chmod -R 755 /var/www/your_domain
```

Set correct permissions for the folder so that the webserver can have full access

```bash
$ sudo chown -R www-data: /var/www/drupal
```

Configure the site in sites-available.

```bash
$ sudo nano /etc/apache2/sites-available/your_domain.conf
```

Configuration template.

```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName your_domain
    ServerAlias www.your_domain
    DocumentRoot /var/www/your_domain
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Switch site with a2ensite with apache and test configuration

```bash
$ sudo a2ensite your_domain.conf
$ sudo apache2ctl configtest
```

Restart apache

```bash
$ sudo systemctl restart apache2
```
