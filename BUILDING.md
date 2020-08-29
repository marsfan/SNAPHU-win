# Build Process

This is the process that I used on a 64bit Windows 10 machine to manually build SNAPHU for native Windows use.
The GitHub Actions script does this exact same process.

1. Download the SNAPHU binaries from [https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/](https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/)
2. Download and install MSYS2 using the instructions on [https://www.msys2.org/](https://www.msys2.org/)
3. Open a terminal for MSYS2
   _Note_ From until the end of these steps, all commands are run in the MSYS2 terminal.
4. Update all programs in MSYS2 and install `gcc` and `make` with `pacman -Syu gcc make`

   _Note_ If MSYS2 says it has to close when during the update and install process, re-open it and run the update
   command again to make sure everything installed right. It acted a bit strange for me.

5. `cd` to `snaphu-vX.X.X/src` (where `X.X.X` is the version of SNAPHU you are compiling)
6. Run `make`
7. `cd` to `../bin`
8. Copy `msys-2.0.dll` into the current directory with `cp /usr/bin/msys-2.0.dll .`

This is all that it took me to compile SNAPHU. `snaphu.exe` can now be placed in any folder on your compututer, but
make sure that you move `msys-2.0.dll` as well, or it will not work.