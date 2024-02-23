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

