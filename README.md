# Ultimate STK Launcher

**Version 24.05.1**

```
This program is designed to work on Linux 64bit.

STK2 is now compatible!
```

## Requirements

- Bash
- Python3 and some packages
   - pick
   - lxml
   - setproctitle
   - pandas
- Optional tools
   - cowsay
   - lolcat
- If you want to install and compile from git repos
   - make sure you have all dependencies required as explained [here](https://github.com/supertuxkart/stk-code/blob/master/INSTALL.md)

## Getting started: several cases

### STK installed via package manager

You installed STK with distro package and you just have to fill the missing fields in the \[Profile_1\] section of `magic_config_orig.ini`. Remove \[Profile_2\] section and save the file as `magic_config.ini`.

- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.

**By example: Manjaro**
```
[Profile_1]
name = STK distro
bin_path = /usr/bin/supertuxkart
data_path = /usr/share/supertuxkart/data/
type = sudo
```

**By example: Ubuntu**
```
[Profile_1]
name = STK distro
bin_path = /usr/games/supertuxkart
data_path = /usr/share/games/supertuxkart/data/
type = sudo
```

Then start `ult_STK_launch.py`.

### STK local binary

You have a local copy (executable file) and you just have to fill the missing fields in the \[Profile_1\] section of `magic_config_orig.ini`. Change type field from *sudo* to *other*. Remove \[Profile_2\] section and save the file as `magic_config.ini`.

- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.

Then start `ult_STK_launch.py`.

### STK local git copy

You have a local copy of the git repo and you did compiled STK locally. You just have to fill the missing fields in the \[Profile_2\] section of `magic_config_orig.ini`. Remove \[Profile_1\] section and save the file as `magic_config.ini`.


- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.
- *git_path* is the absolute path of the directory where git repo is cloned (should normally ends with */stk-code/*)
- *svn_path* is the absolute path of the directory where svn repo is cloned (should normally ends with */stk-assets/*)

Then start `ult_STK_launch.py`.

### From scratch

Just start `ult_STK_launch.py`. Choose *Install last stable version (1.4)*. It will ask you where to download the tarball, extract it, and set it all up.

## Regular launch

When at least one profile is configured in `magic_config.ini` file, just start `ult_STK_launch.py`.

## Other STK copies

Either you feel okay to add sections in the `magic_config.ini` file if you have other copies of STK you would like to launch from this program, or you can also choose *Do another install* in the main menu to get several possibilities (including STK2 and [kimden version](https://github.com/kimden/stk-code)!)

## Bonus: change some files

All files supposed to be in `data` folder can be changed and used each time you run STK with this launcher. Original ones would be reverted when exiting.

Just put them in `my_files` folder. Be careful and respect the path and the name they have in `data` or `stk-assets` directories. Example:

```
my_files/
|
- emoji_used.txt
|
- sfx/
   |
   - appear.ogg
   - energy_bar_full.ogg
   - explosion.ogg
```

Original ones will be renamed with *_old* suffix and those ones put at their places. At the end, those ones will be removed from `data` and `stk-assets` and *_old* suffix removed from original ones so eveything will remain as before. Your custom files in `my_files` will remain unchanged and ready for next launch.

## License
This bunch of crap code lines is GPL, free, public domain, have fun with it!!!

## Project status
Active.
