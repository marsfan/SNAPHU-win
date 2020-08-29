#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads the source code for SNAPHU, but only if a new version has been released.

In addition to the above, this script generates output for Github Actions.
"""
from typing import Dict, Iterable
import requests
import re
from packaging.version import parse as parse_version
from packaging.version import Version
from pathlib import Path
import tarfile
import os

# Get the repository name and owner from the GitHub actions environment variables.
repoName = os.environ["GITHUB_REPOSITORY"]

# SNAPHU Homepage
url = "https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/"

# SNAPHU release notes page
releaseNotesURL = url + "README_releasenotes.txt"

# Regex used to split up the changelog by version.
changelogRegex = re.compile(
    r"Notable changes in (v[\d.]+) since (v[\d.]+):\n-*((?:(?!Notable).)*)", flags=re.M | re.S)

# Regex used to find the SNAPHU download link from the homepage
downloadRegex = re.compile(
    r"source distribution here: *\n<A NAME=\"SNAPHU\" HREF=\"(snaphu-v[\d\.]+tar\.gz)\">snaphu-v[\d\.]+tar\.gz</A>")


def parseChangelog() -> bool:
    """Download SNAPHU changelog, check if a new version has been released, and set workflow outputs.

    Returns:
        Boolean value that indicates if a new version of SNAPHU has been released

    """
    # Download the release notes, and split them up by version
    releaseNotes: str = requests.get(releaseNotesURL).text
    foundNotes = changelogRegex.finditer(releaseNotes)
    parsedNotes: Dict[Version, str] = {parse_version(foundNote.group(1)): foundNote.group(3)
                                       for foundNote in foundNotes}
    # Get the release notes of the latest version of SNAPHU
    latestVersion = max(parsedNotes)
    latestNotes = parsedNotes[latestVersion].strip().replace("\n", "%0A")

    # Get the highest version number currently tagged in the GitHub repo
    tags = requests.get(f"https://api.github.com/repos/{repoName}/git/matching-refs/tags").json()
    parsedVersions: Iterable[Version] = (parse_version(tag["ref"].split("/")[2]) for tag in tags)
    newestBuilt: Version = max(parsedVersions)

    # Check if the newest version of SNAPHU is newer than what is built on the GitHub repo
    newVersion = True if latestVersion > newestBuilt else False

    # Set GitHub actions output values for use in later steps.
    print(f"::set-output name=version::{latestVersion}")
    print(f"::set-output name=notes::{latestNotes}")
    print(f"::set-output name=newVersion::{newVersion}")
    print(f"::set-output name=zipName::snaphu-v{latestVersion}.zip")

    return newVersion


def getSource() -> None:
    """Download the source for the newest version of SNAPHU."""

    # Find SNAPHU download link from the SNAPHU homepage
    homePage = requests.get(url).text
    fileToDownload = downloadRegex.search(homePage).group(1)
    downloadLink = url + fileToDownload

    # Download the source for SNAPHU
    with open("snaphu.tar.gz", "wb") as fileObj:
        fileObj.write(requests.get(downloadLink).content)

    # Unzip SNAPHU source
    with tarfile.open("snaphu.tar.gz") as tar:
        tar.extractall()

    # Rename the folder that we just unzipped to make running later actions eaiser.
    os.rename(next(Path(".").glob("snaphu-v*")), "snaphu")


if __name__ == "__main__":
    if parseChangelog():
        getSource()
