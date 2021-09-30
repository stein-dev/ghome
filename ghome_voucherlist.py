import requests
import json
import uuid
import signal
import os
import random
import argparse
import sys
import base64
from Crypto.Cipher import AES
from colorama import Fore, Back
from colorama import init
init(autoreset=True)

url_prepaidthreshold = "https://globeathomeapp.globe.com.ph/api2/v5/register/prepaid-threshold"
url_sendotp = "https://globeathomeapp.globe.com.ph/api2/v6/register/send-otp"
url_verifyotp = "https://globeathomeapp.globe.com.ph/api2/v6/register/verify-otp"
url_login = "https://globeathomeapp.globe.com.ph/api2/v6/login/"
url_developerid = "https://globeathomeapp.globe.com.ph/api2/v2/accesstoken?"
url_prepaiddetails = "https://globeathomeapp.globe.com.ph/api2/v2/account/prepaid-details"
url_deviceregister = "https://globeathomeapp.globe.com.ph/api2/v4/device/register"
url_devicepin = "https://globeathomeapp.globe.com.ph/api2/v6/device/pin-code"
url_voucher = "https://globeathomeapp.globe.com.ph/api2/v5/cms/voucher/voucher-list?"

SECRETKEY = b"BlYqXOB1NGeGRjiPc1W5OgWe1s5WP8XU"
IVPHRASE = b"xBLgCk4Krx3c8vxT"

filename1 = "ghome_accounts.db"
filename2 = "ghome_vouchers.db"
pincode = "123123"

payload = {
    "Host": "globeathomeapp.globe.com.ph",
    "User-Agent": "BBAPP/Android 11/Xiaomi Redmi Note 10S/2.66.1(1744)",
    "Authorization": "",
    "Strict-Transport-Security": "max-age=31536000",
    "X-Frame-Options": "deny",
    "X-Xss-Protection": "1; mode=block",
    "X-Content-Type-Options": "nosniff",
    "X-Current-Platform": "bb-android",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept-Encoding": "gzip",
}

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

def requestPostApi(str1, str2, str3):
     r = requests.post(str1, data=json.dumps(str2), headers=str3)
     return r.content

def requestGetApi(str1, str2):
     r = requests.get(str1, headers=str2)
     return r.content   

def textDecrypt(encText):
    tmp = base64.b64decode(encText)
    cipher = AES.new(SECRETKEY, AES.MODE_CBC, IVPHRASE)
    return str(cipher.decrypt(tmp).decode('utf-8'))

def voucherList(num, access_token):
    payload2 = {
        "Host": "globeathomeapp.globe.com.ph",
        "User-Agent": "BBAPP/Android 11/Xiaomi Redmi Note 10S/2.66.1(1744)",
        "Authorization": access_token,
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "deny",
        "X-Xss-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "X-Current-Platform": "bb-android",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }
    print("")
    print("Getting voucher list..")
    print("")
    new_url = url_voucher + "customer_identifier=" + num + "&device_id=" + device_id
    tmp = requestGetApi(new_url, payload2)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        for data in data['results']:
            sponsor_name = data['sponsors'][0]['cms_vouchers'][0]['sponsor_name']
            desc = data['sponsors'][0]['cms_vouchers'][0]['short_description']
            code = data['sponsors'][0]['cms_vouchers'][0]['vouchers'][0]['code']
            exp = data['sponsors'][0]['cms_vouchers'][0]['vouchers'][0]['expiration_date']
            decoded_code = textDecrypt(code)
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Name: " + sponsor_name)
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Description: " + desc)
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Code: " + decoded_code)
            print(Back.LIGHTGREEN_EX + Fore.BLACK + "Expiration: " + exp)
            print("")
            updateVoucherFile(num, decoded_code, sponsor_name)
    else:
        print(data)

def devicePin(num, access_token):
    payload = {
        "Host": "globeathomeapp.globe.com.ph",
        "User-Agent": "BBAPP/Android 11/Xiaomi Redmi Note 10S/2.66.1(1744)",
        "Authorization": access_token,
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "deny",
        "X-Xss-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "X-Current-Platform": "bb-android",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }
    body = {"customer_identifier":num,"first_code": pincode,"second_code": pincode}
    print("")
    print("Setting pin...")
    print("")
    tmp = requestPostApi(url_devicepin, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + str(data['results']))
        updateFile(num, email, pincode)
        voucherList(num, access_token)
    else:
        print(data) 

def deviceRegister(num, access_token):
    payload = {
        "Host": "globeathomeapp.globe.com.ph",
        "User-Agent": "BBAPP/Android 11/Xiaomi Redmi Note 10S/2.66.1(1744)",
        "Authorization": access_token,
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "deny",
        "X-Xss-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "X-Current-Platform": "bb-android",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }
    body = {
        "customer_identifier":num,
        "app_version":"2.66.1(1744)",
        "customer_type":"PREPAID",
        "device_id": device_id,
        "device_model":"Pixel 5a",
        "device_name":"Google Pixel",
        "device_token":"c1gumHi6Q6aOZanH-niDYw:APA91bEqyfiqzxStHUZToOu_EEoKJZYep79CPImcoMzVZPHVnhZOhJlPbW_kRgXvA5oOX23st2wv0UDJypWXPafCetwnMsZnbYOiNUVC7YZaDZg7eEdrTPrP9Z5vDl94TVybjCZsW_Og",
        "email_address":"",
        "os_version":"Android 12",
        "platform":"ANDROID"
    }

    print("")
    print("Registering device...")
    print("")
    tmp = requestPostApi(url_deviceregister, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + str(data['results']))
        devicePin(num, access_token)
    else:
        print(data) 

def sendPrepaidDetails(num, email, refid, access_token):
    body = {
        "customer_identifier":num,
        "dob":"June 19, 1998",
        "email":email,
        "email_otp_verified":True,
        "first_name":"Manny",
        "last_name":"Pangilinan",
        "mobile": num2,
        "mobile_otp_verified":False,
        "reference_id":refid
    }
    payload = {
        "Host": "globeathomeapp.globe.com.ph",
        "User-Agent": "BBAPP/Android 11/Xiaomi Redmi Note 10S/2.66.1(1744)",
        "Authorization": access_token,
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "deny",
        "X-Xss-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "X-Current-Platform": "bb-android",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }
    print("")
    print("Sending prepaid details...")
    print("")
    tmp = requestPostApi(url_prepaiddetails, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + data['results'])
        deviceRegister(num, access_token)
    else:
        print(data) 

def getDeveloperID(developer_id, clientid, num, refid):
    print("")
    print("Getting access token...")
    print("")
    new_url = url_developerid + "developer_id=" + developer_id + "&client_id=" + clientid
    tmp = requestGetApi(new_url, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        client_id = data['results']['client_id']
        access_token = data['results']['access_token']
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Client ID: " + client_id)
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Access Token: " + access_token)
        sendPrepaidDetails(num, email, refid, access_token)
    else:
        print(data)

def login(otpcode, num, refid, token):
    body = {
        "code": otpcode,
        "customer_identifier": num,
        "device_id": device_id,
        "is_otp": False,
        "reference_id": refid,
        "token": token,
        "type":"EMAIL_ADDRESS"
    }
    print("Logging in...")
    print("")
    tmp = requestPostApi(url_login + num, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        developer_id = data['results']['developer_id']
        client_id = data['results']['client_id']
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Developer ID: " + developer_id)
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Client ID: " + client_id)
        getDeveloperID(developer_id, client_id, num, refid)
    else:
        print(data) 


def generateDeviceID():
    a = str(uuid.uuid1())
    aa = a.encode('UTF-8')
    return str(aa.decode('UTF-8'))


def verifyOtp(num, refid, token):
    print("")
    otpcode = input("Input otp code: ")
    print("")
    body = {"code": otpcode,"customer_identifier": num,"reference_id": refid}
    tmp = requestPostApi(url_verifyotp, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        refid = data['results']['reference_id']
        msg = data['results']['message']
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + msg)
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Ref ID: " + refid)
        print("")
        login(otpcode, num, refid, token)
    else:
        print(data)   

def sendOtp(num, email):
    global device_id
    device_id = generateDeviceID()
    print("")
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Device ID: " + device_id)
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Mobile: " + num)
    print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Email: " + email)
    print("")
    
    body = { 
        "customer_identifier": num,
        "device_id": device_id,
        "email": True,
        "recipient": email,
        "silent": False,
        "sms": False
    }

    print("Sending otp to : " + email)
    print("")
    tmp = requestPostApi(url_sendotp, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    elif "results" in data.keys():
        refid = data['results']['reference_id']
        token = data['results']['token']
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Ref ID: " + refid)
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Token: " + token)
        verifyOtp(num, refid, token)
    else:
        print(data) 

def generateNum():
    num = '0915178'
    for x in range(4):
        value = random.randint(0, 9)
        num = num + str(value)
    return num

def prepaidThreshold(num, email):
    global num2
    num2 = generateNum()
    body = {    
        "customer_identifier": num,
        "email": email,
        "mobile": num2
    }
    print("")
    print("Sending registration details... ")
    print("")
    tmp = requestPostApi(url_prepaidthreshold, body, payload)
    data = json.loads(tmp)
    if 'error' in data.keys():
        print(Back.LIGHTRED_EX + Fore.BLACK + "Message: " + data['error']['message'])
    else:
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "Message: " + data['results'])
        sendOtp(num, email) 

def generateEmail():
    byom = "@byom.de"
    for x in range(3):
        randomLetter = chr(random.randint(ord('a'), ord('z')))
        byom = randomLetter + byom
    return byom

def createFile(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.close()    

def updateFile(num, email, pin):
    print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saving to ghome_accounts.db..." )
    with open(filename1, "a") as file:
        file.write("Mobile: " + num + "\n")
        file.write("Email: " + email + "\n")
        file.write("Pin: " + pin + "\n")
        file.write("\n")
        file.truncate()
        file.close()
        print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saved!" )
        print("")

def updateVoucherFile(num, voucher_code, sponsor_name):
    print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saving to ghome_vouchers.db..." )
    with open(filename2, "a", encoding="utf-8") as file:
        file.write("Mobile: " + num + "\n")
        file.write("Name: " + sponsor_name + "\n")
        file.write("Voucher: " + voucher_code + "\n")
        file.write("\n")
        file.truncate()
        file.close()
        print(Back.LIGHTGREEN_EX + Fore.BLACK + "Saved!" )
        print("")

def main():
    clearConsole()
    print(Back.LIGHTCYAN_EX + Fore.BLACK + 'GHome-Auto by @pigscanfly')
    print("=====================================")
    num = input("Enter mobile: ")
    global email
    #email = input("Enter email: ")
    email = generateEmail()
    prepaidThreshold(num, email)
    
def main2():
    clearConsole()
    print(Back.LIGHTCYAN_EX + Fore.BLACK + 'GHome-Auto by @pigscanfly')
    print("=====================================")
    num = input("Enter mobile: ")
    global email
    email = input("Enter email: ")
    prepaidThreshold(num, email)

def main3():
    clearConsole()
    print(Back.LIGHTCYAN_EX + Fore.BLACK + 'GHome-Auto by @pigscanfly')
    print("=====================================")
    global num
    num = input("Enter mobile: ")
    global email
    email = input("Enter email: ")
    global pincode
    pincode = input("Enter pincode: ")
    prepaidThreshold(num, email)   

parser = argparse.ArgumentParser(description = "Globe at Home Automator by @pigscanfly")
parser.add_argument("-l", "--login", help = "Login to an existing GHome account", action='store_true')
parser.add_argument("-m", "--manual", help = "Enter email manually", action='store_true')
parser.add_argument("-a", "--auto", help = "Generate email automatically", action='store_true')

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

if args.login:
    print("")
if args.auto:
    createFile(filename1)
    createFile(filename2)
    main()    
if args.manual:
    createFile(filename1)
    createFile(filename2)
    main2()