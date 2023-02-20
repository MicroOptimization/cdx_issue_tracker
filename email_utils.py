from flask_mail import Mail, Message
from flask import Flask
import os
#from application import application as app

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'SpaghettiHorseRadish@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ["mail_password"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello', sender = 'SpaghettiHorseRadish@gmail.com', recipients = ['81h6a3@gmail.com'])
   msg.body = "This is the email body again"
   mail.send(msg)
   return "Sent"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, threaded=True)