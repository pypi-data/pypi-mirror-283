#!/usr/bin/env python3

import faulthandler
import functools
import logging
import sys

import click

from debian import debian_support
from launchpadlib.launchpad import Launchpad
from launchpadlib.uris import service_roots

faulthandler.enable()


def _get_source_packages(archive, lp_series, component="main"):
    source_packages = archive.getPublishedSources(
        exact_match=True,
        distro_series=lp_series,
        component_name=component,
        status="Published",
    )
    return source_packages


def _get_packages_in_archive(package_series, component="main"):
    """
    List all packages and versions in the main archive
    """
    # Log in to launchpad annonymously - we use launchpad to find
    # the package publish time
    launchpad = Launchpad.login_anonymously(
        "published-source-packages-in-archive", service_root=service_roots["production"], version="devel"
    )

    ubuntu = launchpad.distributions["ubuntu"]

    archive = ubuntu.main_archive

    lp_series = ubuntu.getSeries(name_or_version=package_series)

    # attempt to find all binary package names
    source_packages = _get_source_packages(
        archive, lp_series, component,
    )

    all_source_packages = {}
    if len(source_packages):
        for source_package in source_packages:
            if source_package.source_package_name in all_source_packages:
                all_source_packages[source_package.source_package_name].append(source_package.source_package_version)
            else:
                all_source_packages[source_package.source_package_name] = [source_package.source_package_version]

    # we only need to check the latest version of each package so we can use debian's version comparison
    for source_package_name, source_package_versions in all_source_packages.items():
        # find the latest version in the list
        sorted_build_package_versions = sorted(source_package_versions, reverse=True,
                                               key=functools.cmp_to_key(debian_support.version_compare))
        latest_version = sorted_build_package_versions[0]

        print(
            f"{source_package_name}\t{latest_version}"
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
    "--component",
    type=click.Choice(["main", "universe", "restricted", "multiverse"]),
    required=False,
    default="main",
    help="Which archive component do you wish to query.",
    show_default=True,
)
@click.pass_context
def get_source_packages_in_archive(
    ctx, series, logging_level, component):
    # type: (Dict, Text, Text,Text, Bool, Text, Optional[Text]) -> None

    # We log to stderr so that a shell calling this will not have logging
    # output in the $() capture.
    level = logging.getLevelName(logging_level)
    logging.basicConfig(level=level, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")

    _get_packages_in_archive(series, component)


if __name__ == "__main__":
    get_source_packages_in_archive(obj={})
