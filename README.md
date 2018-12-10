# dirarch
Archive a collection of files with the specified creation date in the specified location.

usage: dirarch.py --date <date> --indirectory <source directory> --outdirectory <destination directory>

Utility to move all files with a --date creation date (or older) in the 
source directory specified --indirectory to the destination directory 
specified by --outdirectory.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d DATE, --date DATE  Specifies the date of the files to be moved
  -i INDIRECTORY, --indirectory INDIRECTORY
                        Specifies the source directory of the files to be
                        moved
  -o OUTDIRECTORY, --outdirectory OUTDIRECTORY
                        Specifies the destination directory for the files.

%To Do List: (updated 2018-12-08)
1. Beef up error handling for cases when file copy fails.
2. Add functionality to delete the local files (from the inpath) once 
   successfully copied.

%changelog
* Thu Nov 29 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Initial commit, classes created and tested.
* Sat Dec 08 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.2 - Very limited functionality. It works, but needs tuning.
- Added usage text, todo list and changelog to this file.
* Sun Dec 09 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.3 - Added usage and changelog to main source file.
- Moved code to copy files to methode copy_files().
- Added code to verify base path exists.
- Added code to create YYYY/MM/DD directory structure if it
- does not exist.
