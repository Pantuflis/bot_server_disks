from art import menu_title_art
import datetime as dt
import email
import imaplib
import json
import os
import smtplib as smtp
import time
from subprocess import PIPE, Popen

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Set emails info
user_email = os.getenv('USER_EMAIL')
password = os.getenv('PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')
emails_dict = json.loads(receiver_email)
emails_keys = list(emails_dict.keys())
emails_list = list(emails_dict.values())
subject_1 = 'Hey you, time to change the world, or the disk...'
message_1 = "Hey there Martin, it's time to change our backup disks, you don't want to get hack again don't you?\nOnce you chaged it, please respond this email with an Ok"
subject_2 = 'Good job with those disks!'
message_2 = "I'm impressed with your ability with those disks, there are now connected and ready. You can continue with your boring job"



# Start menu
def start_menu():
    print(menu_title_art)
    print("###########################################################################\n")
    print(f"[1] Admin     [{emails_list[0]}]")
    print(f"[2] Roberto   [{emails_list[1]}]")
    print(f"[3] Martin    [{emails_list[2]}]")
    print(f"[4] Camila    [{emails_list[3]}]")
    print(f"[5] Victoria  [{emails_list[4]}]")
    print(f"[6] Juan      [{emails_list[5]}]")
    print(f"[7] Exit\n")
    options = [1, 2, 3, 4, 5, 6]
    option_selected = int(input("Please select an option from the list: "))
    if option_selected == 7:
        print("Closing program...")
        time.sleep(2)
        exit()
    elif option_selected in options:
        global email_selected
        email_selected = emails_list[option_selected - 1]
        confirm_selection = input(f"The email selected is {email_selected}, you want to continue? [Y/N]: ")
        if confirm_selection.lower() == "y":
            print("Starting program...")
            time.sleep(5)
            os.system("cls")
            start_bot()
        elif confirm_selection.lower() == "n":
            os.system("cls")
            start_menu()
    else:
        print("Please select a valid option from the list")
        time.sleep(5)
        start_menu()


# Get the day and time in str format
def date_now():
    now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return now

# Get the day and time in str format plus some time you want
def date_plus(plus):
    now_plus = (dt.datetime.now() + dt.timedelta(seconds=plus)).strftime("%d/%m/%Y %H:%M:%S")
    return now_plus


# Control the actual time against the time that the next process needs to start
def get_checktime():
    now = dt.datetime.now()
    control_now = float(dt.datetime.now().strftime("%H.%M"))
    control_time = 17.00
    difference = str(round(float(control_now - control_time), 2))
    splitted_time = difference.split('.')
    splitted_time = list(map(int, splitted_time))
    seconds_difference = splitted_time[0] * 3600 + splitted_time[1] * 60
    seconds_difference = (86400 - seconds_difference)
    next_check = (now + dt.timedelta(seconds=seconds_difference)).strftime("%d/%m/%Y %H:%M:%S")
    return next_check, seconds_difference

def disconnect_disk():
    cmd = Popen('cmd.exe', stdin = PIPE)
    cmd.stdin.write(b"diskpart\n")
    cmd.stdin.write(b"select volume 5\n")
    cmd.stdin.write(b"remove dismount all")
    return True

def connect_disk():
    cmd = Popen('cmd.exe', stdin = PIPE)
    cmd.stdin.write(b"diskpart\n")
    cmd.stdin.write(b"select volume 5\n")
    cmd.stdin.write(b"assign letter d")

# Check day and time
def check_day():
    today = dt.datetime.now().weekday()
    if today == 2 or today == 4:
        while today:
            is_sended = check_time()
            if is_sended:
                return True
            else:
                now = date_now()
                now_plus = date_plus(900)
                print(f"[{now}] I'm sleeping from {now} to my next check at {now_plus}")
                time.sleep(900)                

# Check time
def check_time():
    hour = dt.datetime.now().time()
    str_hour = hour.strftime("%H.%M")
    float_hour = float(str_hour)
    # float_hour = 17.10
    if float_hour >= 17:
        now = date_now()
        print(f'[{now}] Sequency initiated, disconnecting disk...')
        disconnect_disk()
        time.sleep(600)
        send_email(subject_1, message_1)
        return True

# Function to send email
def send_email(subject, message):
    with smtp.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user_email, password=password)
        connection.sendmail(
            from_addr=user_email,
            to_addrs=email_selected,
            msg=f"Subject: {subject}\n\n{message}"
        )
        now = date_now()
        print(f'[{now}] Mail sended to {email_selected} ')

def replace_months(month):
    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }
    return str(months[month])

def get_email_time(email_date):
    email_date = email_date.replace(':', ' ')
    split_email_date = email_date.split(" ")
    month = replace_months(split_email_date[1])
    split_email_date[1] = month
    int_email_date = [int(string) for string in split_email_date]
    email_time = dt.datetime(int_email_date[2], int_email_date[1], int_email_date[0], int_email_date[3], int_email_date[4], int_email_date[5])
    return email_time

def check_email_time(email_content, email_time, send_time, from_address):
# Check if the email received is new                
    if email_content[0:2].lower() == ('ok'):
        now = date_now()
        if email_time > send_time:
            print(f'[{now}] Response received successfully from {from_address}, connecting the disk...')
            connect_disk()
            time.sleep(5)
            send_email(subject_2, message_2)
            return True
        else:
            print(f'[{now}] Waiting for email response "Ok" at {user_email}')
            time.sleep(300)


def read_emails(send_time):
    is_email_sent = False
    while not is_email_sent:
        with imaplib.IMAP4_SSL('imap.gmail.com') as connection:
            connection.login(user_email, password)
            connection.select('inbox')
            # Search all the emails ids in the inbox
            result, data = connection.uid('search', None, 'ALL')
            inbox_emails = data[0].split()
            last_mail = inbox_emails[-1]

            # Select an email and get all the content
            result, email_data = connection.uid('fetch', last_mail, '(RFC822)')
            raw_email = email_data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email)
            from_address = email_message['From']
            email_date = email_message['Date'][5:24]
            email_time = get_email_time(email_date)

            # Loop in the email lookin the different items in it
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    break
            content_type = part.get_content_type()
            print(content_type)
            if 'html' in content_type:
                html_content = part.get_payload()
                soup = BeautifulSoup(html_content, 'html.parser')
                email_content = soup.get_text()
                is_email_sent = check_email_time(email_content, email_time, send_time, from_address)
            elif 'alternative' in content_type:
                alternative_content = part.get_payload()
                alternative_content = alternative_content[1].get_payload()
                soup = BeautifulSoup(alternative_content, 'html.parser')
                email_content = soup.get_text()
                is_email_sent = check_email_time(email_content, email_time, send_time, from_address)
            elif 'related' in content_type:
                related_content = part.get_payload()
                related_content = related_content[0].get_payload()
                soup = BeautifulSoup(related_content, 'html.parser')
                email_content = soup.get_text()
                is_email_sent = check_email_time(email_content, email_time, send_time, from_address)

                
def start_bot():
    while True:
        is_day_correct = check_day()
        if is_day_correct:            
            send_time = dt.datetime.now()
            time.sleep(10)
            read_emails(send_time)
            now = date_now()
            check_time = get_checktime()
            print(f"[{now}] I'm sleeping from {now} to my next check at {check_time[0]}")
            time.sleep(check_time[1])
        else:
            now = date_now()
            wake_up_time = get_checktime()
            print(f"[{now}] I'm sleeping from {now} to my next check at {wake_up_time[0]}")
            time.sleep(wake_up_time[1])


if __name__ == "__main__":
    start_menu()