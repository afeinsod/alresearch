## Alix Feinsod
## Python form using template
## Updated January 13th, 2015
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
from xastropy.xutils import xdebug as xdb


@route('/formTest')
def formTest():
    return template('tryTemplate')
 
# Runs on click of "Submit data"
@route('/formTest', method='POST')
def do_response():
	
	dataSources = request.forms.getall('dataSource') # Grabs everything selected in a selection list
	if len(dataSources) == 0:
		return "You must select at least one data source."
	else:
		models = request.forms.getall('modelType') # List
		modelType = models[0] # string
		analyses = request.forms.getall('AnalysisOptions')
		analysis = analyses[0] # string
		outputs = request.forms.getall('OutputOptions') # List
		output = outputs[0] # string
		
		#import pdb
		#pdb.set_trace()
		#fNdata.tst_fn_data(outfil='tmp.png', data_list=dataSources)
		#fNdata.tst_fn_data(outfil='tmp.png', data_list=models)
		
		useremail   = request.forms.get('useremail')

		time = mcmc.test()
		msg = MIMEMultipart()
		msg['Subject'] = "Email data"
		msg['From'] = 'alfeinsod@gmail.com'
		msg['To'] = useremail
		msg.attach( MIMEText(str(time)))
	
		files = []
		#files.append('tmp.png')
	
    		for f in files:
        		part = MIMEBase('application', "octet-stream")
        		part.set_payload( open(f,"rb").read() )
        		encoders.encode_base64(part)
        		part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
        		msg.attach(part)
   	
   		smtp = smtplib.SMTP()
   		smtp.connect('smtp.gmail.com', 587)
   		smtp.starttls()
   		smtp.ehlo()
	
    		smtp.sendmail('alfeinsod@gmail.com', useremail, msg.as_string())
    		smtp.quit()
    	
		return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)

run(host='0.0.0.0', port=8080)
