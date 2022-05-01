---
title: Setting up Drupal CMS (In 2021 :O)
date: 2021-07-17
category: Software
tags: cms,drupal,blog
---

# Setting up a Drupal CMS

I needed to setup a website so I decided to use Drupal, the main reason is the feedback from it and usability for my needs, comparing it with WordPress, Drupal is better suited for developers who want to have a better customizability and better account management, I want to be able to do this, because I want to add a forum and I want to be able to mess with customizing it.

**Note:** This guide is used for setting up on my web server which is running Debian 10.

## Prerequisites

- Hosting platform - either you can set up your own server (with port forwarding, DDNS or static IP) or using a hosting platform like vultr.com (which I use)
- Domain name - you can skip this and just go with your IP if using your own server (can also be a free or paid domain, where I use epik.com)
- Web server - Nginx, Apache, etc.
- Database - MySQL, MariaDB (can be none for testing)
- PHP - as Drupal being a PHP application, it uses PHP for everything (modules and so on)

If you want your site to be public and with your own domain, you will need to pay for a hosting service and a domain name registration.

In my case I use vultr.com for hosting and epik.com for the domain name registration and DNS setup, but you can use anything, like AWS for hosting and e.g. host gator for domain names.

If you decide on vultr.com, you can use my affiliate link

- [https://www.vultr.com/?ref=8910267](https://www.vultr.com/?ref=8910267)

And for a setup tutorial, check this blog

## AMP Stack

Simple and clear

**A**pache \
**M**ySQL \
**P**HP

This is noted in the official documentation, but the database and the web server can be different, like in my case. Let's continue.

## Setup the web server (nginx)

First I install nginx and enable the service

```
# apt install nginx
```

Enable and start the service

```
# systemctl enable nginx
# systemctl start nginx
```

The simple setup is complete and the configuration can be done later at the site installation stage.

## MariaDB setup

We need a database for storing our website's content, so let's create one

For this setup I will install MariaDB

```
# apt install mariadb-server mariadb-client
```

Setup the service

```
# systemctl enable mariadb
# systemctl start mariadb
```

If you're going to use the same database for production use (say yes to everything)

```
# mysql_secure_isntallation
```

- Alternatively skip this if just for testing or trying out

Create the actual database

```
# mysql -u root -p
```

Now we can start creating the database and the user.

```sql
sql> CREATE DATABASE drupal;
sql> CREATE USER 'drupaluser'@'localhost' IDENTIFIED BY 'new_password_here';
sql> GRANT ALL ON drupal.* TO 'drupaluser'@'localhost' IDENTIFIED BY 'user_password_here' WITH GRANT OPTION;
sql> FLUSH PRIVILEGES;
sql> EXIT;
```

- Create database
- Create a user for the database
- Grant all privileges for all tables to the new user
- Save changes and exit

## PHP

Nginx requires `php-fpm` to talk to communicate between Drupal and for Drupal to actually function.

Install the necessary packages first

```
# apt install php php-fpm php-gd php-common php-mysql php-apcu php-gmp php-curl php-intl php-mbstring php-xmlrpc php-gd php-xml php-cli php-zip -y
```

Configure `php-fpm`

```
# vim /etc/php/<VERSION>/fpm/php.ini
```

The main things to change are these, but there are more settings that can be changed, so explore if you are interested

```ini
date.timezone = Region/City  # Edit according to your timezone
cgi.fix_pathinfo = 0
memory_limit = 256M
upload_max_filesize = 64M
max_execution_time = 600
```

Enable `php-fpm` service, **this is version specific**, to find the version you can write `systemctl enable php<TAB>`, on `<TAB>` press tab for completion.

I had version 7.3 so for me it was this

```
# systemctl enable php7.3-fpm
# systemctl start php7.3-fpm
```

## Downloading Drupal

It is recommended by the developers to install it using `composer`

- **Note:** When installing Drupal you will notice a warning to use `roave/better-reflection`, this is only a false flag, because this is a note left by the author, but Drupal required the abandoned package, by it not being a drop in replacement and not extending a PHP class, taken from [here](https://www.drupal.org/project/drupal/issues/3180351)

> *The problem with roave/better-reflection for us is that it does not extend from PHP's builtin \ReflectionClass so it's not a drop in replacement. This also goes for PHPDocumentor's reflection library. This means that we will need extend / rebuild Simple annotation to work with them. The reason we use doctrine/reflection is that it let's us get doc comments without have to load code. This results in a massive memory saving when doing test discovery and also to a lesser extent for plugin discovery.*

After this, the Drupal installation should be in the `./web/core` folder, let's move to the next steps

## Configure Nginx

Nginx has the needed recipe for Drupal right [here](https://www.nginx.com/resources/wiki/start/topics/recipes/drupal/), but **change the php version to your php version in this**, because you will get 502 error, when Nginx can't communication with `php-fpm`.

All of the thing I had to change (The last one should be **your** PHP version for `php-fpm`)

- `server_name example.com` -> `server_name myserver.com www.myserver.com`
- `root /var/www/drupal8` -> `root /var/www/drupal/web`
- `fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;` -> `fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;`

```apache
server {
    server_name example.com;
    root /var/www/drupal8; ## <-- Your only path reference.

    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    # Very rarely should these ever be accessed outside of your lan
    location ~* \.(txt|log)$ {
        allow 192.168.0.0/16;
        deny all;
    }

    location ~ \..*/.*\.php$ {
        return 403;
    }

    location ~ ^/sites/.*/private/ {
        return 403;
    }

    # Block access to scripts in site files directory
    location ~ ^/sites/[^/]+/files/.*\.php$ {
        deny all;
    }

    # Allow "Well-Known URIs" as per RFC 5785
    location ~* ^/.well-known/ {
        allow all;
    }

    # Block access to "hidden" files and directories whose names begin with a
    # period. This includes directories used by version control systems such
    # as Subversion or Git to store control files.
    location ~ (^|/)\. {
        return 403;
    }

    location / {
        # try_files $uri @rewrite; # For Drupal <= 6
        try_files $uri /index.php?$query_string; # For Drupal >= 7
    }

    location @rewrite {
        #rewrite ^/(.*)$ /index.php?q=$1; # For Drupal <= 6
        rewrite ^ /index.php; # For Drupal >= 7
    }

    # Don't allow direct access to PHP files in the vendor directory.
    location ~ /vendor/.*\.php$ {
        deny all;
        return 404;
    }

    # Protect files and directories from prying eyes.
    location ~* \.(engine|inc|install|make|module|profile|po|sh|.*sql|theme|twig|tpl(\.php)?|xtmpl|yml)(~|\.sw[op]|\.bak|\.orig|\.save)?$|/(\.(?!well-known).*)|Entries.*|Repository|Root|Tag|Template|composer\.(json|lock)|web\.config$|/#.*#$|\.php(~|\.sw[op]|\.bak|\.orig|\.save)$ {
        deny all;
        return 404;
    }

    # In Drupal 8, we must also match new paths where the '.php' appears in
    # the middle, such as update.php/selection. The rule we use is strict,
    # and only allows this pattern with the update.php front controller.
    # This allows legacy path aliases in the form of
    # blog/index.php/legacy-path to continue to route to Drupal nodes. If
    # you do not have any paths like that, then you might prefer to use a
    # laxer rule, such as:
    #   location ~ \.php(/|$) {
    # The laxer rule will continue to work if Drupal uses this new URL
    # pattern with front controllers other than update.php in a future
    # release.
    location ~ '\.php$|^/update.php' {
        fastcgi_split_path_info ^(.+?\.php)(|/.*)$;
        # Ensure the php file exists. Mitigates CVE-2019-11043
        try_files $fastcgi_script_name =404;
        # Security note: If you're running a version of PHP older than the
        # latest 5.3, you should have "cgi.fix_pathinfo = 0;" in php.ini.
        # See http://serverfault.com/q/627903/94922 for details.
        include fastcgi_params;
        # Block httpoxy attacks. See https://httpoxy.org/.
        fastcgi_param HTTP_PROXY "";
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_intercept_errors on;
        # PHP 5 socket location.
        #fastcgi_pass unix:/var/run/php5-fpm.sock;
        # PHP 7 socket location.
        fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        try_files $uri @rewrite;
        expires max;
        log_not_found off;
    }

    # Fighting with Styles? This little gem is amazing.
    # location ~ ^/sites/.*/files/imagecache/ { # For Drupal <= 6
    location ~ ^/sites/.*/files/styles/ { # For Drupal >= 7
        try_files $uri @rewrite;
    }

    # Handle private files through Drupal. Private file's path can come
    # with a language prefix.
    location ~ ^(/[a-z\-]+)?/system/files/ { # For Drupal >= 7
        try_files $uri /index.php?$query_string;
    }

    # Enforce clean URLs
    # Removes index.php from urls like www.example.com/index.php/my-page --> www.example.com/my-page
    # Could be done with 301 for permanent or other redirect codes.
    if ($request_uri ~* "^(.*/)index\.php/(.*)") {
        return 307 $1$2;
    }
}
```

### SSL certificate

Setting up an HTTPS site is easy using `certbot`, which does everything automatically, also being able to extend the configuration to newly added sites.

Install `certbot`

```
# apt install nginx python-certbot-nginx
```

Simply run the following and go through the setup

```
# certbot --nginx
```

The next things to do are

- Enter the e-mail address
- Accept the terms of service
- Accept to redirect all HTTPS traffic

DONE! (almost)

## Installation (you can do this yourself :))

This step is a no-brainer, just visit your site and follow the installation instructions and you will be ready to go and create your site.

# Other related things?

## Updating to composer 2

This is not mandatory, but to be up to date, then you can do it.

The official documentation can be read [here](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos), I simply installed composer globally, by running a shell script

```bash
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === '756890a4488ce9024fc62c56153228907f1545c228516cbf63f885e036d37e9a59d27d63f46af1d4d07ee0f76181c7d3') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" php composer-setup.php php -r "unlink('composer-setup.php');"
```

- Script is from [downloads page](https://getcomposer.org/download/)

And then moving the generated `phar` file to `/usr/local/bin/composer`

## Backing up the website

For website backup I use a simple shell script where I leverage `rsync` (simple and useful tool)

```bash
rsync -uvrP --delete-after ~/backup/ root@example.com:/var/www/drupal
```

`rsync` needs to be installed on both machines, to install just use apt

```
# apt install rsync
```

## Troubleshooting

Good tip **Check the logs** -> `/var/log/nginx/error.log`

**502 Error**

I had this problem and the reason was that nginx wasn't able to communicate with the `php-fpm` socket and that's, because I didn't check the configuration that I pasted in and it had the wrong PHP version for the fpm, so when I changed the version from 7.1 to 7.3, everything went well

- Read about more reasons on this [site](https://www.datadoghq.com/blog/nginx-502-bad-gateway-errors-php-fpm/#nginx-cant-access-the-socket)

# Conclusion

Although I had problems with the setup first, the setup was not that difficult and those problems were mostly due to the fact that I didn't check much when configuring Nginx, so I made a guide including the resolutions and tips to the issues I encountered, you this helps.

# Links

Sites that helped me in the installation process:

- [How to Install Drupal with Nginx and Let's Encrypt SSL on Ubuntu 20.04 LTS](https://www.howtoforge.com/tutorial/how-to-install-drupal-with-nginx-and-ssl-on-ubuntu/)
- [Install Drupal CMS on Ubuntu 18.04 LTS with Nginx, MariaDB and PHP 7.1-FPM Support](https://websiteforstudents.com/install-drupal-cms-on-ubuntu-18-04-lts-beta-with-nginx-mariadb-and-php-7-1-fpm-support/)
- [How to Install Drupal 9 with Nginx and Let's Encrypt SSL on Debian 10 (Most relevant to me)](https://www.howtoforge.com/tutorial/debian-nginx-drupal/)
