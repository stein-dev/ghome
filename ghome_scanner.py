import requests
import json
import os
import sys
from random import randint
import time
import signal
import argparse
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
        updateFile(filename, num)

def createFile(str1):
    if not os.path.exists(str1):
        with open(str1, "w") as file:
            file.close()    

def updateFile(str1, str2):
    print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saving " + num + " to ghome_db..." )
    with open(str1, "a") as file:
        file.write(str2 + "\n")
        file.truncate()
        file.close()
        print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saved!" )

def requestApi(str1, str2, str3):
     r = requests.post(str1, data=json.dumps(str2), headers=str3)
     return r.content

def mainProg(int1):
    
    print(Back.LIGHTCYAN_EX + Fore.BLACK + 'GHome-Auto by @pigscanfly')
    global counter
    if int1 == 0:
        while True:
            counter = counter + 1
            print("Request #" + str(counter) + ":")
            print("==================================")
            verifyNum()
            time.sleep(nsleep)
            print("")
    else:            
        for x in range(int1):
            counter = counter + 1
            print("Request #" + str(counter) + ":")
            print("==================================")
            verifyNum()
            time.sleep(2)
            print("")

parser = argparse.ArgumentParser(description = "Globe at Home Automator by @pigscanfly")
parser.add_argument("-l", "--loop", help = "number of times to loop. 0 for infinite loop.", required=True)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

if args.loop:
    createFile(filename)
    x = int(args.loop)
    mainProg(x)
    

