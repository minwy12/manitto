import time
import requests
import hmac
import base64
import hashlib
import random

members = [
    {"name": "", "number": ""}
]


def make_signature(access_key, secret_key, method, uri, timestamp):
    # timestamp = str(int(time.time() * 1000))
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return signingKey


def send_sms(phone_number, subject, message):
    #  URL
    url = "https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:297101864882:dream/messages"
    # access key
    access_key = "FbiPkgxCWKHnpW6eJGO0"
    # secret key
    secret_key = ""
    # uri
    uri = "/sms/v2/services/ncp:sms:kr:297101864882:dream/messages"
    timestamp = str(int(time.time() * 1000))

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "countryCode": "+82",
        "from": "", # Fill my number
        "content": message,
        "messages": [
            {
                "to": phone_number,
                "subject": subject,
                "content": message
            }
        ]
    }

    key = make_signature(access_key, secret_key, 'POST', uri, timestamp)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': key
    }

    res = requests.post(url, json=body, headers=headers)
    print(res.json())

    return res.json()


if __name__ == "__main__":
    target_pool = members.copy()

    i = 0
    for member in members:
        i+=1

        target_idx = random.randrange(0, len(target_pool))
        while member["name"] == target_pool[target_idx]["name"]:
            print("!중복!")
            target_idx = random.randrange(0, len(target_pool))

        # print(i, "번째:", member["name"], "->", target_pool[target_idx]["name"])
        send_sms(member["number"], "Dream", "당신의 진!짜! 마니또는 \"" + target_pool[target_idx]["name"] + "\" 입니다.")
        target_pool.pop(target_idx)