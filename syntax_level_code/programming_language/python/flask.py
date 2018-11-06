#flask is a webserver tool

#importing from flask import Flask

#create a app 
app =Flask(__name__)

#Home page / http:/127.0.0.1/
#Routing it telling the websever what output it needs to give.
@app.route("/")
#above lines tells home page. we can define the function.
def index():
	return "Hi there"

#pass a string.default is string.<username> it takes the string http://127.0.0.1:5000/profile/kendavar
@app.route("/profile/<username>")

def profile(username):
	return "Hi %s" % username

#for integers <int:variable_name>

#render template allows use to send html page
#varibales are passed as {{ variable name }}

#static folder is a default folder for css files
#templates file is the default folder for html files
