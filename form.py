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


@route('/formTest')
def formTest():
    return template('tryTemplate')
    
@route('/formTest', method='POST')
def do_response():
	
	dataSources = request.forms.getall('dataSource')
	models = request.forms.getall('modelType')
	modelType = models[0]
	analyses = request.forms.getall('AnalysisOptions')
	analysis = analyses[0]
	outputs = request.forms.getall('OutputOptions')
	output = outputs[0]
	
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

run(host='0.0.0.0', port=8080)
