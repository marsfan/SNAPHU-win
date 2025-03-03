#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads the source code for SNAPHU, but only if a new version has been released.

In addition to the above, this script generates output for Github Actions.
"""
import os
import re
import tarfile
from pathlib import Path

import requests
from packaging.version import parse as parse_version

# Get the repository name and owner from the GitHub actions environment variables.
repo_name = os.environ["GITHUB_REPOSITORY"]

# Github environment file
gh_env_file = os.environ["GITHUB_OUTPUT"]

# SNAPHU Homepage
URL = "https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/"

# SNAPHU release notes page
RELEASE_NOTES_URL = f"{URL}README_releasenotes.txt"

# Regex used to split up the changelog by version.
changelog_regex = re.compile(
    r"Notable changes in (v[\d.]+) since (v[\d.]+):\n-*((?:(?!Notable).)*)",
    flags=re.M | re.S
)

# Regex used to find the SNAPHU download link from the homepage
download_regex = re.compile(
    r"source distribution here: *\n<A NAME=\"SNAPHU\" HREF=\"(snaphu-v[\d\.]+tar\.gz)\">snaphu-v[\d\.]+tar\.gz</A>"
)


def write_to_github_env(name: str, value: str) -> None:
    """Write a new value to the github environment file.

    Arguments:
        name: The name of the environment variable to write
        value: The value of the environment variable.

    """
    with open(gh_env_file, "a", encoding="utf-8") as file:
        file.write(f"{name}={value}\n")


def parse_changelog() -> bool:
    """Download SNAPHU changelog, check if a new version has been released, and set workflow outputs.

    Returns:
        Boolean value that indicates if a new version of SNAPHU has been released

    """
    # Download the release notes, and split them up by version
    release_notes = requests.get(RELEASE_NOTES_URL, timeout=100).text
    found_notes = changelog_regex.finditer(release_notes)
    parsed_notes = {parse_version(found_note.group(1)): found_note.group(3)
                    for found_note in found_notes}
    # Get the release notes of the latest version of SNAPHU
    latest_version = max(parsed_notes)
    latest_notes = parsed_notes[latest_version].strip().replace("\n", "%0A")

    # Get the highest version number currently tagged in the GitHub repo
    tags = requests.get(
        f"https://api.github.com/repos/{repo_name}/git/matching-refs/tags",
        timeout=100
    ).json()
    parsed_versions = (
        parse_version(tag["ref"].split("/")[2]) for tag in tags)
    newest_built = max(parsed_versions)

    # Check if the newest version of SNAPHU is newer than what is built on the GitHub repo
    new_version = latest_version > newest_built

    # Set GitHub actions output values for use in later steps.
    write_to_github_env("version", str(latest_version))
    write_to_github_env("notes", latest_notes)
    write_to_github_env("newVersion", str(new_version))
    write_to_github_env("zipName", f"snaphu-v{latest_version}.zip")

    return new_version


def get_source() -> None:
    """Download the source for the newest version of SNAPHU."""

    # Find SNAPHU download link from the SNAPHU homepage
    home_page = requests.get(URL, timeout=100).text

    search_result = download_regex.search(home_page)
    if search_result is None:
        raise ValueError("Could not find download link")

    file_to_download = search_result.group(1)
    download_link = f"{URL}{file_to_download}"

    # Download the source for SNAPHU
    with open("snaphu.tar.gz", "wb") as file:
        file.write(requests.get(download_link, timeout=100).content)

    # Unzip SNAPHU source
    with tarfile.open("snaphu.tar.gz") as tar:
        tar.extractall(filter="data")

    # Rename the folder that we just unzipped to make running later actions eaiser.
    os.rename(next(Path(".").glob("snaphu-v*")), "snaphu")

    # Remove the -arch flag from the makefile, since this compiler does not
    # support it.
    makefile = Path("snaphu/src/Makefile")
    patched = makefile.read_text(
        "utf-8").replace("-arch x86_64 ", "-march=x86-64 ")
    makefile.write_text(patched, "utf-8")


if __name__ == "__main__":
    if parse_changelog():
        get_source()
