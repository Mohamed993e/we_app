from core.user import *
from core.record import *
from core.remote import *


if(__name__ == "__main__"):
    us = User()
    if not us.isAuth:
        us.username = input("Enter Username: ")
        us.password = input("Enter Password: ")
    print(us.getRecord())
