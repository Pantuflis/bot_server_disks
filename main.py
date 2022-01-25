from cProfile import run
import datetime as dt
import email
import imaplib
import os
import smtplib as smtp
import time
from subprocess import PIPE, Popen

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Set emails info
user_mail = os.getenv('TEST_MAIL')
password = os.getenv('PASSWORD')
receiver_mail = os.getenv('TEST_EMAIL')
subject_1 = 'Hey you, time to change the world, or the disk...'
message_1 = "Hey there Martin, it's time to change our backup disks, you don't want to get hack again don't you?\nOnce you chaged it, please respond this email with an Ok"
subject_2 = 'Good job with those disks!'
message_2 = "I'm impressed with your ability with those disks, there are now connected and ready. You can continue with your boring job"

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
    return next_check

def disconnect_disk():
    cmd = Popen('cmd.exe', stdin = PIPE)
    cmd.stdin.write(b"diskpart\n")
    cmd.stdin.write(b"select volume 5\n")
    cmd.stdin.write(b"remove dismount all")

def connect_disk():
    cmd = Popen('cmd.exe', stdin = PIPE)
    cmd.stdin.write(b"diskpart\n")
    cmd.stdin.write(b"select volume 5\n")
    cmd.stdin.write(b"assign letter d")

# Check day and time
def check_day():
    today = dt.datetime.now().weekday()
    if today == 2 or today == 3:
        while today:
            is_sended = check_time()
            if is_sended:
                return True
            else:
                time.sleep(300)

# Check time
def check_time():
    hour = dt.datetime.now().time()
    str_hour = hour.strftime("%H.%M")
    float_hour = float(str_hour)
    # float_hour = 17.10
    if float_hour >= 17:
        disconnect_disk()
        time.sleep(900)
        send_email(subject_1, message_1)

# Function to send email
def send_email(subject, message):
    with smtp.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user_mail, password=password)
        connection.sendmail(
            from_addr=user_mail,
            to_addrs=receiver_mail,
            msg=f"Subject: {subject}\n\n{message}"
        )
        now = date_now()
        print(f'Mail sended to {receiver_mail} - {now}')

def read_emails(send_time):
    while True:
        with imaplib.IMAP4_SSL('imap.gmail.com') as connection:
            connection.login(user_mail, password)
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
            email_time = float(email_message['Date'][17:22].replace(':', '.'))

            # Loop in the email lookin the different items in it
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    break
            content_type = part.get_content_type()
            if 'html' in content_type:
                html_content = part.get_payload()
                soup = BeautifulSoup(html_content, 'html.parser')
                email_content = soup.get_text()

            # Check if the email received is new                
                if email_content[0:2] == ('ok'.lower()):
                    now = date_now()
                    if email_time > send_time:
                        print(f'Response received successfully from {from_address}, connecting the disk... - {now}')
                        connect_disk()
                        time.sleep(5)
                        send_email(subject_2, message_2)
                        break
                    else:
                        print(f'Waiting for email response "Ok" at {user_mail} - {now}')
                        time.sleep(300)
                
def run():
    while True:
        is_day_correct = check_day()
        if is_day_correct:            
            now = date_now()
            send_time = float(now[11:16].replace(":", "."))
            time.sleep(10)
            read_emails(send_time)
            new_now = date_now()
            now_plus = get_checktime()
            print(f"Im sleeping from {new_now} to my next check at {now_plus}")
            time.sleep(86400)
        else:
            now = date_now()
            now_plus = date_plus(7200)
            print(f"Im sleeping from {now} to my next check at {now_plus}")
            time.sleep(900)

if __name__ == "__main__":
    run()