import os
import math
import random
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from modules.voice import speak, listen
from modules.apps import open_app, apps
from modules.ai import ask_ai
from modules.visions import capture_screen
from modules.memory import init_db
from modules.memory import (
    add_memory,
    get_recent_memories
)
from modules.mouse_control import start
from modules.web_search import searchit
from modules.vision import FaceMonitor
from modules.file_controller import file_controller
load_dotenv()
face_monitor = FaceMonitor()

threading.Thread(
    target=face_monitor.start,
    daemon=True
).start()
init_db()

HUD_BG = "#020711"
HUD_PANEL = "#081525"
HUD_PANEL_ALT = "#0c1f32"
HUD_CYAN = "#32e6ff"
HUD_BLUE = "#2d7dff"
HUD_TEXT = "#d8fbff"
HUD_MUTED = "#74aebd"
HUD_GREEN = "#5cffb1"
HUD_WARN = "#ffd166"


def clear():

    os.system("cls")


clear()

print("""

========================================
               ATLAS AI
========================================
          Personal AI Assistant
========================================

""")


startup_lines = [

    "Atlas online.",
    "Welcome home sir."

]


OPEN_INTENT_WORDS = (
    "open",
    "launch",
    "start",
    "run",
    "load",
    "bring up",
    "pull up",
    "go to",
    "visit",
    "take me to",
)

AI_PREFIXES = (
    "atlas",
    "ask atlas",
    "ask ai",
    "ai",
    "assistant",
    "tell me",
    "explain",
    "what",
    "who",
    "where",
    "when",
    "why",
    "how",
    "say",
)


def normalize_command(command):

    return " ".join(command.lower().strip().split())


def remove_polite_words(command):

    polite_words = (
        "please",
        "can you",
        "could you",
        "would you",
        "will you",
        "atlas",
    )

    cleaned = command

    for word in polite_words:

        cleaned = cleaned.replace(word, " ")

    return normalize_command(cleaned)


def find_app_in_command(command):

    cleaned = remove_polite_words(command)

    for app_name in sorted(apps, key=len, reverse=True):

        if app_name in cleaned:

            return app_name

    for intent_word in OPEN_INTENT_WORDS:

        if cleaned.startswith(intent_word):

            possible_app = cleaned.replace(intent_word, "", 1).strip()

            if possible_app:

                return possible_app

    return ""


def is_open_intent(command):

    return any(word in command for word in OPEN_INTENT_WORDS)


def clean_ai_prompt(command):

    prompt = command

    for prefix in sorted(AI_PREFIXES, key=len, reverse=True):

        if prompt.startswith(prefix):

            prompt = prompt.replace(prefix, "", 1).strip()

            break

    return prompt or command


def handle_command(command):

    command = normalize_command(command)

    if command == "":

        return True, ""

    if command in ("exit", "quit", "shutdown", "shut down"):

        speak("Shutting down systems.")

        return False, "Shutting down systems."

    if command == "clear":

        clear()

        return True, ""
    if command.startswith("search"):
        
        parts = command.replace("search ", "", 1).split(" for ", 1)
        
        query = parts[0].strip()
        
        message = ""
        if len(parts) > 1:
            message = parts[1].strip()

        result = searchit(
            query
        )

        speak(result)

        return True, result


    
    if command.startswith("message "):
        from modules.whatsapp import send_whatsapp_message
        try:
            parts = command.replace("message ", "").split(" saying ")
            contact = parts[0].strip()
            message = parts[1].strip()
    
            result = send_whatsapp_message(
                contact,
                message
            )
    
            speak(result)
    
            return True, result

        except:
    
            speak(
                "Use format. Message contact saying your message."
            )
    
            return True, ""
    if command.startswith("create folder "):
    
        folder_name = command.replace(
            "create folder ",
            ""
        ).strip()
    
        result = file_controller({
            "action": "create_folder",
            "path": r"D:\Adrish\Projects",
            "name": folder_name
        })
    
        speak(result)
    
        return True, result
    if "camera control" in command:
        threading.Thread(
            target=start,
            daemon=True
        ).start()
    if command.startswith("create file "):
        file_name = command.replace(
            "create file ",
            ""
        ).strip()
    
        result = file_controller({
            "action": "create_file",
            "path": r"D:\Adrish\Projects",
            "name": file_name
        })
    
        speak(result)
    
        return True, result
    if command.startswith("plan "):
        from modules.planner import create_plan
        from modules.memory import get_recent_memories
    
        goal = command.replace("plan ", "")
        memory = get_recent_memories()
    
        plan = create_plan(goal, memory)
    if "screenshot" in command:
        file = capture_screen()
        print(f"Saved: {file}")
        speak("Screenshot captured")
        return True, f"Screenshot captured: {file}"
    if is_open_intent(command):

        app = find_app_in_command(command)

        if app:

            open_app(app)

            return True, f"Opening {app}."

    prompt = clean_ai_prompt(command)
    
    answer = ask_ai(prompt)
    
    return True, answer or ""


class AtlasHUD:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("ATLAS AI")
        self.root.geometry("1180x720")
        self.root.minsize(980, 640)
        self.root.configure(bg=HUD_BG)

        self.running = True
        self.listening = False
        self.processing = False
        self.angle = 0
        self.wave_phase = 0
        self.scan_y = 0
        self.particles = []
        self.nodes = []

        self.build_ui()
        self.seed_visuals()
        self.animate()

        self.root.after(
            400,
            lambda: self.run_background(
                lambda: speak(random.choice(startup_lines))
            )
        )

    def build_ui(self):

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.root,
            bg=HUD_BG,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.side = tk.Frame(
            self.root,
            bg=HUD_PANEL,
            width=330,
            highlightbackground="#12344c",
            highlightthickness=1
        )
        self.side.grid(row=0, column=1, sticky="ns")
        self.side.grid_propagate(False)

        self.title = tk.Label(
            self.side,
            text="ATLAS",
            fg=HUD_CYAN,
            bg=HUD_PANEL,
            font=("Segoe UI", 30, "bold")
        )
        self.title.pack(anchor="w", padx=24, pady=(24, 0))

        self.subtitle = tk.Label(
            self.side,
            text="Holographic Command Interface",
            fg=HUD_MUTED,
            bg=HUD_PANEL,
            font=("Segoe UI", 10)
        )
        self.subtitle.pack(anchor="w", padx=26, pady=(0, 22))

        self.status_rows = {}
        for label, value, color in (
            ("VOICE", "STANDBY", HUD_CYAN),
            ("GESTURE", "TRACKING", HUD_GREEN),
            ("EYE LINK", "CALIBRATED", HUD_BLUE),
            ("HAPTIC", "MICRO-PULSE", HUD_WARN),
        ):
            self.add_status(label, value, color)

        tk.Label(
            self.side,
            text="COMMAND STREAM",
            fg=HUD_CYAN,
            bg=HUD_PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=24, pady=(22, 6))

        self.log = scrolledtext.ScrolledText(
            self.side,
            height=13,
            bg="#04101d",
            fg=HUD_TEXT,
            insertbackground=HUD_CYAN,
            relief="flat",
            font=("Consolas", 9),
            wrap="word"
        )
        self.log.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.log.insert("end", "SYSTEM: Neural interface initialized.\n")
        self.log.configure(state="disabled")

        input_shell = tk.Frame(self.side, bg=HUD_PANEL)
        input_shell.pack(fill="x", padx=24, pady=(0, 18))

        self.command_entry = tk.Entry(
            input_shell,
            bg=HUD_PANEL_ALT,
            fg=HUD_TEXT,
            insertbackground=HUD_CYAN,
            relief="flat",
            font=("Segoe UI", 11)
        )
        self.command_entry.pack(side="left", fill="x", expand=True, ipady=9)
        self.command_entry.bind("<Return>", lambda event: self.submit_text())

        self.send_button = tk.Button(
            input_shell,
            text="SEND",
            command=self.submit_text,
            bg="#0e314a",
            fg=HUD_TEXT,
            activebackground="#155f86",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12
        )
        self.send_button.pack(side="left", padx=(8, 0), ipady=6)

        controls = tk.Frame(self.side, bg=HUD_PANEL)
        controls.pack(fill="x", padx=24, pady=(0, 24))

        self.voice_button = tk.Button(
            controls,
            text="VOICE",
            command=self.submit_voice,
            bg="#063f4e",
            fg=HUD_TEXT,
            activebackground="#0a7188",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        self.voice_button.pack(side="left", fill="x", expand=True, ipady=10)

        self.shutdown_button = tk.Button(
            controls,
            text="SHUTDOWN",
            command=self.shutdown,
            bg="#351728",
            fg="#ffd7e7",
            activebackground="#682646",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        self.shutdown_button.pack(side="left", fill="x", expand=True, padx=(8, 0), ipady=10)

    def add_status(self, label, value, color):

        row = tk.Frame(self.side, bg=HUD_PANEL_ALT)
        row.pack(fill="x", padx=24, pady=4)

        tk.Label(
            row,
            text=label,
            fg=HUD_MUTED,
            bg=HUD_PANEL_ALT,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=12, pady=10)

        value_label = tk.Label(
            row,
            text=value,
            fg=color,
            bg=HUD_PANEL_ALT,
            font=("Consolas", 9, "bold")
        )
        value_label.pack(side="right", padx=12, pady=10)
        self.status_rows[label] = value_label

    def seed_visuals(self):

        for _ in range(46):
            self.particles.append({
                "x": random.randint(10, 850),
                "y": random.randint(10, 680),
                "r": random.choice((1, 1, 2)),
                "speed": random.uniform(0.25, 1.1),
                "alpha": random.choice(("#0d6b85", "#159ec5", "#32e6ff"))
            })

        for _ in range(18):
            self.nodes.append({
                "x": random.randint(60, 820),
                "y": random.randint(70, 620),
                "dx": random.uniform(-0.35, 0.35),
                "dy": random.uniform(-0.35, 0.35)
            })

    def log_line(self, text):

        self.log.configure(state="normal")
        self.log.insert("end", f"{text}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def set_status(self, label, value):

        if label in self.status_rows:
            self.status_rows[label].configure(text=value)

    def submit_text(self):

        command = self.command_entry.get().strip()
        if not command:
            return

        self.command_entry.delete(0, "end")
        self.execute_command(command)

    def submit_voice(self):

        if self.listening:
            return

        self.listening = True
        self.set_status("VOICE", "LISTENING")
        self.voice_button.configure(text="LISTENING")
        self.log_line("VOICE: Listening for command...")

        def worker():
            command = listen()
            self.root.after(0, lambda: self.finish_voice(command))

        self.run_background(worker)

    def finish_voice(self, command):

        self.listening = False
        self.voice_button.configure(text="VOICE")
        self.set_status("VOICE", "STANDBY")

        if command:
            self.execute_command(command)
        else:
            self.log_line("VOICE: No command detected.")

    def execute_command(self, command):

        self.processing = True
        self.set_status("VOICE", "PROCESSING")
        self.log_line(f"YOU: {command}")

        def worker():
            keep_running, output = handle_command(command)
            self.root.after(0, lambda: self.finish_command(keep_running, output))

        self.run_background(worker)

    def finish_command(self, keep_running, output):

        self.processing = False
        self.set_status("VOICE", "STANDBY")

        if output:
            self.log_line(f"ATLAS: {output}")
        else:
            self.log_line("ATLAS: Command cycle complete.")

        if not keep_running:
            self.shutdown()

    def run_background(self, target):

        threading.Thread(target=target, daemon=True).start()

    def shutdown(self):

        self.running = False
        self.root.destroy()

    def animate(self):

        if not self.running:
            return

        width = self.canvas.winfo_width() or 850
        height = self.canvas.winfo_height() or 720
        cx = width * 0.48
        cy = height * 0.5
        radius = min(width, height) * 0.22

        self.canvas.delete("all")
        self.draw_background(width, height)
        self.draw_neural_network(width, height)
        self.draw_particles(width, height)
        self.draw_central_display(cx, cy, radius)
        self.draw_voice_waves(cx, cy, radius)
        self.draw_progress_rings(cx, cy, radius)
        self.draw_hud_labels(width, height)

        self.angle = (self.angle + 3) % 360
        self.wave_phase += 0.18
        self.scan_y = (self.scan_y + 2) % max(height, 1)
        self.root.after(33, self.animate)

    def draw_background(self, width, height):

        for i in range(0, height, 18):
            shade = 10 + int(16 * i / max(height, 1))
            color = f"#{2:02x}{shade:02x}{min(shade + 10, 42):02x}"
            self.canvas.create_rectangle(0, i, width, i + 18, fill=color, outline=color)

        self.canvas.create_line(
            0,
            self.scan_y,
            width,
            self.scan_y,
            fill="#063b54",
            width=1
        )

    def draw_neural_network(self, width, height):

        for node in self.nodes:
            node["x"] += node["dx"]
            node["y"] += node["dy"]
            if node["x"] < 20 or node["x"] > width - 20:
                node["dx"] *= -1
            if node["y"] < 20 or node["y"] > height - 20:
                node["dy"] *= -1

        for index, node in enumerate(self.nodes):
            for other in self.nodes[index + 1:]:
                distance = ((node["x"] - other["x"]) ** 2 + (node["y"] - other["y"]) ** 2) ** 0.5
                if distance < 165:
                    self.canvas.create_line(
                        node["x"],
                        node["y"],
                        other["x"],
                        other["y"],
                        fill="#0b5c78",
                        width=1
                    )

            self.canvas.create_oval(
                node["x"] - 3,
                node["y"] - 3,
                node["x"] + 3,
                node["y"] + 3,
                fill=HUD_CYAN,
                outline=""
            )

    def draw_particles(self, width, height):

        for particle in self.particles:
            particle["y"] -= particle["speed"]
            particle["x"] += random.uniform(-0.25, 0.25)
            if particle["y"] < -10:
                particle["y"] = height + 10
                particle["x"] = random.randint(0, max(int(width), 1))

            self.canvas.create_oval(
                particle["x"] - particle["r"],
                particle["y"] - particle["r"],
                particle["x"] + particle["r"],
                particle["y"] + particle["r"],
                fill=particle["alpha"],
                outline=""
            )

    def draw_central_display(self, cx, cy, radius):

        for offset, color in ((34, "#061727"), (22, "#08243a"), (10, "#0b314d")):
            self.canvas.create_oval(
                cx - radius - offset,
                cy - radius - offset,
                cx + radius + offset,
                cy + radius + offset,
                outline=color,
                width=2
            )

        self.canvas.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            fill="#06111e",
            outline=HUD_CYAN,
            width=2
        )

        self.canvas.create_arc(
            cx - radius - 18,
            cy - radius - 18,
            cx + radius + 18,
            cy + radius + 18,
            start=self.angle,
            extent=84,
            outline=HUD_CYAN,
            width=4,
            style="arc"
        )
        self.canvas.create_arc(
            cx - radius - 32,
            cy - radius - 32,
            cx + radius + 32,
            cy + radius + 32,
            start=-self.angle,
            extent=54,
            outline=HUD_BLUE,
            width=3,
            style="arc"
        )

        self.canvas.create_text(
            cx,
            cy - 24,
            text="ATLAS",
            fill=HUD_TEXT,
            font=("Segoe UI", 38, "bold")
        )
        self.canvas.create_text(
            cx,
            cy + 20,
            text="ONLINE" if not self.processing else "PROCESSING",
            fill=HUD_CYAN if not self.processing else HUD_WARN,
            font=("Consolas", 15, "bold")
        )
        self.canvas.create_text(
            cx,
            cy + 58,
            text="VOICE | GESTURE | EYE LINK | HAPTIC",
            fill=HUD_MUTED,
            font=("Consolas", 9)
        )

    def draw_voice_waves(self, cx, cy, radius):

        base_y = cy + radius + 88
        for index in range(31):
            x = cx - 210 + index * 14
            height = 12 + abs(random.random() * 5 + 30 * abs(math.sin(self.wave_phase + index * 0.38)))
            if not self.listening and not self.processing:
                height *= 0.35
            self.canvas.create_line(
                x,
                base_y - height,
                x,
                base_y + height,
                fill=HUD_CYAN,
                width=2
            )

        self.canvas.create_text(
            cx,
            base_y + 58,
            text="VOICE COMMAND VISUALIZATION",
            fill=HUD_MUTED,
            font=("Consolas", 10)
        )

    def draw_progress_rings(self, cx, cy, radius):

        ring_data = (
            ("TASK", 0.72, cx - radius - 150, cy - radius + 20),
            ("NEURAL", 0.86, cx + radius + 150, cy - radius + 20),
            ("POWER", 0.64, cx - radius - 150, cy + radius - 70),
            ("LINK", 0.93, cx + radius + 150, cy + radius - 70),
        )

        for label, progress, x, y in ring_data:
            self.canvas.create_oval(x - 42, y - 42, x + 42, y + 42, outline="#103149", width=7)
            self.canvas.create_arc(
                x - 42,
                y - 42,
                x + 42,
                y + 42,
                start=90,
                extent=-360 * progress,
                outline=HUD_CYAN,
                width=7,
                style="arc"
            )
            self.canvas.create_text(x, y - 4, text=f"{int(progress * 100)}%", fill=HUD_TEXT, font=("Consolas", 11, "bold"))
            self.canvas.create_text(x, y + 50, text=label, fill=HUD_MUTED, font=("Consolas", 9))

    def draw_hud_labels(self, width, height):

        streams = (
            (36, 44, "DATA STREAM 01"),
            (width - 190, 52, "RETINAL TRACK"),
            (42, height - 72, "GESTURE FIELD ACTIVE"),
        )

        for x, y, text in streams:
            self.canvas.create_text(x, y, text=text, fill=HUD_CYAN, font=("Consolas", 10, "bold"), anchor="w")
            self.canvas.create_line(x, y + 16, x + 146, y + 16, fill="#145a78", width=2)


if __name__ == "__main__":

    hud = AtlasHUD()
    hud.root.mainloop()
