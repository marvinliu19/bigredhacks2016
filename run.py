from flask import Flask, request, redirect
import twilio.twiml
import geocode
import functions

app = Flask(__name__)

callers = {
    "+19496488407": "Dalvor"
}

@app.route("/", methods=['GET', 'POST'])
def respond():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    if text_body == "seven day forecast" or text_body == None:
        areaCode = '310'
        if from_number != None:
            areaCode = from_number[2:5]
        coord = geocode.getCoordinates(areaCode)
        message = functions.sevenDayForecast(coord[0], coord[1])
    else:
        areaCode = '310'
        if from_number != None:
            areaCode = from_number[2:5]
        coord = geocode.getCoordinates(areaCode)
        message = "You are from: (%f, %f)" % (coord[0], coord[1])

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
