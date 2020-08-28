import re
import subprocess
from packaging.version import parse as parse_version

changelogRegex = re.compile(r"Notable changes in (v[\d.]+) since (v[\d.]+):\n-*((?:(?!Notable).)*)", flags=re.M | re.S)

with open("snaphu/README_releasenotes.txt") as fileobj:
    releaseNotes = fileobj.read()

foundNotes = changelogRegex.finditer(releaseNotes)

parsedNotes = {parse_version(foundNote.group(1)):foundNote.group(3) for foundNote in foundNotes}

latestVersion = max(parsedNotes)
latestNotes = parsedNotes[latestVersion].strip().replace("\n", "\\n")

subprocess.Popen(f"echo \"::set-output name=version::{latestVersion}\"", shell=True).wait()
subprocess.Popen(f"echo \"::set-output name=notes::{latestNotes}\"", shell=True).wait()



pass
