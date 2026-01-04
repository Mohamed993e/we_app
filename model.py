import requests
import json
import os
import datetime

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

# Example usage
class Record:
    def __init__(self, total: float, used: float, remain: float, effectiveTime: int, expireTime: int):
        self.total = total
        self.used = used
        self.remain = remain
        self.effectiveTime = effectiveTime
        self.expireTime = expireTime

    @staticmethod
    def from_json(json_data: dict) -> 'Record':
        # Assuming json_data contains the relevant structure as per the original JSON
        body = json_data['body'][0]
        
        # Extract data from the body
        total = body['total']
        used = body['used']
        remain = body['remain']
        effectiveTime = body['effectiveTime']
        expireTime = body['expireTime']
        
        # Create Record object
        return Record(total, used, remain, effectiveTime, expireTime)
    def convert_timestamp(self, timestamp: int) -> str:
        # Convert Unix timestamp (milliseconds) to a human-readable date
        return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    @property
    def get_effective_time(self) -> str:
        # Convert and return effective time
        return self.convert_timestamp(self.effectiveTime)
    @property
    def get_expire_time(self) -> str:
        # Convert and return expire time
        return self.convert_timestamp(self.expireTime)
    def __str__(self) -> str:
        # Override __str__ to provide a more user-friendly string representation
        return (f"Record Details:\n"
                f"  Total: {self.total} GB\n"
                f"  Used: {self.used} GB\n"
                f"  Remaining: {self.remain} GB\n"
                f"  Effective Time: {self.get_effective_time}\n"
                f"  Expiry Time: {self.get_expire_time}\n")

class User: 
    username : str =" "
    password : str =" "
    indiv_login_token : str =" "
    subscriber_id : str =" "
    csrftoken : str =" "
    
    def __init__(self , load : bool = True):
        if load:
            data = self.load()
            if data!= None:
                self.username = data["username"]
                self.password = data["password"]
                self.indiv_login_token = data["indiv_login_token"]
                self.subscriber_id = data["subscriber_id"]
                self.csrftoken = data["csrftoken"]

    def getToken(self):
        if not self.isAuth:
            raise Exception("no User or Password") 
        result = authenticate_user(username= f"FBB{self.username}" , password= self.password)
        self.indiv_login_token = result["body"]["utoken"]
        self.subscriber_id = result["body"]["subscriber"]["subscriberId"]
        self.csrftoken = result["body"]["token"]
        self.save()

    def getRecord(self)->Record:
        data = query_free_unit(self.subscriber_id,self.indiv_login_token,self.csrftoken)
        return Record.from_json(data)
    
    def __str__(self):
        return json.dumps( {
            "username" : self.username,
            "password" : self.password,
            "indiv_login_token" : self.indiv_login_token,
            "subscriber_id" : self.subscriber_id,
            "csrftoken" : self.csrftoken,
        } ,indent=2)
    
    @property
    def isAuth(self)->bool:
        return len(self.username) > 6 and len(self.password) > 8
    
    def save(self):
        data=open("user.json" , "w")
        data.writelines(self.__str__())
        data.close()

    def load(self):
        try:
            ex =os.path.exists("user.json")
            if ex:
                fil=open("user.json" , "r")
                lines = fil.read().replace("\n" , "")
                data  = json.loads(lines)
                fil.close()
                return data
        finally:
            pass





if(__name__ == "__main__"):
    us = User()
    us.getToken()
    print(us.getRecord())

    




# result = query_free_unit(subscriber_id, indiv_login_token, csrftoken)

# print(result)
