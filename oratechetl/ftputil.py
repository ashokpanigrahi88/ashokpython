# Anonymous FTP login
import os
import glob
from ftplib import FTP, all_errors, FTP_TLS, FTP_PORT
from oratechetl import secrets as secret

class FTPUtil():
    keyprefix = 'ORATECH_DATAHUB_FTP'
    host = secret.getkey(keyprefix+'HOST')
    user = secret.getkey(keyprefix+'USER')
    pwd = secret.getkey(keyprefix+'PWD')
    port = int(secret.getkey(keyprefix+'PORT'))
    ftpobject = FTP()
    def __init__(self,p_host = None , p_user = None, p_pwd = None,*args, **kwargs):
        if p_host is not None:
            self.host = p_host
        if p_user is not None:
            self.user = p_user
        if p_pwd is not None:
            self.pwd = p_pwd

    def get_welcome(self):
        welcomde = self.ftpobject.getwelcome()
        print(welcomde)
        return welcomde

    def connect(self):
        self.ftpobject.connect(host=self.host,port=self.port)
        self.ftpobject.login(user=self.user,passwd=self.pwd)
        self.get_welcome()

    def close(self):
        self.ftpobject.close()

    def createdir(self, p_directory):
        self.ftpobject.mkd(p_directory)

    def get_currentdir(self):
        try:
            workingdir = self.ftpobject.pwd()
            print(workingdir)
            return workingdir
        except all_errors as e:
            print(f'Error with FTP: {e}')

    def changedir(self, p_directory):
        self.ftpobject.cwd(p_directory)

    def local_changedir(self, p_directory):
        os.chdir(p_directory)

    def local_currentdir(self):
        return os.getcwd()

    def removedir(self, p_directory):
        self.ftpobject.rmd(p_directory)

    def get_files(self):
        files = []
        self.ftpobject.dir(files.append)
        return files

    def get_localfiles(self,p_filepattern= '*.*'):
        files = glob.glob(p_filepattern)
        return files

    def upload_file(self,p_file:str="", p_filetype = 'text'):
        if len(p_file) == 0:
            return
        with open(p_file,'rb')  as file:
            if p_filetype == 'text':
                self.ftpobject.storlines('STOR {}'.format(p_file),file)
            else:
                self.ftpobject.storbinary('STOR {}'.format(p_file),file)

    def get_size(self,p_file:str="", p_filetype = 'text'):
        if len(p_file) == 0:
            return
        size = 0
        try:
            if p_filetype == 'text':
                self.ftpobject.sendcmd('TYPE A')
                size =  self.ftpobject.size(p_file)
            else:
                self.ftpobject.sendcmd('TYPE I')
                size =  self.ftpobject.size(p_file)
        except all_errors as error:
            print(f"Error checking image size: {error}")
        finally:
            return size

    def rename(self, p_file, p_newfile):
        try:
            self.ftpobject.rename(p_file, p_newfile)
        except all_errors as error:
            print(f'Error renaming file on server: {error}')

    def download(self,p_file, p_filetype = 'text'):
        with open(p_file, 'w') as local_file:
            if p_filetype == 'text':
                response = self.ftpobject.retrlines('RETR {}'.format(p_file), local_file.write)
            else:
                response = self.ftpobject.retrbinary('RETR {}'.format(p_file), local_file.write)
            if response.startswith('226'):  # Transfer complete
                print('Transfer complete')
            else:
                print('Error transferring. Local file may be incomplete or corrupt.')

    def delete(self,p_file):
        try:
            self.ftpobject.delete(p_file)
        except all_errors as error:
            print(f'Error deleting file: {error}')
