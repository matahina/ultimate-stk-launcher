# Ultimate STK Launcher

**Version 24.06**

> This program is designed to work on Linux 64bit.
>
> STK2 is now compatible!

## Requirements

- On Ubuntu:
```
sudo apt install python3-questionary python3-lxml python3-setproctitle python3-pandas cowsay lolcat
```

- On Arch/Manjaro:
```
sudo pacman -S python3-lxml python3-setproctitle python3-pandas cowsay lolcat
```
```
yay -S python3-questionary
```

- If you want to install and compile from git repos
   - make sure you have all dependencies required as explained [here](https://github.com/supertuxkart/stk-code/blob/master/INSTALL.md)

## Everyday usage

Just start `ult_STK_launch.py`.

Choose *Install last stable version (1.4)*. It will ask you where to download the tarball, extract it, and set it all up.

See how to configure below if you don't want the automatic STK installation process.


## Getting started: several cases

### STK installed via package manager (apt, pacman...)

You just have to fill the missing fields in the \[Profile_1\] section of `magic_config_orig.ini`.

Remove \[Profile_2\] section and save the file as `magic_config.ini`.

- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.

**Manjaro**
```
[Profile_1]
name = STK distro
bin_path = /usr/bin/supertuxkart
data_path = /usr/share/supertuxkart/data/
type = sudo
```

**Ubuntu**
```
[Profile_1]
name = STK distro
bin_path = /usr/games/supertuxkart
data_path = /usr/share/games/supertuxkart/data/
type = sudo
```

### STK local binary

You have a local copy (executable file) of STK.

You just have to fill the missing fields in the \[Profile_1\] section of `magic_config_orig.ini`.

Change type field from *sudo* to *other*. Remove \[Profile_2\] section and save the file as `magic_config.ini`.

- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.


### STK local git copy

You have a local copy of the git repo and you did compiled STK locally.

You just have to fill the missing fields in the \[Profile_2\] section of `magic_config_orig.ini`.

Remove \[Profile_1\] section and save the file as `magic_config.ini`.


- *bin_path* is the absolute path of the executable itself.
- *data_path* is the absolute path of the *data* directory. Don't forget to add "/" at the end.
- *git_path* is the absolute path of the directory where git repo is cloned (should normally ends with */stk-code/*)
- *svn_path* is the absolute path of the directory where svn repo is cloned (should normally ends with */stk-assets/*)


### Other cases

If you have other copies of STK you would like to launch from this program, you should feel okay to add sections in the `magic_config.ini` file.

You can also choose *Do another install* in the main menu to get several possibilities (including STK2 and [kimden version](https://github.com/kimden/stk-code)!)


## Bonus: change some files

All files supposed to be in `data` folder can be changed and used each time you run STK with this launcher.

Just put them in `my_files` folder. Be careful and respect the paths and the names they have in `data` or `stk-assets` directories.

Example:

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

Original files will be renamed with *_old* suffix.

Your files will be copied in the `data` or `assets` location.

When exiting STK, your custom files will be removed from `data` or `stk-assets` and *_old* suffix removed from original ones so everything will remain as before.

Your custom files will remain in `my_files` and be ready for next launch.

## License
This bunch of crap code lines is GPL, free, public domain, have fun with it!!!

## Project status
Active.
