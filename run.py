from flask import Flask, request, redirect, g
import twilio.twiml
import geocode
import functions
import sqlite3
from twilio.rest import TwilioRestClient
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# ===================++BACKGROUND===============================================
account_sid = "AC069bbc61f7db2e120ba0fff6fc342e6e"
auth_token = "44dae430182496def82f6992a64de198"
client = TwilioRestClient(account_sid, auth_token)

def send_sms():
    #"+19496488407"
    message = client.messages.create(to="+19493953324", from_="+13104395349",
                                         body="dang")

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=send_sms,
    trigger=IntervalTrigger(seconds=5),
    id='send_sms',
    name='send_sms every 5 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# ==============================================================================

app = Flask(__name__)

DATABASE = 'forecast'

@app.route("/", methods=['GET', 'POST'])
def respond():
    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    if text_body == "seven day forecast":
        coord = geocode.getCoordinates(from_number[2:5])
        message = functions.sevenDayForecast(coord[0], coord[1])
    elif text_body == None:
        message = "No text body"
    else:
        args = text_body.split()
        if args[0] == "subscribe:" and len(args) == 2:
            crop = args[1]
            conn = sqlite3.connect(DATABASE)
            insertQuery = "INSERT INTO subscription VALUES(\'%s\', \'%s\')" % (from_number, crop)
            conn.execute(insertQuery)
            conn.commit()
            conn.close()
            message = "You have subscribed to updates for " + crop + "!"
        else:
            message = "Sorry, we don't recognize your text"

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
