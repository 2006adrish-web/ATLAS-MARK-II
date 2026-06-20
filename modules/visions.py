import mss
from PIL import Image
from datetime import datetime
import pygetwindow as gw
import os
import re


def get_active_window():

    try:

        window = gw.getActiveWindow()

        if window:

            return window.title

        return "unknown"

    except:

        return "unknown"


def clean_filename(text):

    text = re.sub(
        r'[<>:"/\\|?*]',
        '',
        text
    )

    text = text.strip()

    text = text.replace(" ", "_")

    return text[:40]


def capture_screen(context="general"):

    os.makedirs(
        "images",
        exist_ok=True
    )

    active_window = clean_filename(
        get_active_window()
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"images/"
        f"{context}_"
        f"{active_window}_"
        f"{timestamp}.png"
    )

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(
            monitor
        )

        img = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        img.save(filename)

    return filename