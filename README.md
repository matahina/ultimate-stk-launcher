# Ultimate STK Launcher

**Version 0.4999RC2**

Where we are actually:

- [x] Working with git / tarball installations
- [x] Working with apt / rpm / system installations from distro package and using sudo thingie
- [ ] Working with flatpak (AAAAAAHHHHHHHH!!!!!!!! ~~and using sudo thingie~~) (maybit, pls try and tell me)
- [ ] Making *emoji_used* file and *sfx* files _per profile_ and not in general section
- [x] Making more than sfx files user-tweakable (because some files stay in data, some go into stk-assets from svn)
- [ ] Allowing to tweak profiles and to add new profiles (by example in case that both git and distro installations are available) without manually editing config file
- [x] IT CAN UPDATE YOUR ADDONS AND SHOW YOU FRESH ONES NOT DOWNLOADED YET

*See commit changelog for changelog.*

## Requirements

- Python 3
- Zenity
- Python pick (pip install pick)
- Optional: cowsay and lolcat

## Getting started

You're now gonna be able to launch STK with:

- either powerup file you need (and update these files automatically)
- debug mode you need (both drivelines and checklines if needed)
- ~~or from location (profile!) you want – either from git install or system install~~ (multi-profiles not yet fully implemented)

## Know where are your files stored

At first start, you'll be prompt about those files and directories:
- stk bin executable file
- data directory
- git directory (if u did install that way)
- assets directory (i.e. svn if u installed via git)

## Bonuses for geniuses

You can also tweak:
- if using KDE, and Openbox installed, enable a script to switch temporarily from KDE to Openbox while playing (and saving CPU×RAM)
- choose a specific emoji_used file you keep stored somewhere in your computer (will be used each time, you can still modify it later without moving file manually)
- change some sfx files — you need to have them stored in a directory reproducing the same structure _data_ (or _stk-assets_) have. 

## License
This bunch of crap code lines is GPL, free, public domain, have fun with it!!!

## Project status
"Active" or kinda.
