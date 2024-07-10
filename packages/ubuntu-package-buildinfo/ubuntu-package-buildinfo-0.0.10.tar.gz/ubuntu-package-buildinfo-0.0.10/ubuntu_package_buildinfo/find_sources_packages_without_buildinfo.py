#!/usr/bin/env python3

import faulthandler
import hashlib
import logging
import sys

import click

from launchpadlib.launchpad import Launchpad
from launchpadlib.uris import service_roots

faulthandler.enable()

def _get_source_packages(archive, version, source_package_name, lp_series, component_name="main"):
    source_packages = archive.getPublishedSources(
        exact_match=True,
        version=version,
        source_name=source_package_name,
        order_by_date=True
    )
    return source_packages

def get_buildinfo(
    package_series, package_name, package_version, component_name="main"):

    # Log in to launchpad annonymously - we use launchpad to find
    # the package publish time
    launchpad = Launchpad.login_anonymously(
        "ubuntu-package-buildinfo", service_root=service_roots["production"], version="devel"
    )

    ubuntu = launchpad.distributions["ubuntu"]

    archive = ubuntu.main_archive

    lp_series = ubuntu.getSeries(name_or_version=package_series)
    binary_package_build_found = False
    source_packages = _get_source_packages(archive, package_version, package_name, lp_series, component_name)
    if len(source_packages):
        for source_package in source_packages:
            # print(source_package.distro_series_link)
            # print(source_package.binaryFileUrls())
            distro_series = launchpad.load(source_package.distro_series_link)
            binaries = source_package.getPublishedBinaries(active_binaries_only=False)
            if len(binaries):

                binary_package_build_found = True
                print(
                    f"INFO######: \tFound binary package from source package "
                    f"{package_name} version {package_version} in {distro_series.name}."
                )
                for binary in binaries:
                    # print(binary)
                    print(binary.build_link)
            else:
                print(
                    f"**********WARNING: \tNo binary builds found for source package {package_name} version {package_version} in {distro_series.name}."
                )
            source_package_builds = source_package.getBuilds()
            if len(source_package_builds):
                for source_package_build in source_package_builds:
                    print(source_package_build)
                    print(source_package_build.current_source_publication_link)
                    print(source_package_build.pocket)
                    print(source_package_build.source_package_version)
                    print(source_package_build.source_package_name)
                    print(source_package_build.arch_tag)
                    print(source_package_build.getLatestSourcePublication())
                binary_package_build_found = True
                print(
                    f"INFO: \tFound binary package from source package "
                    f"{package_name} version {package_version} in {distro_series.name}."
                )
            else:
                print(
                    f"**********WARNING: \tNo binary builds found for source package {package_name} version {package_version} in {distro_series.name}."
                )
        source_package = source_packages[0]
        binaries = source_package.getPublishedBinaries()
        if len(binaries):
            binary_package_build_found = True
            print(
                f"INFO: \tFound binary package from source package "
                f"{package_name} version {package_version} in {package_series}."
            )
        else:
            print(
                f"**********WARNING: \tNo binary builds found for source package {package_name} version {package_version} in {package_series}."
            )
    if binary_package_build_found and len(binaries):
        binary_build_link = binaries[0].build_link
        binary_build = launchpad.load(binary_build_link)
        buildinfo_url = binary_build.buildinfo_url
        if buildinfo_url is None:
            print(f"**********ERROR: \tNo buildinfo found for {package_name} version {package_version} in {package_series}. See {binary_build_link} for more details. Source package {binary_build.source_package_name} version {binary_build.source_package_version}.")
    else:
        print(
            f"**********ERROR: \tNo builds found for {package_name} version {package_version} in {package_series}."
        )


@click.command()
@click.option(
    "--series",
    help="The Ubuntu series eg. '20.04' or 'focal'.",
    required=True,
)
@click.option(
    "--package-name",
    help="Package name",
    required=True,
)
@click.option(
    "--package-version",
    help="Package version",
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
def find_sources_packages_without_buildinfo(
    ctx, series, package_name, package_version, logging_level, component):
    # type: (Dict, Text, Text,Text, Bool, Text, Optional[Text]) -> None

    # We log to stderr so that a shell calling this will not have logging
    # output in the $() capture.
    level = logging.getLevelName(logging_level)
    logging.basicConfig(level=level, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")

    get_buildinfo(series, package_name, package_version, component)


if __name__ == "__main__":
    find_sources_packages_without_buildinfo(obj={})
