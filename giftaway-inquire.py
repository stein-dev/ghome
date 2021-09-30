import requests
import json

url = "https://gform.entry.ph/api/globe/inquire"
url_redeem = "https://gform.entry.ph/api/globe/v2/redeem"
url2 = "https://gform.entry.ph/api/globe/voucher/"
id = "4571f03a-9c2a-4cf0-acb0-fcb23ff1da41"
voucher_id = "aa2d8398-f91f-412a-b275-1118e7d5a6bf"
code = "G54T8KBK28"

#https://gform.entry.ph/campaign/v2/globe91721/G54T8KBK28

def requestPostApi(str1, str2, str3):
     r = requests.post(str1, data=json.dumps(str2), headers=str3)
     return r.content

def requestNoBodyPostApi(str1, str3):
     r = requests.post(str1, headers=str3)
     return r.content     

def inq():
    payload = {
        "Host": "gform.entry.ph",
        "User-Agent": "Mozilla/5.0 (Android 9; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-PH",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Origin": "https://gform.entry.ph",
        "Connection": "keep-alive",
        "Referer": "https://gform.entry.ph/campaign/v2/globe91721/" + id + "/" + code,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    body = {"code": code,"id": id}
    new_url = url + "/" + code

    print("Sending inquire request...")
    print("")
    tmp = requestPostApi(new_url, body, payload)
    data = json.loads(tmp)
    global voucher_id
    voucher_id = data['data']['voucher']['id']
    print(voucher_id)

def red():
    payload = {
        "Host": "gform.entry.ph",
        "User-Agent": "Mozilla/5.0 (Android 9; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-PH",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Origin": "https://gform.entry.ph",
        "Connection": "keep-alive",
        "Referer": "https://gform.entry.ph/campaign/v2/globe91721/" + id + "/" + code,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    body = {"code": code,"id": id}
    new_url = url + "/" + code

    print("Sending inquire request...")
    print("")
    tmp = requestNoBodyPostApi(url_redeem, payload)
    data = json.loads(tmp)
    print(data)

        
inq()  