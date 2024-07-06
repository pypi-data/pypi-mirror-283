#!/usr/bin/env python3

import faulthandler
import hashlib
import logging
import sys

import click

from launchpadlib.launchpad import Launchpad
from launchpadlib.uris import service_roots

faulthandler.enable()


def _get_binary_packages(archive, lp_arch_series):
    binaries = archive.getPublishedBinaries(
        exact_match=True,
        distro_arch_series=lp_arch_series,
        ordered=False,
        status="Published",
        component_name="multiverse",
    )
    return binaries

def get_packages_in_main_manifest(
    package_series, package_architecture="amd64"):
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
    binaries = _get_binary_packages(
        archive, lp_arch_series
    )

    if len(binaries):
        for binary in binaries:
            print(
                f"{binary.binary_package_name}\t{binary.binary_package_version}"
            )


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
@click.pass_context
def ubuntu_package_buildinfo(
    ctx, series, logging_level, package_architecture):
    # type: (Dict, Text, Text,Text, Bool, Text, Optional[Text]) -> None

    # We log to stderr so that a shell calling this will not have logging
    # output in the $() capture.
    level = logging.getLevelName(logging_level)
    logging.basicConfig(level=level, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")

    get_packages_in_main_manifest(series, package_architecture)


if __name__ == "__main__":
    ubuntu_package_buildinfo(obj={})
