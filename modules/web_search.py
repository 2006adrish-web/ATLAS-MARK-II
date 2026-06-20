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


def open_browser():

    pyautogui.press("win")
    time.sleep(0.5)

    _paste("Edge")
    time.sleep(0.5)

    pyautogui.press("enter")

    time.sleep(1.5)


def search(query: str):

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    _paste(query)

    time.sleep(0.8)

    pyautogui.press("enter")

    time.sleep(0.8)





def searchit(query: str):

    try:

        open_browser()

        search(query)

  

        return f"Searched {query}"

    except Exception as e:

        return f"Failed: {e}"