# nsdgenzone

This is a project to generate test zones for NSD.

## Usage

```
usage: nsdgenzone.py [-h] --zones ZONES --domainname DOMAINNAME --ipaddress \
                     IPADDRESS --zonesdir ZONESDIR --configfile CONFIGFILE \
                     --queryfile QUERYFILE

options:
  -h, --help            show this help message and exit
  --zones ZONES         Number of zones.
  --domainname DOMAINNAME
                        Domain name.
  --ipaddress IPADDRESS
                        IP address of name server.
  --zonesdir ZONESDIR   Directory of zones directory.
  --configfile CONFIGFILE
                        The configuration file for the NSD zone clause to be created.
  --queryfile QUERYFILE
                        The data file to be created, used for dnsperf queries.
```

For example,

```
nsdgenzone --zones 1000000 --domainname test. --ipaddress 192.0.2.53 \
    --zonesdir /etc/nsd/zones --configfile /etc/nsd/nsd.conf.d/zones.conf \
    --queryfile querydata.txt
```

## TIPS

### systemd

If NSD startup times out in systemd, increase the TimeoutStartSec value as follows:

```
$ sudo systemctl edit nsd.service 
```

```
[Service]
TimeoutStartSec=600
```

### NSD

/etc/nsd/nsd.conf.d/server.conf

```
server:
        interface: 192.0.2.53
        port: 53
```

### Unbound

/etc/unbound/unbound.conf.d/test.conf

```
server:
        local-zone: test. nodefault

stub-zone:
        name: test.
        stub-addr: 192.0.2.53@53
```
