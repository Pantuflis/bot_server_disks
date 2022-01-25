import os
import time
import datetime as dt
from subprocess import PIPE, Popen

# def disconnect_disk():
#     cmd = Popen('cmd.exe', stdin = PIPE)
#     cmd.stdin.write(b"diskpart\n")
#     cmd.stdin.write(b"select volume 5\n")
#     cmd.stdin.write(b"remove dismount all")

# def connect_disk():
#     cmd = Popen('cmd.exe', stdin = PIPE)
#     cmd.stdin.write(b"diskpart\n")
#     cmd.stdin.write(b"select volume 5\n")
#     cmd.stdin.write(b"assign letter d")
#     return True

# def hello():
#     is_disk_connected = True
#     while is_disk_connected:
#         print("Waiting")
#         time.sleep(300)

def run():
    now = dt.datetime.now()
    control_now = float(dt.datetime.now().strftime("%H.%M"))
    control_time = 17.00
    difference = str(round(float(control_now - control_time), 2))
    splitted_time = difference.split('.')
    splitted_time = list(map(int, splitted_time))
    seconds_difference = splitted_time[0] * 3600 + splitted_time[1] * 60
    seconds_difference = (86400 - seconds_difference)
    next_check = (now + dt.timedelta(seconds=seconds_difference)).strftime("%d/%m/%Y %H:%M:%S")
    print(next_check)


if __name__ == '__main__':
    run()