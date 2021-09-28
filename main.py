import discord
import os 
import requests
import json
import random 
from keep_alive import keep_alive


my_secret = os.environ['token']

client=discord.Client()
def news_on_topic(topic):
  

  url = 'https://newsapi.org/v2/everything?'
  parameters = {
    'q': topic,
    'pageSize': 5,  # maximum is 100
    'apiKey': "4dbc17e007ab436fb66416009dfb59a8"
 
   }

  response = requests.get(url, params=parameters)


  response_json = response.json()
  
  lst=[]
  
  for i in response_json['articles']:
    lst.append(i['title'])
    
  return lst


def weather(city):
  api_key= "f1bc759caccfd06424345249b4433429"
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
  complete_url = base_url + "appid=" + api_key + "&q=" +city
  response = requests.get(complete_url)
  x = response.json()
  if x["cod"] != "404":
     y = x["main"]
     current_temperature = y["temp"]
     current_pressure = y["pressure"]
     current_humidity = y["humidity"]
     z = x["weather"]
     weather_description = z[0]["description"]
     #current_temperature=current_temperature-273.15
  return current_temperature,current_pressure,current_humidity,weather_description
  
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  news=[]
  if message.content.startswith("$news"):
    topic= message.content.split("$news ",1)[1]
    news = news_on_topic(topic)
    for i in news:
       await message.channel.send(i)

  if message.content.startswith("$weather"):
    city= message.content.split("$weather ",1)[1]
    
    
    temp,atmospheric_pressure,humidity,description=weather(city)
    await message.channel.send("City name: "+ str(city))
    await message.channel.send(" Temperature (in kelvin unit) = "+str(temp))
    await message.channel.send("\n Atmospheric pressure (in hPa unit) = "+str(atmospheric_pressure))
    await message.channel.send("\n Humidity (in percentage) ="+str(humidity))
    await message.channel.send("\n Description ="+str(description))
                    


keep_alive()
client.run(os.environ['token'])








