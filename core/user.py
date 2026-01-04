
import os
import json
from core.remote import authenticate_user, query_free_unit
from core.record import Record

class User: 
    username : str =" "
    password : str =" "
    indiv_login_token : str =" "
    subscriber_id : str =" "
    csrftoken : str =" "
    
    def __init__(self , load : bool = True , username : str =" " , password : str =" "):
        self.username = username
        self.password = password
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
        if "errorMsg" in result["header"]:
            raise Exception(f"user or pass invalid {result['header']['errorMsg']}")
        self.indiv_login_token = result["body"]["utoken"]
        self.subscriber_id = result["body"]["subscriber"]["subscriberId"]
        self.csrftoken = result["body"]["token"]
        self.save()

    def getRecord(self)->Record:
        data = query_free_unit(self.subscriber_id,self.indiv_login_token,self.csrftoken)
        if "errorMsg" in data["header"]:
            print( data['header']['errorMsg'])
            self.getToken()
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
    @property
    def is_logged_in(self)->bool:
        return len(self.indiv_login_token) > 4 and len(self.subscriber_id) >4 and len(self.csrftoken) >4
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
    def clear(self):
        try:
            ex =os.path.exists("user.json")
            if ex:
                os.remove("user.json")
        finally:
            pass