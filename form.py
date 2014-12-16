## Alix Feinsod
## Python form using template
## Updated December 15, 2014
## uses tryTemplate to take in data!!!

from bottle import route, run, template, post, request
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from array import array


from xastropy.stats import mcmc 
from xastropy.igm.fN import data as fNdata
#from xastropy.xutils import xdebug as xdb


@route('/formTest')
def formTest():
    return template('tryTemplate')
    
# Runs on click of "Submit data"
@route('/formTest', method='POST')
def do_response():
	
	dataSources = request.forms.getall('dataSource') # Grabs everything selected in a selection list
	models = request.forms.getall('modelType') # List
	modelType = models[0] # string
	analyses = request.forms.getall('AnalysisOptions')
	analysis = analyses[0] # string
	outputs = request.forms.getall('OutputOptions') # List
	#output = outputs[0]

	import pdb
	pdb.set_trace()
	fNdata.tst_fn_data(outfil='tmp.png', data_list=dataSources)

    #fNdata.tst_fn_data(outfil='tmp.png', data_list=models)
	
	useremail   = request.forms.get('useremail')

	time = mcmc.test()
	msg     = str(time)

   	smtp = smtplib.SMTP()
   	smtp.connect('smtp.gmail.com', 587)
   	smtp.starttls()
   	smtp.ehlo()
	smtp.login('alfeinsod@gmail.com','mamabear112294')
    	smtp.sendmail('alfeinsod@gmail.com', useremail, msg)
    	smtp.quit()
    	
	return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)
    #return template('tryTemplate2')

run(host='0.0.0.0', port=8080)
