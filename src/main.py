import tkinter as tk
from tkinter.filedialog import askopenfilename
from Globals import Globals
from Utilities import get_resource_path
from ConfigManager import ConfigManager
from Routines import autodisconnect
import pygame
import threading
import webbrowser

# Load configuration
config = ConfigManager.load()
scan_thread = None
stop_event = threading.Event()

def toggle_scan():
    global scan_thread
    print(f"[DEBUG] toggle_scan called. Globals.scan_running: {Globals.scan_running}, Globals.alarm_active: {Globals.alarm_active}")
    if Globals.alarm_active or Globals.scan_running:
        Globals.alarm_active = False
        Globals.scan_running = False
        pygame.mixer.music.stop()
        stop_event.set()
        if scan_thread is not None:
            scan_thread.join()
            scan_thread = None
        toggle_button.config(text="Start Scan")
        print("[DEBUG] Alarm and scan stopped by user.")
    else:
        print("[DEBUG] Starting scan.")
        Globals.scan_running = True
        Globals.alarm_active = False
        stop_event.clear()
        scan_thread = threading.Thread(target=autodisconnect, args=(mp3_path.get(), int(delay_entry.get()), stop_event, scan_disconnect.get(), scan_death.get(), scan_ingame.get()))
        scan_thread.start()
        toggle_button.config(text="Stop Scan")
        print("[DEBUG] Scan started.")

def select_mp3_file():
    filename = askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if filename:
        mp3_path.delete(0, tk.END)
        mp3_path.insert(0, filename)
        config["AudioFilePath"] = filename
        ConfigManager.save(config)

def on_closing():
    global scan_thread
    print("[DEBUG] on_closing called.")
    Globals.scan_running = False
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    config["deathDelay"] = int(delay_entry.get())
    config["scanForDisconnect"] = scan_disconnect.get()
    config["scanForDeath"] = scan_death.get()
    config["scanForIngame"] = scan_ingame.get()
    ConfigManager.save(config)
    if scan_thread is not None:
        stop_event.set()
        scan_thread.join()
    app.destroy()

def open_kofi_link(event):
    webbrowser.open_new("https://ko-fi.com/evolex")

app = tk.Tk()
app.title("Sailor Sleep")

# Set the window icon
icon_path = get_resource_path("images/title.ico")
app.iconbitmap(icon_path)

# Frame for MP3 file selection
mp3_frame = tk.Frame(app)
mp3_frame.pack(pady=10)

select_button = tk.Button(mp3_frame, text="Select MP3 File", command=select_mp3_file)
select_button.pack(side=tk.LEFT, padx=5)

mp3_path = tk.Entry(mp3_frame, width=50)
mp3_path.pack(side=tk.LEFT, padx=5)
mp3_path.insert(0, config["AudioFilePath"])

# Checkboxes for scan options
scan_disconnect = tk.BooleanVar(value=config["scanForDisconnect"])
scan_death = tk.BooleanVar(value=config["scanForDeath"])
scan_ingame = tk.BooleanVar(value=config["scanForIngame"])

checkbox_frame = tk.Frame(app)
checkbox_frame.pack(pady=10)

disconnect_checkbox = tk.Checkbutton(checkbox_frame, text="Scan for Disconnect", variable=scan_disconnect)
disconnect_checkbox.pack(side=tk.LEFT, padx=5)

death_checkbox = tk.Checkbutton(checkbox_frame, text="Scan for Death", variable=scan_death)
death_checkbox.pack(side=tk.LEFT, padx=5)

ingame_checkbox = tk.Checkbutton(checkbox_frame, text="Scan for Crash", variable=scan_ingame)
ingame_checkbox.pack(side=tk.LEFT, padx=5)

# Frame for death delay alert
delay_frame = tk.Frame(app)
delay_frame.pack(pady=10)

delay_label = tk.Label(delay_frame, text="Alert after being dead for (seconds):")
delay_label.pack(side=tk.LEFT, padx=5)

delay_entry = tk.Entry(delay_frame, width=10)
delay_entry.pack(side=tk.LEFT, padx=5)
delay_entry.insert(0, config["deathDelay"])

# Instructions
instructions = (
    "1. Keep your game on your MAIN screen, else this might not work.\n"
    "2. Make sure the sro_client is fully shown or else 'Crash' alert might trigger."
)
instructions_label = tk.Label(app, text=instructions, justify=tk.LEFT, padx=10, pady=10)
instructions_label.pack()

toggle_button = tk.Button(app, text="Start Scan", command=toggle_scan)
toggle_button.pack(pady=20)

# Signature frame
signature_frame = tk.Frame(app)
signature_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

signature_label = tk.Label(signature_frame, text="Made by Evolex", fg="blue", cursor="hand2")
signature_label.pack(side=tk.RIGHT, padx=5)
signature_label.bind("<Button-1>", open_kofi_link)

app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()