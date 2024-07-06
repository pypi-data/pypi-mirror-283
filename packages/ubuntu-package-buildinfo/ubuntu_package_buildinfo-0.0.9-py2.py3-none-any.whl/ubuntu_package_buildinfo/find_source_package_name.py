#!/usr/bin/env python3

import faulthandler
import hashlib
import logging
import sys

import click

from launchpadlib.launchpad import Launchpad
from launchpadlib.uris import service_roots

faulthandler.enable()


def _get_binary_package(archive, lp_arch_series, binary_package_name, binary_package_version):
    binaries = archive.getPublishedBinaries(
        exact_match=True,
        distro_arch_series=lp_arch_series,
        ordered=False,
        binary_name=binary_package_name,
        # version=binary_package_version,
    )
    return binaries


def _find_source_package_name(
    package_series, package_name, package_version, package_architecture="amd64"):
    """
    List all packages and versions in the main archive
    """
    # Log in to launchpad annonymously - we use launchpad to find
    # the package publish time
    launchpad = Launchpad.login_anonymously(
        "ubuntu-package-buildinfo", service_root=service_roots["production"], version="devel"
    )

    ubuntu = launchpad.distributions["ubuntu"]

    archive = ubuntu.main_archive

    lp_series = ubuntu.getSeries(name_or_version=package_series)
    lp_arch_series = lp_series.getDistroArchSeries(archtag=package_architecture)

    # attempt to find all binary package names
    binaries = _get_binary_package(
        archive, lp_arch_series, package_name, package_version
    )

    if len(binaries):
        binary_package = binaries[0]
        source_package_name = binary_package.source_package_name
        source_package_version = binary_package.source_package_version
        print(f'{source_package_name}\t{source_package_version}')


@click.command()
@click.option(
    "--series",
    help="The Ubuntu series eg. '20.04' or 'focal'.",
    required=True,
)
@click.option(
    "--logging-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    required=False,
    default="ERROR",
    help="How detailed would you like the output.",
    show_default=True,
)
@click.option(
    "--package-architecture",
    help="The architecture to use when querying package "
    "version in the archive. The default is amd64. ",
    required=True,
    default="amd64",
    show_default=True,
)
@click.option(
    "--package-name",
    help="The name of the binary package",
    required=True,
)
@click.option(
    "--package-version",
    help="The version of the binary package",
    required=True,
)
@click.pass_context
def find_source_package_name(
    ctx, series, logging_level, package_architecture, package_name, package_version):
    # type: (Dict, Text, Text,Text, Bool, Text, Optional[Text]) -> None

    # We log to stderr so that a shell calling this will not have logging
    # output in the $() capture.
    level = logging.getLevelName(logging_level)
    logging.basicConfig(level=level, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")

    _find_source_package_name(series, package_name, package_version, package_architecture)


if __name__ == "__main__":
    find_source_package_name(obj={})
