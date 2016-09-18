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

DATABASE = 'forecast'

# =============================BACKGROUND=======================================
account_sid = "AC069bbc61f7db2e120ba0fff6fc342e6e"
auth_token = "44dae430182496def82f6992a64de198"
client = TwilioRestClient(account_sid, auth_token)

def send_weather_update():
    conn = sqlite3.connect(DATABASE)
    selectQuery = "SELECT phoneNumber FROM subscription WHERE crop = 'forecast'"
    cursor = conn.execute(selectQuery)
    for row in cursor:
        phoneNumber = str(row[0])
        coord = geocode.getCoordinates(phoneNumber[2:5])
        text = functions.sevenDayForecast(coord[0], coord[1])
        print "sending weather update to %s at coord %f %f" % (phoneNumber, coord[0], coord[1])
        message = client.messages.create(to=phoneNumber, from_="+13104395349", body=text)

def send_corn_update():
    conn = sqlite3.connect(DATABASE)
    selectQuery = "SELECT phoneNumber FROM subscription WHERE crop = 'corn'"
    cursor = conn.execute(selectQuery)
    for row in cursor:
        phoneNumber = str(row[0])
        text = functions.price('corn')
        print "sending corn update to %s" % phoneNumber
        message = client.messages.create(to=phoneNumber, from_="+13104395349", body=text)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=send_weather_update,
    trigger=IntervalTrigger(seconds=600),
    id='send_weather_update',
    name='send_weather_update every minute',
    replace_existing=True)

scheduler.add_job(
    func=send_corn_update,
    trigger=IntervalTrigger(seconds=300),
    id='send_corn_update',
    name='send_corn_update every minute',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# ==============================================================================

app = Flask(__name__)

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
        if args[0] == "subscribe" and len(args) == 2:
            subscribe_to = args[1]
            if valid_subscription(subscribe_to):
                conn = sqlite3.connect(DATABASE)
                insertQuery = "INSERT INTO subscription VALUES(\'%s\', \'%s\')" % (from_number, subscribe_to)
                conn.execute(insertQuery)
                conn.commit()
                conn.close()
                if subscribe_to == "forecast":
                    message = "You have subscribed to weather forecast updates!"
                else:
                    message = "You have subscribed to updates for %s!" % subscribe_to
            else:
                message = "Sorry! We don't have subsciption updates for %s :(" % (subscribe_to)
        elif args[0] == "unsubscribe" and len(args) == 2:
            unsubscribe_from = args[1]
            if valid_subscription(unsubscribe_from):
                conn = sqlite3.connect(DATABASE)
                query = "DELETE FROM subscription WHERE phoneNumber = \'%s\' and crop = \'%s\'" % (from_number, unsubscribe_from)
                conn.execute(query)
                conn.commit()
                conn.close()
                if unsubscribe_from == "forecast":
                    message = "You have unsubscribed from weather forecast updates!"
                else:
                    message = "You have unsubscribed from updates for %s!" % unsubscribe_from
            else:
                message = "Sorry! We don't have subsciption updates for %s :(" % (subscribe_to)
        elif args[0] == "price" and args[1] == "corn" and len(args) == 2:
            crop = args[1]
            message = functions.price(crop)
        elif args[0] == "local" and args[1] == "corn" and len(args) == 2:
            crop = args[1]
            message = "%d acres of %s are being planted near you" % (12, crop)
        else:
            message = "Sorry, we don't recognize your text"

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

def valid_subscription(subscribe_to):
    return subscribe_to == "forecast" or subscribe_to == "corn"

if __name__ == "__main__":
    app.run(debug=True)
