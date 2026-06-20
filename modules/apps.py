import os
import webbrowser
from modules.voice import speak

apps = {

    # Coding / Dev
    "vscode": r"C:\Users\ADMIN\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vs code": r"C:\Users\ADMIN\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "pycharm": r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.2.2\bin\pycharm64.exe",
    "arduino": r"C:\Program Files (x86)\Arduino\arduino.exe",
    "CapCut": r"C:\Users\ADMIN\AppData\Local\CapCut\Apps\CapCut.exe",
    "Cap Cut": r"C:\Users\ADMIN\AppData\Local\CapCut\Apps\CapCut.exe",

    # Communication
    "discord": r"C:\Users\Adrish\AppData\Local\Discord\app-1.0.9001\Discord.exe",


    # Browsers / Research
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "youtube": "https://youtube.com",
    "chat gpt": "https://chatgpt.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "gitlab": "https://gitlab.com",
    "google": "https://google.com",

    # Entertainment
    "netflix": "https://netflix.com",
    "prime video": "https://primevideo.com",
    "spotify": "Spotify.exe",

    # Productivity / Notes
    "notion": r"C:\Users\Adrish\AppData\Local\Programs\Notion\Notion.exe",
    "obsidian": r"C:\Users\Adrish\AppData\Local\Programs\Obsidian\Obsidian.exe",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",

    # Utilities
    "calculator": r"C:\Windows\System32\calc.exe",
    "file explorer": r"C:\Windows\explorer.exe",
    "snipping tool": r"C:\Windows\System32\SnippingTool.exe",
    "paint": r"C:\Windows\System32\mspaint.exe"
}


def open_app(app_name):

    if app_name in apps:

        target = apps[app_name]

        speak(f"Opening {app_name}")

        try:

            if target.startswith("http"):

                webbrowser.open(target)

            elif "whatsapp" in target:
              
                os.system("start whatsapp:")

            else:

                os.startfile(target)

        except Exception as e:

            print("OPEN ERROR:", e)

            speak("Failed to open application.")

    else:

        speak("Application not found.")