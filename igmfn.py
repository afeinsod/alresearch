## Alix Feinsod
## Python form using template
## Updated April 22nd, 2015
## uses astropyTemplate to take in data

from bottle import route, run, template, post, request
import smtplib, os

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
    ##Sends this info to profx machine by mkdir, generating an SCP request for any user uploads, executes a 
    ##python call on profx to run in the background on (some amount) of processors. 

		return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)

run(host='0.0.0.0', port=8080)
