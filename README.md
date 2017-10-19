

To be able to send mail with this program, you will need fully working SMTP -server running on background.
Postfix was used for testing this program.

There are multiple sources which can guide for successful configuration.

Some important parts in configration:

**Make sure your Linux hostname is correct:**
```
nicce@mail:~$ hostname
deeplylost.tech
```

/etc/hosts and /etc/hostname should contain proper information

**Be sure about virtuals in Postfix configuration, they are your email accounts.**
```
> nicce@mail:~$ sudo cat /etc/postfix/virtual
> nicce@deeplylost.tech nicce
> nicce@mail.deeplylost.tech nicce
> niklas.saari@deeplylost.tech nicce
```
**Here is my Postfix configuration file:**

```
# See /usr/share/postfix/main.cf.dist for a commented, more complete version


# Debian specific:  Specifying a file name will cause the first
# line of that file to be used as the name.  The Debian default
# is /etc/mailname.
myorigin = /etc/mailname
mydomain = deeplylost.tech
biff = no

# appending .domain is the MUA's job.
append_dot_mydomain = no

# Uncomment the next line to generate "delayed mail" warnings
#delay_warning_time = 4h

readme_directory = no

# TLS parameters
smtp_tls_security_level = may
smtp_tls_loglevel = 1
smtpd_tls_cert_file=/etc/postfix/ssl/cert.pem
smtpd_tls_key_file=/etc/postfix/ssl/privkey.pem
smtpd_use_tls=yes
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache

# See /usr/share/doc/postfix/TLS_README.gz in the postfix-doc package for
# information on enabling SSL in the smtp client.

myhostname = deeplylost.tech
smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
mydestination = localhost $myhostname mail.$myhostname
#relayhost = $mydomain
mynetworks = 127.0.0.0/8
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = all
home_mailbox = Maildir/
virtual_alias_maps = hash:/etc/postfix/virtual
smtpd_sasl_local_domain =
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
broken_sasl_auth_clients = yes
smtpd_relay_restrictions = permit_mynetworks, reject_unauth_destination
smtpd_client_restrictions =permit_sasl_authenticated,permit_mynetworks,reject_unauth_destination, reject_non_fqdn_helo_hostname, permit
smtpd_recipient_restrictions=permit_sasl_authenticated,permit_mynetworks,reject_unauth_destination, permit

smtpd_tls_security_level = may
smtpd_tls_auth_only = no
smtp_tls_note_starttls_offer = yes

# DKIM
milter_default_action = accept
milter_protocol = 2
smtpd_milters = inet:localhost:12345
non_smtpd_milters = inet:localhost:12345
```
