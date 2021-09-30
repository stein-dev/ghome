import requests
import json
import os
from random import randint
import signal
from colorama import Fore, Back
from colorama import init
init(autoreset=True)

url_verify = "https://globeathomeapp.globe.com.ph/api2/v6/register/verify"
url_activate = "https://globeathomeapp.globe.com.ph/api2/v2/register/activate-sim"
filename = "ghome_db.txt"
counter = 0
nsleep = 5

payload = {
        "User-Agent": "BBAPP/Android 12/Pixel 5a/2.66.1(1744)",
        "Authorization": "", 
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "deny",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "x-current-platform": "bb-android",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "globeathomeapp.globe.com.ph",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip" 
}

def handler(signum, frame):
    print(Fore.CYAN + "Exiting program. Bye! @pigscanfly")
    exit(1)
       
signal.signal(signal.SIGINT, handler)

def randomNumber():
    algonum = '0945044'
    for x in range(4):
        value = randint(0, 9)
        algonum = algonum + str(value)
    return str(algonum)

# def randomNumber():
#     algonum = '09661186'
#     value = randint(100, 999)
#     algonum = algonum + str(value)
#     return str(algonum)



def verifyNum():

    global num
    num = randomNumber() 

    body = {"customer_identifier": num}
    
    print("Verifying number: " + num)
    tmp = requestApi(url_verify, body, payload)
    resp_len = len(tmp)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif 'results' in data.keys():
        if resp_len > 100:
            print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + str(data['results']))
        elif resp_len < 100:
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Message: " + str(data['results']))
            activateNum()
        else:
            print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + str(data))    

def activateNum():

    body = {"customer_identifier": num}
    
    print("Activating number: " + num)
    tmp = requestApi(url_activate, body, payload)
    resp_len = len(tmp)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif 'results' in data.keys():    
        print(Back.LIGHTGREEN_EX + Fore.BLACK + "Message: " + str(data['results']))
        verifyNum()

def requestApi(str1, str2, str3):
     r = requests.post(str1, data=json.dumps(str2), headers=str3)
     return r.content        

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    else:
        command  = 'clear' 
    os.system(command)  

def handler(signum, frame):
    print(Fore.CYAN + "Exiting program. Bye! @pigscanfly")
    exit(1)
       
signal.signal(signal.SIGINT, handler)

def main():
    clearConsole()
    print(Back.LIGHTCYAN_EX + Fore.BLACK + 'GHome-Checker by @pigscanfly')
    print("=====================================")
    global num     
    num = input("Enter mobile: ")
    activateNum()

main()    