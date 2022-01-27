import os
import time
import datetime as dt
from subprocess import PIPE, Popen
import imaplib
import smtplib as smtp
from dotenv import load_dotenv
import json
import email
from bs4 import BeautifulSoup

load_dotenv()

def date_now():
    now = dt.datetime.now()
    return now

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
    date = email_date.split(" ")
    month = replace_months(date[1])
    date[1] = month
    int_dates = [int(string) for string in date]
    email_time = dt.datetime(int_dates[2], int_dates[1], int_dates[0], int_dates[3], int_dates[4], int_dates[5])
    return email_time

# def run():
# #     string = '26 Jan 2022 17:17:10'
# #     string_forated = string.replace(':', ' ')
# #     date = string_forated.split(" ")
# #     month = replace_months(date[1])
# #     date[1] = month
# #     int_dates = [int(string) for string in date]
# #     final_date = dt.datetime(int_dates[2], int_dates[1], int_dates[0], int_dates[3], int_dates[4], int_dates[5])
#     pass

def check_email_time(email_content, email_time, send_time, from_address):
# Check if the email received is new            
    if email_content[0:2].lower() == ('ok'):
        now = date_now()
        print(email_time, send_time)
        if email_time >= send_time:
            print(f'Response received successfully from {from_address}, connecting the disk... - {now}')
            # connect_disk()
            time.sleep(5)
            # send_email(subject_2, message_2)
            return True
        else:
            print(f'Waiting for email response "Ok" at {email_time} - {now}')
            time.sleep(10)

def read_emails(send_time):
    is_sended = False
    while not is_sended:
        with imaplib.IMAP4_SSL('imap.gmail.com') as connection:
            connection.login("botsistemas.estudiodc@gmail.com", "estudioDC8080")
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
            email_date = email_message['Date'][5:25]
            email_time = get_email_time(email_date)

            # Loop in the email lookin the different items in it
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    break
            content_type = part.get_content_type()
            if 'html' in content_type:
                print('html')
                html_content = part.get_payload()
                soup = BeautifulSoup(html_content, 'html.parser')
                email_content = soup.get_text()
                check_email_time(email_content, email_time, send_time, from_address)
            elif 'alternative' in content_type:
                print('alternative')
                alternative_content = part.get_payload()
                alternative_content = alternative_content[1].get_payload()
                soup = BeautifulSoup(alternative_content, 'html.parser')
                email_content = soup.get_text()
                is_sended = check_email_time(email_content, email_time, send_time, from_address)


if __name__ == '__main__':
    now = dt.datetime.now()
    read_emails(now)