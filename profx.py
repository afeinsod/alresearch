## Alix Feinsod
## Process of igmfn, for execution on profx comp
## Created April 22nd, 2015
## runs MCMC and emails results

from bottle import route, run, template, post, request
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from array import array
from email.mime.application import MIMEApplication

from xastropy.igm.fN import mcmc 
from xastropy.igm.fN import data as fNdata
from xastropy.xutils import xdebug as xdb

from bottle import static_file
import shutil

def runmcmcemail(modelType, useremail, sources, extraSources):
		
		if modelType is 'Akio Model':
			mcmc.mcmc_main(useremail, sources, extraSources, 1)
		else:
			mcmc.mcmc_main(useremail, sources, extraSources)
	
		files = os.listdir('C:/Xastropy Output Files/' + useremail)

		path = '/Users/afeinsod/Dropbox/Output/'
		if os.path.isdir(path + useremail):  
            		path = path +  useremail
        	else:
            		os.mkdir(path + useremail) 
            		path = path +  useremail
            		
		for f in files:
			oldpath = os.path.abspath(f)
        		shutil.copy2(oldpath, path)

		dropboxLink = 'https://www.dropbox.com/sh/lokufndo4gc7mbz/AACFRsF5qewnni8f4AYoUg8ka?dl=0'

		msg = MIMEMultipart()
		msg['Subject'] = "IGMFN"
		msg['From'] = 'xastropy@aol.com'
		msg['To'] = useremail
		msg.attach( MIMEText(str('Hello, \nYou can access your results from igmfn.ucolick.org here: ' + dropboxLink + ' in the folder ladeled with your email. \nBest, \n UCO/Lick')))

   		smtp = smtplib.SMTP()
   		smtp.connect('smtp.aol.com', 587)
   		smtp.ehlo()
   		smtp.starttls()
   		smtp.ehlo()
   		smtp.login('xastropy@aol.com','ucsc2015')
    		smtp.sendmail('xastropy@aol.com', useremail, msg.as_string())
    		smtp.quit()

if __name__ == '__main__':

	import argparse

    	# PARSE 
    	parser = argparse.ArgumentParser(description='profx code for igmfn')
    	parser.add_argument("infile", type=string, help="Name of input ascii file")
    	args = parser.parse_args()
	infile=args.infile
	
	#now read in file to get modelType, useremail, sources, extraSources
        #and use this to properly call runmcmcemail
        
        #format: firstline = modelType, second = useremail, third = sources split by spaces,
        #fourth = extrasources split by spaces
        
        f=infile.read()
	lines = f.split("\n")
				
	modelType=lines[0].split(" ")
	useremail=lines[1]
	sources=lines[2].split(" ")
	extraSources=lines[3].split(" ")
	runmcmcemail(modelType, useremail, sources, extraSources)
