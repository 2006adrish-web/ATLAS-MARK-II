import time

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.08
except ImportError:
    raise RuntimeError("Install pyautogui first: pip install pyautogui")

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False


def _paste(text: str):

    if HAS_CLIPBOARD:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.write(text, interval=0.02)


def open_whatsapp():

    pyautogui.press("win")
    time.sleep(0.5)

    _paste("WhatsApp")
    time.sleep(0.5)

    pyautogui.press("enter")

    time.sleep(3)


def search_contact(contact: str):

    pyautogui.hotkey("ctrl", "alt","/")
    time.sleep(0.4)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    _paste(contact)

    time.sleep(3.2)

    pyautogui.press("down")
    time.sleep(1.3)

    pyautogui.press("enter")

    time.sleep(1.8)


def send_text(message: str):

    _paste(message)

    time.sleep(1.2)

    pyautogui.press("enter")


def send_whatsapp_message(contact: str, message: str):

    try:

        open_whatsapp()

        search_contact(contact)

        send_text(message)

        return f"Message sent to {contact}"

    except Exception as e:

        return f"Failed: {e}"