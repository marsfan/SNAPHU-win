from os import pardir
import requests
import re
import subprocess
from packaging.version import parse as parse_version
from pathlib import Path
import tarfile
import os

url = "https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/"


def parseChangelog():
    changelogRegex = re.compile(
        r"Notable changes in (v[\d.]+) since (v[\d.]+):\n-*((?:(?!Notable).)*)", flags=re.M | re.S)

    releaseNotesURL = url + "README_releasenotes.txt"
    releaseNotes = requests.get(releaseNotesURL).text

    foundNotes = changelogRegex.finditer(releaseNotes)

    parsedNotes = {parse_version(foundNote.group(1)): foundNote.group(3) for foundNote in foundNotes}

    latestVersion = max(parsedNotes)
    latestNotes = parsedNotes[latestVersion].strip().replace("\n", "\\n")

    builtVersions = Path("./builds").iterdir()
    try:
        newestbuilt = max((parse_version(version.name) for version in builtVersions))
        newVersion = True if latestVersion > newestbuilt else False
    except ValueError:
        newVersion = True

    print(f"::set-output name=version::{latestVersion}")
    print(f"::set-output name=notes::{latestNotes}")
    print(f"::set-output name=newVersion::{newVersion}")
    print(f"::set-output name=zipName::snaphu-v{latestVersion}.zip")

    return newVersion


def getSource():
    downloadRegex = re.compile(
        r"Download the full source distribution here: *\n<A NAME=\"SNAPHU\" HREF=\"(snaphu-v[\d\.]+tar\.gz)\">snaphu-v[\d\.]+tar\.gz</A>")

    homePage = requests.get(url).text

    fileToDownload = downloadRegex.search(homePage).group(1)

    downloadLink = url + fileToDownload

    with open("snaphu.tar.gz", "wb") as fileObj:
        fileObj.write(requests.get(downloadLink).content)

    with tarfile.open("snaphu.tar.gz") as tar:
        tar.extractall()

    os.rename(next(Path(".").glob("snaphu-v*")), "snaphu")


if __name__ == "__main__":
    if parseChangelog():
        getSource()
