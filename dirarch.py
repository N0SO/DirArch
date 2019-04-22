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

"""

import argparse
import os, sys, time, shutil
from stat import S_ISREG, ST_CTIME, ST_MODE
#import datetime
#from dateutil.parser import parse

VERSION = '0.0.5'

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
        parser.add_argument("-l", "--logfile", default=None,
            help="Specifies a log output file name. If not specified messages go to console.")
        parser.add_argument("-r", "--removefiles", default='False',
            help="Remove files successfully copied from the source directory. Default is do not remove files.") 
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
    
    def get_remove(self, args):
        removeFlag = False
        removestg = args.args.removefiles
        if ('TRUE' in removestg.upper()):
           removeFlag=True
        return removeFlag

    def get_target_date(self, args):
        temp_date = ""
        temp_date = args.args.date
        if ('TODAY' in temp_date):
           target_date = time.mktime(time.localtime())
        else:
           target_date = time.mktime(time.strptime(temp_date, '%Y-%m-%d-%H:%M'))
        return int(target_date)
        
    def get_logpath(self, args):
        """
           Redirect STDOUT, STDERR to args.logfile
           if that option is provided
        """
        retpath = args.args.logfile
        if (retpath):
           retpath += time.strftime("-%Y%m%d-%H%M%S.txt")
           retsock = open(retpath, 'w')
           self.old_stdout = sys.stdout
           self.old_stderr = sys.stderr
           sys.stdout = sys.stderr = retsock
        return retpath
        
    def savelogfile(self,logpath, outpath):
       success = False
       if (logpath):
	      success = True
	      #Switch back to original STDIN, STDERR
	      logsock = sys.stdout
	      sys.stdout = self.old_stdout
	      sys.stderr = self.old_stderr
	      try:
	         logsock.close()
	         shutil.copy(logpath, outpath)
	      except IOError as e:
	         print("Unable to copy file. %s" % e)
	         success = False
	      except:
	         print("Unexpected error:", sys.exc_info())    
	         success = False
       return success

    def get_file_list(self, inpath, tdate):
        #all entries in the directory w/ stats
        retdata = []
        data = (os.path.join(inpath, fn) for fn in os.listdir(inpath))
        data = ((os.stat(path), path) for path in data)
        for stat, path in data:
           if S_ISREG(stat[ST_MODE]):
              cdate = stat[ST_CTIME]
              if cdate <= tdate:
                 retdata.append([cdate, path])
        return retdata

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

    def copy_files(self, fileList, outpath, tdate, deleteFiles = False):
        success = True
        filecount = 0
        for cdate, path in sorted(fileList):
              if (cdate <= tdate):
                 #Set path for this file
                 thisfileoutpath = self.set_fullPath(outpath, cdate)
                 #Log file copy and copy it
                 print('Copy %s (%s) to %s'%(path, time.ctime(cdate), thisfileoutpath))
                 # adding exception handling
                 try:
                    shutil.copy(path, thisfileoutpath)
                 except IOError as e:
                    print("Unable to copy file. %s" % e)
                    success = False
                 except:
                    print("Unexpected error:", sys.exc_info())    
                    success = False
                 if (success):
                    filecount += 1
                    #delete file if copied successfully
                    if (deleteFiles):
                       os.remove(path)
        return success, filecount
    
    def appMain(self):
        result = False
        args = get_args()
        tdate = self.get_target_date(args)
        inpath = self.get_inpath(args)
        removeFlag = self.get_remove(args)
        outpath = self.get_outpath(args)
        logpath = self.get_logpath(args)
        #print ('Inpath = %s\nOutpath = %s\nDate = %s'%(inpath, outpath, date))

        if (os.path.exists(outpath)):
           fileList = self.get_file_list(inpath, tdate)
           
           if (len(fileList) > 0):
              #fullpath = self.set_fullPath(outpath, tdate)
              result, filecount = self.copy_files(fileList, outpath, tdate, removeFlag) 
              
           print ('Result of file success = %s, copied %d files.'%(result, filecount))
           
           if(self.savelogfile(logpath, outpath)):
              os.remove(logpath)

#
# Main program for running stand-alone
#
if __name__ == '__main__':
   app=DirArch()
	
