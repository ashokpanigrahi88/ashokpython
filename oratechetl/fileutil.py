import os
import shutil
import time, stat
from os import (environ, path)
from pathlib import Path
from datetime import datetime , date, timedelta
import glob
import logging

class FileUtility():
    filename = ""
    directory = ""
    created = ""
    lastchangetime = ""
    filefullname = ""
    age = 0
    direxists = False
    fileexists = False
    operationmode = 'r'
    mustexist = False
    unit_min = 60
    unit_hour = unit_min*60
    unit_day = unit_hour*24
    fileobject = None
    extension = ".csv"
    """
    'r'	This is the default mode. It Opens file for reading.
    'w'	This Mode Opens file for writing.If file does not exist, it creates a new file.
                    If file exists it truncates the file.
    'x'	Creates a new file. If file already exists, the operation fails.
    'a'	Open file in append mode.If file does not exist, it creates a new file.
    't'	This is the default mode. It opens in text mode.
    'b'	This opens in binary mode.
    '+'	This will open a file for reading and writing (updating)
    """
    def __init__(self, p_filename:str,
                 p_directory:str = None,
                 p_operation:str = 'r',
                 p_mustexist:bool = False):
        self.filename = r"{}".format(p_filename)
        if p_directory is not None:
            self.directory = r"{}".format(p_directory)
        else:
            self.directory = p_directory
        self.operationmode = p_operation
        self.mustexist = p_mustexist
        self.extractdirname(self.filename)
        self.filefullname = self.get_filefullname()
        self.set_extension()

    def extractdirname(self, p_filename = filename):
        if self.directory is None:
            self.directory, self.filename = path.split(p_filename)

    def get_filefullname(self):
        self.filefullname = path.join(self.directory,self.filename)
        return self.filefullname

    def convertodir(self,p_str):
        return r"{}".format(p_str)

    def isdir(self,p_directory = directory):
        return path.isdir(p_directory)

    def isfile(self,p_filename = filename):
        return path.isfile(p_filename)

    def isdirexist(self,p_directory = directory):
        return path.exists(p_directory)

    def isfileexist(self,p_filename = filename):
        return path.exists(p_filename)

    def readable(self):
        return os.access(self.filefullname,os.R_OK)

    def writable(self):
        return os.access(self.filefullname,os.W_OK)

    def exists(self):
        return os.access(self.filefullname,os.F_OK)

    def executable(self):
        return os.access(self.filefullname,os.X_OK)

    def timestamp(self, p_file = None):
        file = self.filefullname
        if p_file is not None:
            file = p_file
        try:
            return os.stat(file)[stat.ST_MTIME]
        except:
            return 0

    def age(self, p_unit:int = 1,  p_file = None):
        seconds = time.time() - self.timestamp(p_file=p_file)
        result = round(seconds/p_unit, 3)
        return result

    def age_inminute(self , p_file = None):
        return self.age(self.unit_min, p_file=p_file)

    def age_inhour(self,  p_file = None):
        return self.age(self.unit_hour, p_file=p_file)

    def age_inday(self,  p_file = None):
        return self.age(self.unit_day, p_file=p_file)

    def lastchanged(self):
        return datetime.fromtimestamp(self.timestamp())

    def openfile(self,p_mode:str = 'r'):
        try:
            filefullname = r"{}".format(self.get_filefullname())
            print(filefullname)
            print('fileobject',self.fileobject)
            if not self.fileobject:
                self.fileobject =  open(filefullname,p_mode)
                print('fileobject',self.fileobject)
            return self.fileobject
        except Exception as ex:
            logging.error("{} - {} - {}".format(self.filefullname,p_mode,ex))
            return None

    def closefile(self):
        if self.fileobject:
            self.fileobject.close()
        self.fileobject = None

    def readfile(self):
        self.fileobject = self.openfile('r+')
        content = self.fileobject.read()
        return content

    def write(self,p_data):
        self.fileobject = self.openfile('w+')
        self.fileobject.write(p_data)

    def append(self,p_data):
        self.fileobject = self.openfile('a+')
        self.fileobject.write(p_data)

    def createfile(self,p_mode ='W'):
        self.fileobject = self.openfile(p_mode=p_mode)
        return self.fileobject

    def get_working_dir(self):
        return os.getcwd()

    def changedirectory(self,p_directory):
        os.chdir(p_directory)

    def get_files(self,p_directory = None,p_filepattern='*.csv',p_age_min:int = 0):
        directory = self.directory
        if p_directory is not None:
            directory = p_directory
        filepattern = r"{}\{}".format(directory,p_filepattern)
        files = glob.glob(filepattern)
        if p_age_min == 0:
            return files
        result = []
        for file in files:
            age_min = self.age_inminute(p_file=file)
            print(file,age_min)
            if age_min > p_age_min:
                result.append(file)
        return result

    def appenddir(self,p_directory:str):
        return os.path.join(self.directory,p_directory)

    def movefile(self,p_todir:str):
        targetdir = self.appenddir(p_todir)
        if not self.isdirexist(targetdir):
            os.makedirs(targetdir)
        targetfile = os.path.join(targetdir,self.filename)
        print(self.filefullname,targetfile)
        shutil.move(self.filefullname,targetfile)

    def get_extension(self,p_filename = filefullname):
        name, extension = path.splitext(p_filename)
        return extension

    def set_extension(self):
        self.extension = self.get_extension(self.filefullname)


    def copyfile(self,p_todir:str):
        targetdir = self.appenddir(p_todir)
        if not self.isdirexist(targetdir):
            os.makedirs(targetdir)
        targetfile = os.path.join(targetdir,self.filename)
        shutil.move(self.filefullname,targetfile)

    def deletefile(self,p_file = None):
        file = self.filefullname
        if p_file is not None:
            file = p_file
        os.remove(file)

    def get_datetimestring(self):
        datetimestring = datetime.now().strftime("%Y%m%d-%H%M%S")
        return datetimestring

    def add_datetimetofile(self, p_file = None):
        file = self.filefullname
        if p_file is not None:
            file = p_file
        filename , extension = os.path.splitext(file)
        filename = "{}-{}{}".format(filename,self.get_datetimestring(),extension)
        return filename

    def archivefile(self, p_todir:str = r"archive\\", p_addtime:bool = True):
        targetdir = self.appenddir(p_todir)
        if not self.isdirexist(targetdir):
            os.makedirs(targetdir)
        targetfile = os.path.join(targetdir,self.filename)
        if p_addtime:
            targetfile = self.add_datetimetofile(targetfile)
        print(self.filefullname,targetfile)
        shutil.move(self.filefullname,targetfile)

    def movefilestoarchive(self, p_fromdir:str = None,
                           p_filepattern:str = '*.csv',
                           p_addtime:bool = True,
                           p_age_min:int = 30):
        directory = self.directory
        if p_fromdir is not None:
            directory = p_fromdir
        files = self.get_files(p_directory=directory,
                               p_filepattern=p_filepattern,
                               p_age_min =p_age_min)
        return files