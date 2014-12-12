## Alix Feinsod
## Python form using template
## Updated December 11, 2014
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


@route('/formTest')
def formTest():
    return template('tryTemplate')
    
@route('/formTest', method='POST')
def do_response():
	dataSources = []
	options = []
	options = request.forms.getElement("dataSource[]").options
	for x in options.options:
		if x.selected:
			dataSources.append(x.value)
		else:
			dataSources.append('no')
	
	options = request.forms.get("modelType[]")
	for x in options:
		if x.selected:
			modelType = x.value
	
	options = request.forms.get("AnalysisOptions[]")
	for x in options:
		if x.selected: 
			analysis = x.value
	
	options = request.forms.get("OutputOptions[]")
	for x in options:
		if x.selected:
			output = x.value
	

	useremail   = request.forms.get('useremail')

	time = mcmc.test()
	msg     = output
   	
   	smtp = smtplib.SMTP()
   	smtp.connect('smtp.gmail.com', 587)
   	smtp.starttls()
   	smtp.ehlo()
	smtp.login('alfeinsod@gmail.com','mamabear112294')
    	smtp.sendmail('alfeinsod@gmail.com', useremail, msg)
    	smtp.quit()
    	
	return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)

run(host='0.0.0.0', port=8080)
