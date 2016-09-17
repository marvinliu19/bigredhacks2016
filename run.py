from flask import Flask, request, redirect
import twilio.twiml
import geocode

app = Flask(__name__)

callers = {
    "+19496488407": "Dalvor"
}

@app.route("/", methods=['GET', 'POST'])
def respond():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)

    if text_body == "seven day forecast":
        #message = forecast.getSevenDayForecast()
        message = "Seven day forecast requested."
    else:
        #args = text_body.split()
        #message = "Oops! That's not a recognized command. Please try again."
        areaCode = '310'
        if from_number != None:
            areaCode = from_number[2:5]
        coord = geocode.getCoordinates(areaCode)
        print coord[0]
        print coord[1]
        message = "You are from: (%f, %f)" % (coord[0], coord[1])

    # if body != None:
    #     if from_number in callers:
    #         message = "Hi " + callers[from_number] + "! You are now subscribed to" + body + "."
    #     else:
    #         message = "Hi! You are now subscribed to" + body + "."
    # else:
    #     message = "Oops! Something went wrong :("

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
