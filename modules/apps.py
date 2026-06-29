import os
import webbrowser
from modules.voice import speak
import time

LOCAL = os.getenv("LOCALAPPDATA")
PROGRAMFILES = os.getenv("PROGRAMFILES")
PROGRAMFILESX86 = os.getenv("PROGRAMFILES(X86)")


apps = {

    "vscode":{

        "aliases":[
            "vscode",
            "vs code",
            "visual studio code"
        ],

        "paths":[
            os.path.join(
                LOCAL,
                "Programs",
                "Microsoft VS Code",
                "Code.exe"
            )
        ],

        "exe":"Code.exe"

    },

    "chrome":{

        "aliases":[
            "chrome",
            "google chrome"
        ],

        "paths":[
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],

        "exe":"chrome.exe"

    },

    "calculator":{

        "aliases":[
            "calculator",
            "calc"
        ],

        "command":"calc.exe"

    },

    "youtube":{

        "aliases":[
            "youtube"
        ],

        "url":"https://youtube.com"

    },

    "github":{

        "aliases":[
            "github"
        ],

        "url":"https://github.com"

    },

    "spotify":{

        "aliases":[
            "spotify"
        ],

        "exe":"Spotify.exe"

    }

}


import os
import shutil
import subprocess
import webbrowser
import pyautogui
import time

def open_app(name):

    app = apps.get(name)

    if not app:
        speak("Application not found.")
        return

    speak(f"Opening {name}")

    # Website
    if "url" in app:
        webbrowser.open(app["url"])
        return

    # Windows command
    if "command" in app:
        subprocess.Popen(app["command"], shell=True)
        return

    # Known install paths
    for path in app.get("paths", []):

        if os.path.exists(path):

            subprocess.Popen(path)

            return

    # Search PATH
    exe = shutil.which(app.get("exe", ""))

    if exe:

        subprocess.Popen(exe)

        return

    # Windows Search fallback
    pyautogui.press("win")
    time.sleep(.4)

    pyautogui.write(name)

    time.sleep(.5)

    pyautogui.press("enter")