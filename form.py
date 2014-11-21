## Alix Feinsod
## Python form using template
## Updated November 20, 2014
## uses tryTemplate to take in data!!!

from bottle import route, run, template, post, request

@route('/formTest')
def formTest():
    return template('tryTemplate')
    
@route('/formTest', method='POST')
def do_response():
	userEmail = request.forms.get('useremail')
	return "Processing your request. Results will be sent to '{0}' in a few hours or days.".format(userEmail)

run(host='0.0.0.0', port=8080)
