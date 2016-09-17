from twilio.rest import TwilioRestClient

account_sid = "AC069bbc61f7db2e120ba0fff6fc342e6e"
auth_token = "44dae430182496def82f6992a64de198"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+19496488407", from_="+13104395349",
                                     body="dang")
