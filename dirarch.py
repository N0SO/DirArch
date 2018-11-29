#!/usr/bin/python
"""
dirarch - Archive a collection of files with the specified creation date in the specified location.
"""

import argparse
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time

VERSION = '0.0.1'

class get_args():
    def __init__(self):
        if __name__ == '__main__':
            self.args = self.getargs()
            
    def getargs(self):
        usageSTG = ('dirarch.py --date <date> '
                    '--indirectory <source directory> '
                    '--outdirectory <destination directory>')
        aboutSTG = ('Utility to move all files with creation date specified by --date '
                    'in the source directory specified by --indirectory to '
                    'the destination specified by --outdirectory.')

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
        target_date = ""
        target_date = args.args.date
        return target_date
        
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
        date = self.get_target_date(args)
        inpath = self.get_inpath(args)
        outpath = self.get_outpath(args)
        #print ('Inpath = %s\nOutpath = %s\nDate = %s'%(inpath, outpath, date))
   
        fileList = self.get_file_list(inpath)
   
        for cdate, path in sorted(fileList):
              print('%s\t%s'%(time.ctime(cdate), os.path.basename(path)))
       


#
# Main program for running stand-alone
#
if __name__ == '__main__':
   app=DirArch()
	