#! usr/bin/python

from app import app, db, models
#from flask import Flask
from flask import jsonify, request, render_template
import smtplib, subprocess, json
from models import SWJsonify, User, Post, Device, Vital, SOS, Notification, NotificationContact
#app = Flask(__name__)
import json

def send_email(text):
    gmail_user = "pcsvitals@gmail.com"
    gmail_pwd = "slativscp"
    FROM = 'pcsvitals@gmail.com'
    TO = ['sharvil2009@gmail.com']
    SUBJECT = "Health vital information"
    TEXT = text

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



def ruleEngine(vitals_data, device_id):
    #checking HR threshold
    print "inside rule engine"
    #print vitals_data['HR'] 
    
    if int(vitals_data['HR'])>70 and int(vitals_data['HR'])<140: 
        print "You're fine"
    else:
        print "Sending notification via Email and Text"
        text = "Unusual Health vitals!"
        send_email(text)

        #Notification object
        notif_obj = Notification(device_id, text, 'email')
        db.session.add(notif_obj)
        db.session.commit()
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
        [HR, bloodoxy, temp_body, temp_env, baro] = map(lambda x: float(x), json_dict.values())

        ruleEngine(json_dict, device_id) 

        #Make into Vital Object
        vit_obj = Vital(device_id, temp_body, temp_env, HR, bloodoxy, baro)
        db.session.add(vit_obj)
        db.session.commit()


        #print json_dict['message']
        #return "Received JSON Message: " + jsonify(**request.json)
       
        return "JSON Message" + json.dumps(json_dict)

@app.route("/api/<device_id>/SOS", methods= ['POST'])
def SOS_Trigger(device_id):
    if request.headers['Content-Type'] == 'text/plain':
        text = "SOS Trigger activated!"
        send_email(text)

        #making object to store in SOS table
        sos_obj = SOS(device_id, text)
        db.session.add(sos_obj)
        db.session.commit()

        notif_obj = Notification(device_id, text, 'email')
        db.session.add(notif_obj)
        db.session.commit()


        data_recd = request.data
        print data_recd
        return data_recd

@app.route("/api/dashboard", methods= ['GET'])
def dashboard():
    vitals = Vital.query.all()
    no_of_users=5
    heart_data = [['Timestamp']]
    for i in range(1, no_of_users+1):
        heart_data[0].append('User '+str(i))

    time_info = {}
    for vital in vitals:
        time = "%s:%s" % (vital.timestamp.minute, vital.timestamp.second)
        if time in time_info:
            time_info[time][vital.user_id-1]=vital.heartrate
        else:
            time_info[time] = [80 for _ in range(no_of_users)]
            time_info[time][vital.user_id-1]=vital.heartrate
    
    for key, val in time_info.items():
        temp = [key]
        for obj in val:
            temp.append(obj)
        heart_data.append(temp)
    
    return render_template("dashboard.html", json_data=json.dumps(heart_data))

@app.route("/Trial", methods= ['GET', 'POST'])
def Trial():
    
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            json_dict = request.get_json()

    
            return render_template("index.html", messages=json.dumps(json_dict))
    else:
        # v = Vital.query.get(1)
        # dict_vital = v.__dict__
        # print dict_vital
        # del dict_vital['_sa_instance_state']
        # dict_vital['timestamp'] = str(dict_vital['timestamp'])



        # return json.dumps(dict_vital)
        vitals = Vital.query.all()
        return SWJsonify({'vitals':vitals })

if __name__ == '__main__':
    app.debug= True
    app.run()
