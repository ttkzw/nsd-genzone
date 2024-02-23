# nsdgenzone

This is a project to generate test zones for NSD.

## Usage

```
usage: nsdgenzone [-h] --zones ZONES --hosts HOSTS --domainname DOMAINNAME 
                  --ipaddress IPADDRESS --configdir CONFIGDIR --zonesdir
                  ZONESDIR

options:
  -h, --help            show this help message and exit
  --zones ZONES         Number of zones.
  --hosts HOSTS         Number of hosts.
  --domainname DOMAINNAME
                        Base of domain name.
  --ipaddress IPADDRESS
                        IP address of name server.
  --configdir CONFIGDIR
                        Config directory of NSD.
  --zonesdir ZONESDIR   Directory of zones directory.
```

For example,

```
nsdgenzone --zones 1000000 --hosts 10 --domainname test. \
    --ipaddress 192.0.2.53 --configdir /etc/nsd/nsd.conf.d \
    --zonesdir /etc/nsd/zones 
```

