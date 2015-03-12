## Alix Feinsod
## Python form using template
## Updated March 5th, 2015
## uses astropyTemplate to take in data

from bottle import route, run, template, post, request
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from array import array


from xastropy.igm.fN import mcmc 
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
	
	else:
		builtInSources = ['OPB07', 'OPW12', 'OPW13', 'K05', 'K13R13', 'N12']
		extraSources = []
		sources = []
		for src in dataSources:
			if src not in builtInSources:
				src = os.path.abspath(src)
				extraSources.append(src)
				sources.append(src)
			else:
				sources.append(src)
				
		models = request.forms.getall('modelType') # List
		modelType = models[0] # string
		analyses = request.forms.getall('AnalysisOptions')
		analysis = analyses[0] # string
		outputs = request.forms.getall('OutputOptions') # List
		output = outputs[0] # string
		useremail   = request.forms.get('useremail')

		fN_data = mcmc.set_fn_data(sources, extraSources)
		if modelType == 'Original Model'
			fN_model = mcmc.set_fn_model() 
		else:
			fN_model = mcmc.set_fn_model(1)
		parm = mcmc.set_pymc_var(fN_model)
		fN_model.param = mcmc.np.array([iparm.value for iparm in parm])
		mcmc.run(fN_data, fN_model, parm, useremail)
		
		import pdb
		pdb.set_trace()
		#fNdata.tst_fn_data(outfil='tmp.png', data_list=dataSources)
		#fNdata.tst_fn_data(outfil='tmp.png', data_list=models)

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
