#!/usr/bin/python
"""
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
"""

import argparse
import os, sys, time, shutil
from stat import S_ISREG, ST_CTIME, ST_MODE
#import datetime
#from dateutil.parser import parse

VERSION = '0.0.3'

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        usageSTG = ('dirarch.py --date <date> '
                    '--indirectory <source directory> '
                    '--outdirectory <destination directory>')
        aboutSTG = ('Utility to move all files with a --date creation date (or older) in the '
                    'source directory specified --indirectory to the destination directory '
                    'specified by --outdirectory.')

        parser = argparse.ArgumentParser(usage=usageSTG,
                                         description=aboutSTG,
                                         epilog='That\'s all folks!')
        parser.add_argument('-v', '--version', action='version', version = VERSION)
        parser.add_argument("-d", "--date", default='TODAY',
            help="Specifies the date of the files to be moved")
        parser.add_argument("-i", "--indirectory", default='./',
            help="Specifies the source directory of the files to be moved")
        parser.add_argument("-o", "--outdirectory", default='./',
            help="Specifies the destination directory for the files.")
        return parser.parse_args()

class DirArch():

    def __init__(self):
        if __name__ == '__main__':
            self.appMain()
        
    def get_inpath(self, args):
        path = ""
        path = args.args.indirectory
        return path
    
    def get_outpath(self, args):
        path = ""
        path = args.args.outdirectory
        return path
    
    def get_target_date(self, args):
        temp_date = ""
        temp_date = args.args.date
        if ('TODAY' in temp_date):
           target_date = time.mktime(time.localtime())
        else:
           target_date = time.mktime(time.strptime(temp_date, '%Y-%m-%d-%H:%M'))
        return int(target_date)
        
    def get_file_list(self, inpath):
        #all entries in the directory w/ stats
        data = (os.path.join(inpath, fn) for fn in os.listdir(inpath))
        data = ((os.stat(path), path) for path in data)

        # regular files, insert creation date
        data = ((stat[ST_CTIME], path)
              for stat, path in data if S_ISREG(stat[ST_MODE]))
        return data

    def set_fullPath(self, basepath, tdate):
        retpath = basepath
        sdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tdate))
        #print sdate
        ymd_date = sdate.split('-')
        year = ymd_date[0]
        mo = ymd_date[1]
        day = ymd_date[2][0]
        day += ymd_date[2][1]
        #print ymd_date, year, mo, day
        retpath += '/' + year
        if not (os.path.exists(retpath)):
           os.mkdir(retpath)
        retpath += '/' + mo
        if not (os.path.exists(retpath)):
           os.mkdir(retpath)
        retpath += '/' + day + '/'
        if not (os.path.exists(retpath)):
           os.mkdir(retpath)
        return retpath

    def copy_files(self, fileList, outpath, tdate):
        success = True
        for cdate, path in sorted(fileList):
              if (cdate <= tdate):
                 print('%d, %d, %s\t%s'%(tdate, cdate, time.ctime(cdate), os.path.basename(path)))
                 # adding exception handling
                 try:
                    shutil.copy(path, outpath)
                 except IOError as e:
                    print("Unable to copy file. %s" % e)
                    success = False
                 except:
                    print("Unexpected error:", sys.exc_info())    
                    success = False
        return success
    
    def appMain(self):
        args = get_args()
        tdate = self.get_target_date(args)
        inpath = self.get_inpath(args)
        outpath = self.get_outpath(args)
        #print ('Inpath = %s\nOutpath = %s\nDate = %s'%(inpath, outpath, date))

        if (os.path.exists(outpath)):
           fileList = self.get_file_list(inpath)
       
           fullpath = self.set_fullPath(outpath, tdate)

           self.copy_files(fileList, fullpath, tdate) 

#
# Main program for running stand-alone
#
if __name__ == '__main__':
   app=DirArch()
	
