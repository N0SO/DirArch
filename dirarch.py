#!/usr/bin/python
"""
dirarch - Archive a collection of files with the specified creation date or older,
          from the specified location.
"""

import argparse
import os, sys, time, shutil
from stat import S_ISREG, ST_CTIME, ST_MODE
#import datetime
#from dateutil.parser import parse

VERSION = '0.0.2'

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
           target_date = time.mktime(time.strptime(temp_date, '%Y-%m-%d'))
        return int(target_date)
        
    def get_file_list(self, inpath):
        #all entries in the directory w/ stats
        data = (os.path.join(inpath, fn) for fn in os.listdir(inpath))
        data = ((os.stat(path), path) for path in data)

        # regular files, insert creation date
        data = ((stat[ST_CTIME], path)
              for stat, path in data if S_ISREG(stat[ST_MODE]))
        return data
    
    def appMain(self):
        args = get_args()
        tdate = self.get_target_date(args)
        inpath = self.get_inpath(args)
        outpath = self.get_outpath(args)
        #print ('Inpath = %s\nOutpath = %s\nDate = %s'%(inpath, outpath, date))
   
        fileList = self.get_file_list(inpath)
   
        for cdate, path in sorted(fileList):
              if (tdate >= cdate):
                 print('%s\t%s'%(time.ctime(cdate), os.path.basename(path)))
                 # adding exception handling
                 try:
                    shutil.copy(path, outpath)
                 except IOError as e:
                    print("Unable to copy file. %s" % e)
                 except:
                    print("Unexpected error:", sys.exc_info())    


#
# Main program for running stand-alone
#
if __name__ == '__main__':
   app=DirArch()
	
