dirarch - Archive a collection of files with the specified creation date or older,
          from the specified location.
          
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
          -l LOGFILE --logfile LOGFILE
                                Specify the the file name of the logfile. This file
                                will be copied to OUTDIRECTORY and the original
                                will be deleted after files are copied.

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
* Sun Dec 16 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.4 - Moved check for an empty file list before the
- creation of YYYY/MM/DD directories. No need to create
- if no data exists.
- Sorted files in output directory by the file cdate instead
- of the specified command line --date option. That way files
- older than --date will be sorted properly.
- Added --removefiles option - files copied successfully will
- be deleted from the source if this flag is set as TRUE. If
- the file move fails, the file (and all subsequent files)
- will not be deleted.
* Sun Apr 21 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.5 - Added -l, --logfile option to redirect STDOUT/
-   STDERR to a file, then copy that file to the OUTDIRECTORY
-   and delete the log.    
