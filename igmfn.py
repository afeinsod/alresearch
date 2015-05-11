## Alix Feinsod
## Python form using template
## Updated April 22nd, 2015
## uses astropyTemplate to take in data

from bottle import route, run, template, post, request
import smtplib, os
import commands
from bottle import static_file
import subprocess

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='')
    
@route('/astropy')    
def form():
    return template('astropyTemplate')
 
# Runs on click of "Submit data"
@route('/astropy', method='POST')
def do_response():
	useremail   = request.forms.get('useremail')
	dataSources = request.forms.getall('dataSource') # Grabs everything selected in a selection list
	if len(dataSources) == 0:
		return "You must select at least one data source."
	
	else:
		builtInSources = ['OPB07', 'OPW12', 'OPW13', 'K05', 'K13R13', 'N12']
		extraSources = []
		sources = []
		for src in dataSources:
			if src not in builtInSources:
				#we have a user upload
				#first, make sure the format is correct
				upload = request.files.get('upload')
				flag = True
				f=upload.file.read()
				import pdb
				pdb.set_trace()
				lines = f.split("\n")
				
				firstline=lines[0].split(" ")
				 
				if len(firstline) != 2:
					flag = False
				for i in firstline:
					if type(i) is not float:
						flag = False
						
				for i in range(1, len(lines) -1):
					line = lines[i].split(" ") 
					if len(line) != 4:
						flag = False
					for a in line:
						if type(a) is not float:
							flag = False
				
				if flag is False:
					return "Wrong file format."
					
				#second, save it
				name, ext = os.path.splitext(upload.filename)
				save_path = "/tmp/{email}".format(email=useremail)
        			if not os.path.exists(save_path):
           				os.makedirs(save_path)

        			file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
				with open(file_path, 'w') as open_file:
        				open_file.write(upload.file.read())
				#third, add it to the list 
				# not sure if this is necessary: src = os.path.abspath(src)
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
		
    ##Sends this info to profx machine by mkdir, generating an SCP request for any user uploads, executes a 
    ##python call on profx to run in the background on (some amount) of processors. 
		if (len(extraSources) != 0): 
			#makes directory in afeinsod
			HOST = 'afeinsod@profx'
			COMMAND = 'mkdir ' + useremail
			ssh = subprocess.call(["ssh", "-C", "%s" % HOST, COMMAND])
			#copies all user uploads to that directory
			for src in extraSources:
				p=subprocess.call(['scp', src, 'profx:/Users/afeinsod/' + useremail])
		COMMAND = 'python profx.py ' + modelType + analysis + output + useremail 
		for src in sources:
			COMMAND = COMMAND + src
		process=subprocess.Popen(["ssh", "-C", "%s" % HOST, COMMAND])
				
		return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(useremail)

run(host='0.0.0.0', port=8080)
