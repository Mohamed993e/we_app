import requests
import json

def authenticate_user(username, password):
    # The URL for the API endpoint
    url = 'https://my.te.eg/echannel/service/besapp/base/rest/busiservice/v1/auth/userAuthenticate'
    
    # Headers to be included in the request
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://my.te.eg',
        'Referer': 'https://my.te.eg/echannel/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'channelId': '702',
        'csrftoken': '',
        'delegatorSubsId': '',
        'deviceId': '',
        'isCoporate': 'false',
        'isMobile': 'false',
        'isSelfcare': 'true',
        'languageCode': 'en-US',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'systemType': '',
    }

    # Data to be sent with the request
    data = {
        'acctId': username,
        'password': password,
        'appLocale': 'en-US',
        'isSelfcare': 'Y',
        'isMobile': 'Y',
        'recaptchaToken': ''
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        return response.json()  # Return the JSON response if the authentication is successful
    else:
        return {"error": "Authentication failed", "status_code": response.status_code}

def query_free_unit(subscriber_id, indiv_login_token, csrftoken):
    # The URL for the API endpoint
    url = 'https://my.te.eg/echannel/service/besapp/base/rest/busiservice/cz/cbs/bb/queryFreeUnit'
    
    # Headers to be included in the request
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://my.te.eg',
        'Referer': 'https://my.te.eg/echannel/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'channelId': '702',
        'csrftoken': csrftoken,  # Use the provided csrftoken parameter
        'delegatorSubsId': '',
        'deviceId': '',
        'isCoporate': 'false',
        'isMobile': 'false',
        'isSelfcare': 'true',
        'languageCode': 'en-US',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'systemType': '',
    }

    # Cookies to be sent with the request
    cookies = {
        'indiv_login_token': indiv_login_token
    }

    # Data to be sent with the request
    data = {
        'subscriberId': subscriber_id,
        'needQueryPoint': True
    }

    # Send the POST request
    response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(data))

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        return response.json()  # Return the JSON response if the query is successful
    else:
        return {"error": "Query failed", "status_code": response.status_code}
