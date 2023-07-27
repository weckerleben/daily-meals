# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC1e97b7a0c7c568891f41d88b6ac998c5'
auth_token = '015e63603991b0257dc3a4249ac9a3f2'
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml='<Response><Say>Hola Ilza, William me creó para que pueda hacer llamadas y hablarle, esta es una prueba. '
          'Dice William que mañana de tardecita pasará Emilio a buscar a Jack. Adiós.</Say></Response>',
    to='+595982844853',
    from_='+13203026795'
)

call2 = client.calls.create(
    twiml='<Response><Say>Hola Christian, ¿qué tal? William me creó para que pueda hacer llamadas y hablar. Esta es solo una prueba, jeje. Adiós. También le llamé a Ilza. </Say></Response>',
    to='+595982844853',
    from_='+13203026795'
)

print(call.sid)
print(call2.sid)
