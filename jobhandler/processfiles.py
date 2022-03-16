import os
import time
import shutil
import glob
import jobhandler.smtpclientinfo as config
import jobhandler.requestutil as requestutil
import jobhandler.mailutil as mailutil
import xml.etree.ElementTree as ET
def readxmlfile(p_xmlfile):
    tree = ET.parse(p_xmlfile)
    root = tree.getroot()
    return root
def getelementtext(p_xml,p_element):
    try:
        return p_xml.find(p_element)
    except:
        return ""
def getfiles(p_directory = 'Y:/oratechjobs/',
             p_filepattern='otch_*.xml',
             p_postaction = None,
             p_maxfiles = 1):
    
    filectr = 0
    xmltodict = {}    
    for file in glob.glob(p_directory+p_filepattern):
        try:
            print(file)
            xmlcontent = readxmlfile(file)    
            xmltodict = {}   
            for i in xmlcontent.findall('./*'):
                xmltodict[i.tag] = i.text
            if xmltodict['Jobtype'] == 'ORACLEREPORT':
                print('runreport')
                requestutil.runreport(xmltodict['Oraclereporturl'])
            if xmltodict['Jobtype'] == 'MAIL':
                attachdir , attachfile = os.path.split(xmltodict['Mailattachment'])
                attachdir = attachdir.replace(config.Mapdirectoryfrom,config.Mapdirectoryto)
                mailutil.sendmail(p_server = config.Host ,
                p_port = config.Port,
                p_sender = config.Username,
                p_password = config.Password,
                p_receiver = xmltodict['Mailto'] ,
                p_message = xmltodict['Mailbody'] ,
                p_subject = xmltodict['Mailsubject'] ,
                p_body   = xmltodict['Mailbody'] ,
                p_footer = config.Signature,
                p_attachdir = attachdir,
                p_attachfile = '/'+attachfile)

            if p_postaction == 'move':
                print('moving file {} to {}'.format(file,config.Processeddir))
                try:
                    filedir , filenm =  os.path.split(file)
                    shutil.move(file,config.Processeddir+'/'+filenm)
                except:
                    print('file already exists')
                    try:
                        os.remove(file)
                    except:
                        print('unable to delete')
            filectr = filectr+1
            print('File counter',filectr)
            if filectr%50 == 0:
                time.sleep(30)
            if filectr >= p_maxfiles:
                break
            time.sleep(3)
        except:
            print('error:',file)
    print('{} files processed'.format(filectr))

def startprocess():
    while True:
        getfiles(p_postaction='move',p_maxfiles=50)