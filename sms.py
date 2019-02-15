from auth import account_sid, auth_token, src_phone_number, dest_phone_number
from twilio.rest import Client


def sendMessage(forecast):
    client = Client(account_sid, auth_token)
    weather = ''

    for x in range(2):
        first, second, third = forecast[x]
        weather = weather + first + ' ' + second + '\n' + third + '\n'

    try:
        message = client.messages.create(
                body = weather,
                from_ = src_phone_number,
                to = dest_phone_number
            )

    except:
        raise SystemExit