#!/usr/bin/env python3
"""nsdcheckzone"""

from __future__ import annotations
import sys
from argparse import ArgumentParser
from pathlib import Path
from math import ceil, floor, log10
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace

MAX_FILE_IN_DIR = 100
DEFAULT_TTL = 300
SOA_MINIMUM = 300
ZONEFILE_SUFFIX = "zone"


def generate_zonefile(zonefile: Path, zonename: str, ipaddress: str) -> None:
    """Generate a zone file."""
    lines: list[str] = []
    lines.append(f"$TTL {DEFAULT_TTL}")
    lines.append(
        f"{zonename} IN SOA ns.{zonename} hostmaster.{zonename} "
        f"2023100701 3600 900 604800 {SOA_MINIMUM}"
    )
    lines.append(f"@   IN  NS    ns.{zonename}")
    lines.append(f"ns  IN  A     {ipaddress}")
    lines.append(f'@   IN  TXT   "v=spf1 ip4:{ipaddress} -all"')
    lines.append(f"@   IN  A     {ipaddress}")
    lines.append(f"www IN  CNAME {zonename}")
    lines.append(f"@   IN  MX    10 mx.{zonename}")
    lines.append(f"mx  IN  A     {ipaddress}")
    lines.append("")
    zonefile.write_text("\n".join(lines))


def generate_querylines(zonename: str) -> list[str]:
    """Generate query data lines."""
    lines: list[str] = []
    lines.append(f"{zonename} A")
    lines.append(f"{zonename} TXT")
    lines.append(f"www.{zonename} A")
    lines.append(f"{zonename} MX")
    return lines


def generate_configlines(zonename: str, zonefile: Path) -> list[str]:
    """Generate configuration lines."""
    lines: list[str] = []
    lines.append("zone:")
    lines.append(f"        name: {zonename}")
    lines.append(f"        zonefile: {zonefile}")
    lines.append("")
    return lines


def generate(
    zones: int,
    domainname: str,
    ipaddress: str,
    zonesdir: Path,
    configfile: Path,
    queryfile: Path,
) -> None:
    """Generate zone files and a config file."""
    if not domainname.endswith("."):
        domainname = f"{domainname}."

    subdomainname_digit: int = ceil(log10(zones))
    dir_digit: int = ceil(log10(MAX_FILE_IN_DIR))
    depth: int = floor((subdomainname_digit - 1) / 2)

    configlines: list[str] = []
    querylines: list[str] = []

    for i in range(0, zones):
        zonename: str = f"{i:0{subdomainname_digit}}.{domainname}"

        dirname: Path = zonesdir
        for j in range(0, depth):
            dirname = dirname.joinpath(
                zonename[j * dir_digit : (j + 1) * dir_digit]  # noqa: E203
            )
        if not dirname.is_dir():
            dirname.mkdir(parents=True, exist_ok=True)

        zonefile: Path = dirname.joinpath(f"{zonename}{ZONEFILE_SUFFIX}")
        generate_zonefile(zonefile, zonename, ipaddress)

        configlines.extend(generate_configlines(zonename, zonefile))
        querylines.extend(generate_querylines(zonename))

    configfile.write_text("\n".join(configlines))

    querylines.append("")
    queryfile.write_text("\n".join(querylines))


def main() -> int:
    """main"""
    parser = ArgumentParser()
    parser.add_argument(
        "--zones",
        dest="zones",
        action="store",
        type=int,
        required=True,
        help="Number of zones.",
    )
    parser.add_argument(
        "--domainname",
        dest="domainname",
        action="store",
        type=str,
        required=True,
        default="test.",
        help="Domain name.",
    )
    parser.add_argument(
        "--ipaddress",
        dest="ipaddress",
        action="store",
        type=str,
        required=True,
        help="IP address of name server.",
    )
    parser.add_argument(
        "--zonesdir",
        dest="zonesdir",
        action="store",
        type=Path,
        required=True,
        help="Zones directory.",
    )
    parser.add_argument(
        "--configfile",
        dest="configfile",
        action="store",
        type=Path,
        default=Path("/etc/nsd/nsd.conf.d/zones.conf"),
        required=True,
        help="Configuration file for NSD zone clauses to be created.",
    )
    parser.add_argument(
        "--queryfile",
        dest="queryfile",
        action="store",
        type=Path,
        required=True,
        help="Data file to be created, used for dnsperf queries.",
    )
    args: Namespace = parser.parse_args()
    if not args.zonesdir.is_dir():
        parser.error(f"argument --zonesdir: no such directory: '{args.zonesdir}'")
    if args.configfile.is_file():
        parser.error(f"argument --configfile: already exists: '{args.configfile}'")
    if args.queryfile.is_file():
        parser.error(f"argument --queryfile: already exists: '{args.queryfile}'")

    generate(
        zones=args.zones,
        domainname=args.domainname,
        ipaddress=args.ipaddress,
        zonesdir=args.zonesdir,
        configfile=args.configfile,
        queryfile=args.queryfile,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
