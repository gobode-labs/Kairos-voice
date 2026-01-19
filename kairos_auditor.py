"""
Copyright 2026 Eduardo Morales | Gobode Labs
Licensed under the Apache License, Version 2.0
Project: Kairos - Auditory Inspection Module

LOGIC OVERVIEW:
This module utilizes a threaded Text-to-Speech (TTS) engine to perform 
auditory audits of system logs or forensic buffers. It is designed to 
operate within WSL2 using the WSLg PulseAudio bridge.

DEPENDENCIES:
- python3-tk (System level)
- libespeak-ng1 (System level)
- pyttsx3 (Venv level)
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import re
import threading
import os

class KairosReader:
    def __init__(self, root):
        """
        Constructor: Initializes the UI and the TTS Engine.
        Focuses on state stability by catching initialization errors early.
        """
        self.root = root
        self.root.title("Gobode Labs | Kairos Project - Audio Auditor")
        self.root.geometry("600x550")
        self.root.configure(bg="#121212") # Dark theme for visual audit focus

        # Initialize TTS Engine
        try:
            # We explicitly force the 'espeak' driver. On Linux/WSL, this is 
            # the most reliable driver for communicating with PulseAudio.
            self.engine = pyttsx3.init(driverName='espeak')
            
            # Ensure volume is at unity (1.0) for maximum forensic clarity.
            self.engine.setProperty('volume', 1.0) 
        except Exception as e:
            # Defensive Exit: If the engine fails, the process terminates 
            # to avoid entering an undefined hardware state.
            messagebox.showerror("Kernel Error", f"TTS Engine failed: {e}")
            self.root.destroy()

        self.ui_init()

    def ui_init(self):
        """
        Tactical UI Layout:
        Designed for high-contrast readability in terminal environments.
        """
        # Module Header
        tk.Label(self.root, text="KAIROS PROJECT: AUDIO AUDITOR", 
                 font=("Courier", 16, "bold"), bg="#121212", fg="#00FF00").pack(pady=15)

        # Forensic Input Buffer Label
        tk.Label(self.root, text="FORENSIC INPUT BUFFER:", bg="#121212", fg="#FFFFFF", 
                 font=("Consolas", 10)).pack()
        
        # ScrolledText: Allows for large log files to be pasted and reviewed.
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=12,
                                                   bg="#1E1E1E", fg="#FFFFFF", font=("Consolas", 10),
                                                   insertbackground="#00FF00")
        self.text_area.pack(padx=20, pady=5)

        # Audit Rate Control: WPM (Words Per Minute)
        # Allows the operator to speed up for scanning or slow down for deep analysis.
        tk.Label(self.root, text="AUDIT PLAYBACK RATE (WPM):", bg="#121212", fg="#FFFFFF",
                 font=("Consolas", 9)).pack(pady=(10, 0))
        self.rate_slider = tk.Scale(self.root, from_=100, to=400, orient=tk.HORIZONTAL, 
                                    length=300, bg="#121212", fg="#00FF00", 
                                    highlightthickness=0, troughcolor="#1E1E1E")
        self.rate_slider.set(200) # Default operational speed
        self.rate_slider.pack()

        # Action Trigger: Executes the auditory transformation.
        self.run_btn = tk.Button(self.root, text="EXECUTE AUDIT", command=self.run_audio,
                                 bg="#00FF00", fg="#000000", font=("Courier", 12, "bold"),
                                 activebackground="#008800", padx=20, pady=10)
        self.run_btn.pack(pady=25)

        # Forensic Status Bar
        self.status = tk.Label(self.root, text="SYSTEM READY", bg="#121212", fg="#555555", 
                               font=("Consolas", 8))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def sanitize(self, text):
        """
        DOCTRINE OF SELF-DEFENSE (Sanitization Layer):
        Uses Regular Expressions to strip out non-standard characters.
        This prevents 'Injection' style errors where the TTS engine might 
        interpret certain symbols as control commands.
        """
        return re.sub(r'[^\w\s\.,!?\-]', '', text)

    def run_audio(self):
        """
        Main Execution Logic:
        Extracts data from the buffer, applies sanitization, and 
        spawns a worker thread to handle the sound generation.
        """
        raw_text = self.text_area.get("1.0", tk.END).strip()
        
        # Pre-condition check: Prevent execution on empty buffers.
        if not raw_text:
            messagebox.showwarning("Logic Error", "Input buffer is empty.")
            return

        # Lock UI to prevent race conditions (multiple playback instances).
        self.run_btn.config(state=tk.DISABLED)
        self.status.config(text="AUDIT IN PROGRESS...", fg="#00FF00")

        def speak_task():
            """
            Threaded worker: Decouples the synthesis from the Main UI Thread.
            This prevents the window from 'Freezing' while speaking.
            """
            try:
                # Apply the mathematical transformation (Sanitize)
                clean_text = self.sanitize(raw_text)
                
                # Sync parameters
                self.engine.setProperty('rate', self.rate_slider.get())
                
                # Auditory Output
                self.engine.say(clean_text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Audit Exception: {e}")
            finally:
                # Return UI to 'Normal' state safely via the main thread.
                self.root.after(0, self.reset_ui)

        # Start the thread as a 'daemon' so it closes if the window is closed.
        threading.Thread(target=speak_task, daemon=True).start()

    def reset_ui(self):
        """
        Resets UI components to the 'Ready' state post-audit.
        """
        self.run_btn.config(state=tk.NORMAL)
        self.status.config(text="SYSTEM READY", fg="#555555")

if __name__ == "__main__":
    # Primary Application Entry Point
    root = tk.Tk()
    
    # Ensure the process dies correctly when the 'X' is clicked.
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    
    app = KairosReader(root)
    root.mainloop()
