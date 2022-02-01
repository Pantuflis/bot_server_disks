import os
import json
import time
from soupsieve import Iterable
from art import menu_title_art
from dotenv import load_dotenv

load_dotenv()

receiver_mail = os.getenv('RECEIVER_EMAIL')
emails_dict = json.loads(receiver_mail)
emails_list = list(emails_dict.values())
# print(emails_list)

def run():
    print(menu_title_art)
    print("###########################################################################\n")
    print("[1] Admin     [confidential]")
    print("[2] Roberto   [roberto.estudiodc@gmail.com]")
    print("[3] Martin    [martin.estudiodc@gmail.com]")
    print("[4] Camila    [camila.estudiodc@gmail.com]")
    print("[5] Victoria  [victoria.estudiodc@gmail.com]")
    print("[6] Juan      [juan.estudiodc@gmail.com]")
    print("[7] Exit\n")
    options = [1, 2, 3, 4, 5, 6]
    print_options()
    mail_selected = int(input("Please select an option from the list: "))
    if mail_selected == 7:
        print("Closing program...")
        time.sleep(2)
        exit()
    elif mail_selected in options:
        confirm_selection = input(f"The email selected is {emails_list[mail_selected - 1]}, you want to continue? [Y/N]: ")
        if confirm_selection.lower() == "y":
            print("Starting program...")
            time.sleep(5)
            os.system("cls")
            #start bot
        elif confirm_selection.lower() == "n":
            os.system("cls")
            run()
    else:
        print("Please select a valid option from the list")
        time.sleep(5)
        run()



if __name__ == '__main__':
    run()
