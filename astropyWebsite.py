## Alix Feinsod
## Python form using template
## Updated February 24th, 2015
## uses astropyTemplate to take in data

from bottle import route, run, template, post, request
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from array import array

##TODO import mcmc from igm.fN
from xastropy.stats import mcmc 
from xastropy.igm.fN import data as fNdata
from xastropy.xutils import xdebug as xdb

from bottle import static_file


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='')
    
@route('/astropy')    
def form():
    return template('astropyTemplate')
 
# Runs on click of "Submit data"
@route('/astropy', method='POST')
def do_response():
	
	dataSources = request.forms.getall('dataSource') # Grabs everything selected in a selection list
	if len(dataSources) == 0:
		return "You must select at least one data source."

	## TODO: check if any user data sources. create boolean isUserSource = true if there is a user source, else false
	
	else:
		models = request.forms.getall('modelType') # List
		modelType = models[0] # string
		analyses = request.forms.getall('AnalysisOptions')
		analysis = analyses[0] # string
		outputs = request.forms.getall('OutputOptions') # List
		output = outputs[0] # string
		

		##TODO: 
		##	- fN_data = set_fn_data(dataSources, extra_fNc=user input if isUserSource is true)
		##		note: above includes making fn_data_from_fits-type function for ASCII
		##	- fN_model = set_fn_model() Does this have any input? Does it need to be edited to take 
		##		into account user model selection?
		##	- rest is exact from run part of mcmc.py:
		## 		- parm = set_pymc_var(fN_model)
   		## 		- fN_model.param = np.array([iparm.value for iparm in parm])
		## 		- run(fN_data, fN_model, parm)
		##		- What about the output? how do we get the output of run and use it in the email?



		#import pdb
		#pdb.set_trace()
		fNdata.tst_fn_data(outfil='tmp.png', data_list=dataSources)
		#fNdata.tst_fn_data(outfil='tmp.png', data_list=models)
		
		useremail   = request.forms.get('useremail')

		time = mcmc.test()
		msg = MIMEMultipart()
		msg['Subject'] = "Email data"
		msg['From'] = 'xastropy@gmail.com'
		msg['To'] = useremail
		msg.attach( MIMEText(str(time)))
	
		files = []
		files.append('tmp.png')
	
    		for f in files:
        		part = MIMEBase('application', "octet-stream")
        		part.set_payload( open(f,"rb").read() )
        		encoders.encode_base64(part)
        		part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
        		msg.attach(part)
   	
   		smtp = smtplib.SMTP()
   		smtp.connect('smtp.gmail.com', 587)
   		smtp.starttls()
   		smtp.login('xastropy@gmail.com','ucsc2015')
    		smtp.sendmail('xastropy@gmail.com', useremail, msg.as_string())
    		smtp.quit()
    	
		return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)

run(host='0.0.0.0', port=8080)
