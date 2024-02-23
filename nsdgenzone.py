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
CONFIG_FILE = "zones.conf"
ZONEFILE_SUFFIX = "zone"


def generate_zonefile(
    zonefile: Path, zonename: str, ipaddress: str, hosts: int
) -> None:
    """Generate a zone file."""
    lines: list[str] = []
    lines.append(f"$TTL {DEFAULT_TTL}")
    lines.append(
        f"{zonename} IN SOA ns.{zonename} hostmaster.{zonename} "
        f"2023100702 3600 900 604800 {SOA_MINIMUM}"
    )
    lines.append(f"@  IN NS ns.{zonename}")
    lines.append(f"ns IN A {ipaddress}")
    hostname_digit: int = ceil(log10(hosts))
    for i in range(0, hosts):
        lines.append(f"{i:0{hostname_digit}} IN A {ipaddress}")
    lines.append("")

    zonefile.write_text("\n".join(lines))


def generate_zone_config(zonename: str, zonefile: Path) -> str:
    """Generate zone configuration."""
    lines: list[str] = []
    lines.append("zone:")
    lines.append(f"        name: {zonename}")
    lines.append(f"        zonefile: {zonefile}")
    lines.append("")
    return "\n".join(lines)


def generate(
    zones: int,
    hosts: int,
    domainname: str,
    ipaddress: str,
    configdir: Path,
    zonesdir: Path,
) -> None:
    """Generate zone files and a config file."""
    if not domainname.endswith("."):
        domainname = f"{domainname}."

    subdomainname_digit: int = ceil(log10(zones))
    dir_digit: int = ceil(log10(MAX_FILE_IN_DIR))
    depth: int = floor((subdomainname_digit - 1) / 2)

    configlines: list[str] = []

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
        generate_zonefile(zonefile, zonename, ipaddress, hosts)

        zoneconfig: str = generate_zone_config(zonename, zonefile)
        configlines.append(zoneconfig)

    configfile: Path = configdir.joinpath(CONFIG_FILE)
    configfile.write_text("\n".join(configlines))


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
        "--hosts",
        dest="hosts",
        action="store",
        type=int,
        required=True,
        help="Number of hosts.",
    )
    parser.add_argument(
        "--domainname",
        dest="domainname",
        action="store",
        type=str,
        required=True,
        help="Base of domain name.",
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
        "--configdir",
        dest="configdir",
        action="store",
        type=Path,
        required=True,
        help="Config directory of NSD.",
    )
    parser.add_argument(
        "--zonesdir",
        dest="zonesdir",
        action="store",
        type=Path,
        required=True,
        help="Directory of zones directory.",
    )
    args: Namespace = parser.parse_args()
    if not args.configdir.is_dir():
        parser.error(f"argument --configdir: no such directory: '{args.configdir}'")
    if not args.zonesdir.is_dir():
        parser.error(f"argument --zonesdir: no such directory: '{args.zonesdir}'")

    generate(
        zones=args.zones,
        hosts=args.hosts,
        domainname=args.domainname,
        ipaddress=args.ipaddress,
        configdir=args.configdir,
        zonesdir=args.zonesdir,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
