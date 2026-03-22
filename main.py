import requests
import os
from twilio.rest import Client

#get location
# api https://api.openweathermap.org/geo/1.0/direct?q=Krakow,PL&appid=558ea258d23edafcd8588309d3edc612
# or in latlong.net

#json viewer https://jsonviewer.stack.hu/

#sms https://console.twilio.com/dashboard?variant_override=non-dev
#whatsapp https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
#run code pythonanywhere.com
#envs
# lista  dir Env:
# ustawienie  setx OWM_API_KEY "zzzzzzzzzzzzzzzzzzzzzzzzzzzz" ale to nie działa
#              unix export OWM_API_KEY=zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

#apilist.fun

KR_LAT=50.0619474
KR_LON=19.9368564
#test FR
KR_LAT=43.608292
KR_LON=3.879600

twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

# https://api.openweathermap.org/data/2.5/weather?q=London,UK&appid=558ea258d23edafcd8588309d3edc612
#api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}

url = 'https://api.openweathermap.org/data/2.5/forecast'
parameters={"lat":KR_LAT,
            "lon":KR_LON,
            "units":"metric",
            "cnt":4, #only 4 timestamps
            "appid": os.environ.get("OWM_API_KEY")
#            "appid":api_key_p
}
print(f"Results:  {os.environ.get("OWM_API_KEY")}")
response = requests.get(url=url, params = parameters)
response.raise_for_status()
try:
    x = response.json()
    #position = (response.json()["iss_position"]["longitude"], response.json()["iss_position"]["latitude"])
    print(f"Results:  {x["list"]}")
    print(f"Current weather:  {x["list"][0]['weather'][0]['description']}")
    # print(f" Results  {x["list"][0]['weather'][0]['id']}") #id is giving weather code - see documentation
    for wf in x["list"]:
        if int(wf['weather'][0]['id'])< 700:
            print('! Bring an Umbrella, it is going to rain or snow in next 12h')
            #sms
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(
                body="\nBring an Umbrella, it is going to rain or snow in next 12h",
                from_="+17754427191",
                to="+48538159944",
            )
            #whatsapp
            # message = client.messages.create(
            #     from_='whatsapp:+14155238886',
            #     body='Bring an Umbrella, it is going to rain or snow in next 12h',
            #     to='whatsapp:+48538159944'
            # )
            #print(message.status)
            break

    #print(f" sunrise hour {x["results"]["sunrise"].split("T")[1].split(":")[0]}  sunset hour {x["results"]["sunset"].split("T")[1].split(":")[0]}")
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:", response.text)
