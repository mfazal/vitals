#! usr/bin/python

from flask import Flask
from flask import json, jsonify, request
import smtplib, subprocess
app = Flask(__name__)


def send_email():
    gmail_user = "pcsvitals@gmail.com"
    gmail_pwd = "slativscp"
    FROM = 'pcsvitals@gmail.com'
    TO = ['gpr.1993@gmail.com']
    SUBJECT = "Health vital information"
    TEXT = "Lorem ipsum"

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent'
    except:
        print 'Failed to send!'



def ruleEngine(vitals_data):
    #checking HR threshold
    print "inside rule engine"
    #print vitals_data['HR'] 
    
    if int(vitals_data['HR']>70) and int(vitals_data['HR'])<140: 
        print "You're fine"
    else:
        print "Sending notification via Email and Text"
        send_email()
        #bashCommand = "curl -X POST http://textbelt.com/intl -d number=971507646637 -d 'message=Api-called-Testing' "
        #subprocess.Popen(bashCommand)
    

@app.route("/")
def hello():
    return "Hello World"


@app.route("/index")
def index():
    return "My name is guru"

@app.route("/api/<device_id>/vitals", methods= ['POST'])
def postVitals(device_id):
    #print request.method, request.headers
    print "Device id =  ", device_id
    if request.headers['Content-Type'] == 'application/json':
        #print "posted some data"
        json_dict=request.get_json() 
        print json_dict.keys(), json_dict.values()
        #print json_dict['message']
        #return "Received JSON Message: " + jsonify(**request.json)
        ruleEngine(json_dict) 
        return "Received JSON Message"

@app.route("/api/<device_id>/SOS", methods= ['POST'])
def SOS_Trigger(device_id):
    if request.headers['Content-Type'] == 'text/plain':
        send_email()
        data_recd = request.data
        print data_recd
        return data_recd

@app.route("/api/dashboard")
def dashboard():
    return "I am in dashboard! More work needs to be done!!!"


if __name__ == '__main__':
    app.debug= True
    app.run()
