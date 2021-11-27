# SNAPHU Windows Build

**THIS IS NOT AN OFFICIAL BUILD OF SNAPHU, I AM NOT AFFILIATED WITH THE STANFORD RADAR INTERFEROMETRY RESEARCH GROUP**
If you are a member of the SNAPHU development team, and would like me to take this repository down, please contact me
with further information at Marsfan@users.noreply.github.com. This will redirect to my personal email address, and I
will respond as soon as possible (less than a week).

SNAPHU is a tool used to unwrap phase images used radar interferometry.
It is developed by Stanford University, and the full source code can be found here:
[https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/](https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/)

The Stanford website does not contain pre-compiled binaries of this program. This is normally not a problem, as it can
be found in many Linux Software Repositories. However, this is not possible on Windows. While the European Space Agency
does provide a pre-built Windows binary (found here:
[http://step.esa.int/main/third-party-plugins-2/snaphu/](http://step.esa.int/main/third-party-plugins-2/snaphu/))
It is for a much older version of SNAPHU.

This repository uses GitHub Actions to check the SNAPHU website once a week, and if a new version of SNAPHU has been
released, it builds it and adds it to the releases pages.
