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


def _get_binary_package_publishing_histories(archive, version, binary_package_name):
    binary_publish_histories = archive.getPublishedBinaries(
        exact_match=True,
        version=version,
        binary_name=binary_package_name,
        order_by_date=True,
    )
    return binary_publish_histories

def download_deb(
    package_name, package_version, package_architecture="amd64", fallback=False, series=None):
    """
    Download a deb from launchpad for a specific package version and architecture
    """
    if f":{package_architecture}" in package_name:
        # strip the architecture from the package name if it is present
        package_name = package_name.replace(f":{package_architecture}", "")
    # Log in to launchpad annonymously - we use launchpad to find
    # the package publish time
    launchpad = Launchpad.login_anonymously(
        "ubuntu-package-download-deb", service_root=service_roots["production"], version="devel"
    )

    ubuntu = launchpad.distributions["ubuntu"]

    archive = ubuntu.main_archive

    # lp_series = ubuntu.getSeries(name_or_version=package_series)
    # lp_arch_series = lp_series.getDistroArchSeries(archtag=package_architecture)

    # Is this a series specific version
    deb_version = debian_support.Version(package_version)
    binary_publishing_histories = _get_binary_package_publishing_histories(
        archive, package_version, package_name
    )

    if len(binary_publishing_histories):
        # we don't filter the getPublishedBinaries query by distro_arch_series as
        # the version we are querying might have been built for a previous release
        # instead we can filter the builds on the arch tag
        architecture_all_arch_tag = "amd64"
        architecture_all_build = None
        architecture_all_build_distro_series = None
        architecture_build = None
        architecture_build_distro_series = None
        for binary_publishing_history in binary_publishing_histories:
            binary_build_link = binary_publishing_history.build_link
            try:
                binary_build = launchpad.load(binary_build_link)
                binary_build_distro_arch_series_link = binary_publishing_history.distro_arch_series_link
                binary_build_distro_arch_series = launchpad.load(binary_build_distro_arch_series_link)
                binary_build_distro_series_link = binary_build_distro_arch_series.distroseries_link
                binary_build_distro_series = launchpad.load(binary_build_distro_series_link)
                if binary_build.arch_tag == architecture_all_arch_tag:
                    # This will be our fallback if we do not find a build for the specified architecture
                    architecture_all_build = binary_build
                    architecture_all_build_distro_series = binary_build_distro_series
                if binary_build.arch_tag == package_architecture:
                    architecture_build = binary_build
                    architecture_build_distro_series = binary_build_distro_series
                    print(
                        f"INFO: \tFound binary package "
                        f"{package_name} {package_architecture} version {package_version} in {binary_build_distro_series.name} {binary_build.arch_tag} build."
                    )
                    break
            except ValueError:
                print(
                    f"**********ERROR(Exception): \tCould not load binary build link {binary_build_link}."
                )

        if architecture_build is None and architecture_all_build is not None:
            architecture_build = architecture_all_build
            architecture_build_distro_series = architecture_all_build_distro_series
            print(
                f"INFO: \tNo build found for architecture {package_architecture} using {architecture_all_arch_tag} instead. This will occur if there is no build for the specified architecture and the amd64 architecture build is used instead. - when `Architecture: all` is used for example")

        if architecture_build:
            binary_build_urls = binary_publishing_history.binaryFileUrls()
            for binary_build_url in binary_build_urls:
                binary_build_filename = binary_build_url.split("/")[-1]
                with open(f"{binary_build_filename}", "wb") as f:
                    f.write(launchpad._browser.get(binary_build_url))
                    print(f"INFO: \tDownloaded {binary_build_filename} from {architecture_build_distro_series.name} {architecture_build.arch_tag} build.")
        else:
            print(
                f"ERROR: \tCould not find binary package {package_name} {package_architecture} version {package_version}."
            )
    else:
        if fallback:
            print(
                f"WARNING: \tCould not find binary package {package_name} {package_architecture} version {package_version}."
            )
            print(
                f"INFO: \tFALLBACK - Attempting to find and download the next version of "
                f"{package_name} {package_architecture}..."
            )
            binary_publishing_histories_all_versions = _get_binary_package_publishing_histories(
                archive, None, package_name
            )
            if len(binary_publishing_histories_all_versions):
                next_binary_package_version = None
                build_package_versions = []
                for binary_publishing_history in binary_publishing_histories_all_versions:
                    build_package_version = binary_publishing_history.binary_package_version
                    build_package_versions.append(build_package_version)

                # now sort the versions and find the next version
                sorted_build_package_versions = sorted(build_package_versions, reverse=True,
                                                       key=functools.cmp_to_key(debian_support.version_compare))
                for build_package_version in sorted_build_package_versions:

                    version_comparison = debian_support.version_compare(build_package_version,
                                                                        package_version)
                    if version_comparison > 0:
                        """
                        > 0 The version build_package_version is greater than version package_version.

                        = 0 Both versions are equal.

                        < 0 The version current_package_version is less than version previous_package_version.
                        """
                        next_binary_package_version = build_package_version
                    else:
                        # This is a version equal to or lower than the current version so we can break from the
                        # loop knowing that we now know the next newest version that has a build publishing history
                        break

                if next_binary_package_version:
                    print(
                        f"INFO: \tFALLBACK - Found next version {next_binary_package_version} of {package_name} {package_architecture} (queried version was {package_version})."
                    )
                    download_deb(
                        package_name, next_binary_package_version, package_architecture
                    )
            else:
                print(
                    f"ERROR: \tCould not find any build publishing history for {package_name}."
                )
        else:
            print(
                f"ERROR: \tCould not find binary package {package_name} {package_architecture} version {package_version}."
            )




@click.command()
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
    "--package-architecture",
    help="The architecture of the package you want to download.",
    required=True,
    default="amd64",
    show_default=True,
)
@click.option(
    "--fallback",
    is_flag=True,
    help="If the exact version cannot be found should we download the next version?",
    default=False,
    show_default=True,
)
@click.option(
    "--series",
    help="The Ubuntu series eg. '20.04' or 'focal'.",
    required=False,
)
@click.pass_context
def ubuntu_package_download_deb(
    ctx, package_name, package_version, logging_level, package_architecture, fallback, series):

    # We log to stderr so that a shell calling this will not have logging
    # output in the $() capture.
    level = logging.getLevelName(logging_level)
    logging.basicConfig(level=level, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")

    download_deb(package_name, package_version, package_architecture, fallback, series)


if __name__ == "__main__":
    ubuntu_package_download_deb(obj={})
