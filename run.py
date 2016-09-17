from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

callers = {
    "+19496488407": "Dalvor"
}

@app.route("/", methods=['GET', 'POST'])
def respond():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)

    if body != None:
        if from_number in callers:
            message = "Hi " + callers[from_number] + "! You are now subscribed to" + body + "."
        else:
            message = "Hi! You are now subscribed to" + body + "."
    else:
        message = "Oops! Something went wrong :("
        
    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        m.media("https://demo.twilio.com/owl.png")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
