from flask import Flask, request, redirect, g
import twilio.twiml
import geocode
import functions
import sqlite3

DATABASE = 'forecast'

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def respond():
    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    if text_body == "seven day forecast":
        areaCode = '310'
        if from_number != None:
            areaCode = from_number[2:5]
        coord = geocode.getCoordinates(areaCode)
        message = functions.sevenDayForecast(coord[0], coord[1])
    elif text_body == None:
        crop = "lol"
        from_number = "+19493953324"
        conn = sqlite3.connect(DATABASE)
        cursor = conn.execute('SELECT COUNT(*) from subscription')
        (count,) = cursor.fetchone()
        insertQuery = "INSERT INTO subscription VALUES(%i, \'%s\', \'%s\')" % (count, from_number, crop)
        conn.execute(insertQuery)
        conn.commit()
        conn.close()
        message = "You have subscribed to updates for " + insertQuery + "!"
    else:
        args = text_body.split()
        if args[0] == "subscribe:" and len(args) == 2:
            crop = args[1]
            conn = sqlite3.connect(DATABASE)
            cursor = conn.execute('SELECT COUNT(*) from subscription')
            (count,) = cursor.fetchone()
            insertQuery = "INSERT INTO subscription VALUES(%i, \'%s\', \'%s\')" % (count, from_number, crop)
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
