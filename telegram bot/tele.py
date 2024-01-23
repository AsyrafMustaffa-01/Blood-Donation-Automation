import requests
import datetime
age = 20
bot_url = "https://api.telegram.org/bot6905941845:AAEE8qD7HZ0GJYO5BT6kvoATAi1jFBFGF0g/sendPhoto"

files = {"photo" : open("D:\\output.png", 'rb')}
file = open(r'C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\telegram bot\\log.txt', 'a')

parameter = {
    "chat_id" : "-4171022632",
    "caption" : f"The Demographic shows that blood donor around the age {age} is the most frequent returning blood donor."
}

resp = requests.get(bot_url,data=parameter, files=files)
file.write(f'{datetime.datetime.now()} - script successfully run \n')