"""
Jarvis AI — Tkinter GUI
Feature 6: Full chat-style graphical interface.
Run with: python main.py --gui
Or set GUI_MODE = True in config/settings.py
"""

import sys
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime


class JarvisGUI:
    """
    Chat-style GUI for Jarvis AI.
    Runs the Jarvis loop in a background thread to keep UI responsive.
    """

    # ── Color palette ──────────────────────────────────────────
    BG          = "#0d1117"
    SIDEBAR_BG  = "#161b22"
    INPUT_BG    = "#1c2128"
    ACCENT      = "#00d4ff"
    ACCENT_DIM  = "#005f73"
    USER_BG     = "#1f3a5f"
    BOT_BG      = "#1a2332"
    TEXT_FG     = "#e6edf3"
    TEXT_DIM    = "#8b949e"
    SUCCESS     = "#3fb950"
    WARNING     = "#d29922"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JARVIS AI Shell")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.root.configure(bg=self.BG)
        self._configure_styles()
        self._build_ui()
        self._startup_message()

    # ── UI Construction ────────────────────────────────────────

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Accent.TButton",
                         background=self.ACCENT_DIM,
                         foreground=self.TEXT_FG,
                         font=("Consolas", 10, "bold"),
                         relief="flat",
                         padding=6)
        style.map("Accent.TButton",
                  background=[("active", self.ACCENT)])

    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────────
        topbar = tk.Frame(self.root, bg=self.SIDEBAR_BG, height=48)
        topbar.pack(fill=tk.X, side=tk.TOP)
        topbar.pack_propagate(False)

        logo = tk.Label(topbar, text="⚡ JARVIS AI",
                        bg=self.SIDEBAR_BG, fg=self.ACCENT,
                        font=("Consolas", 15, "bold"))
        logo.pack(side=tk.LEFT, padx=18, pady=10)

        self.status_label = tk.Label(topbar, text="● Online",
                                     bg=self.SIDEBAR_BG, fg=self.SUCCESS,
                                     font=("Consolas", 9))
        self.status_label.pack(side=tk.RIGHT, padx=18)

        # ── Main area ────────────────────────────────────────
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill=tk.BOTH, expand=True)

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(
            main,
            bg=self.BG, fg=self.TEXT_FG,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bd=0,
            padx=16, pady=10,
            selectbackground=self.ACCENT_DIM,
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Tag styles for different message types
        self.chat_area.tag_config("timestamp", foreground=self.TEXT_DIM,
                                  font=("Consolas", 8))
        self.chat_area.tag_config("user_label", foreground=self.ACCENT,
                                  font=("Consolas", 9, "bold"))
        self.chat_area.tag_config("user_msg", foreground=self.TEXT_FG,
                                  font=("Consolas", 10),
                                  lmargin1=20, lmargin2=20)
        self.chat_area.tag_config("bot_label", foreground=self.SUCCESS,
                                  font=("Consolas", 9, "bold"))
        self.chat_area.tag_config("bot_msg", foreground=self.TEXT_FG,
                                  font=("Consolas", 10),
                                  lmargin1=20, lmargin2=20)
        self.chat_area.tag_config("system_msg", foreground=self.WARNING,
                                  font=("Consolas", 9, "italic"),
                                  lmargin1=10, lmargin2=10)
        self.chat_area.tag_config("error_msg", foreground="#f85149",
                                  font=("Consolas", 9),
                                  lmargin1=10, lmargin2=10)
        self.chat_area.tag_config("separator", foreground=self.SIDEBAR_BG)

        # ── Input area ───────────────────────────────────────
        input_frame = tk.Frame(self.root, bg=self.INPUT_BG, height=60)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 0))
        input_frame.pack_propagate(False)

        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(
            input_frame,
            textvariable=self.input_var,
            bg=self.INPUT_BG, fg=self.TEXT_FG,
            insertbackground=self.ACCENT,
            font=("Consolas", 11),
            bd=0,
            relief=tk.FLAT,
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH,
                               expand=True, padx=(18, 6), pady=14)
        self.input_field.bind("<Return>", self._on_send)

        send_btn = ttk.Button(input_frame, text="Send ➤",
                              style="Accent.TButton",
                              command=self._on_send)
        send_btn.pack(side=tk.RIGHT, padx=(4, 8), pady=10)

        mic_btn = ttk.Button(input_frame, text="🎤",
                             style="Accent.TButton",
                             command=self._on_voice)
        mic_btn.pack(side=tk.RIGHT, padx=(0, 4), pady=10)

        clear_btn = ttk.Button(input_frame, text="🗑",
                               style="Accent.TButton",
                               command=self._clear_chat)
        clear_btn.pack(side=tk.RIGHT, padx=(0, 4), pady=10)

        self.input_field.focus()

    def _startup_message(self):
        self._append_system("Jarvis AI Shell initialized. Type a command below.")
        self._append_system("Try: 'check cpu', 'open chrome', 'search Python tutorials', or 'how much RAM do I have?'")

    # ── Message Display ────────────────────────────────────────

    def _append_user(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        self._write(f"[{ts}]  ", "timestamp")
        self._write("You\n", "user_label")
        self._write(f"{text}\n\n", "user_msg")
        self._scroll_bottom()

    def _append_jarvis(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        self._write(f"[{ts}]  ", "timestamp")
        self._write("Jarvis\n", "bot_label")
        self._write(f"{text}\n\n", "bot_msg")
        self._scroll_bottom()

    def _append_system(self, text: str):
        self._write(f"  ⚙ {text}\n", "system_msg")
        self._scroll_bottom()

    def _append_error(self, text: str):
        self._write(f"  ✘ {text}\n\n", "error_msg")
        self._scroll_bottom()

    def _write(self, text: str, tag: str):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text, tag)
        self.chat_area.config(state=tk.DISABLED)

    def _scroll_bottom(self):
        self.chat_area.see(tk.END)

    def _clear_chat(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self._startup_message()

    # ── Input Handlers ─────────────────────────────────────────

    def _on_send(self, event=None):
        text = self.input_var.get().strip()
        if not text:
            return
        self.input_var.set("")
        self._process_input(text)

    def _on_voice(self):
        self._append_system("Listening for voice input...")
        self._set_status("🎤 Listening...", self.WARNING)
        threading.Thread(target=self._voice_thread, daemon=True).start()

    def _voice_thread(self):
        try:
            from interface.speech_input import get_voice_input
            from config.settings import VOICE_ENGINE
            text = get_voice_input(timeout=5, engine=VOICE_ENGINE)
            if text:
                self.root.after(0, lambda: self._process_input(text))
            else:
                self.root.after(0, lambda: self._append_system("No speech detected. Try typing instead."))
        except Exception as e:
            self.root.after(0, lambda: self._append_error(f"Voice error: {e}"))
        finally:
            self.root.after(0, lambda: self._set_status("● Online", self.SUCCESS))

    def _process_input(self, text: str):
        """Handles a command (text or voice) — runs Jarvis in background thread."""
        if text.lower() in ("exit", "quit", "shutdown jarvis"):
            self._append_user(text)
            self._append_jarvis("Shutting down Jarvis. Goodbye.")
            self.root.after(1500, self.root.destroy)
            return

        self._append_user(text)
        self._set_status("⏳ Thinking...", self.WARNING)
        self.input_field.config(state=tk.DISABLED)
        threading.Thread(target=self._jarvis_thread, args=(text,), daemon=True).start()

    def _jarvis_thread(self, user_input: str):
        """Runs the Jarvis pipeline in a background thread."""
        try:
            from core.router import route_command
            from executor.command_executor import execute_command
            from permission.permission_manager import check_permission
            from core.memory import add_recent_command
            from config.settings import SAFE_MODE

            action_plan = route_command(user_input)

            if not action_plan:
                self.root.after(0, lambda: self._append_error("I could not understand that request."))
                return

            # Permission check (for critical intents)
            approved = check_permission(action_plan)
            if not approved:
                self.root.after(0, lambda: self._append_system("Action cancelled by permission check."))
                return

            result = execute_command(action_plan)
            add_recent_command(user_input)

            display = result or "Done."
            self.root.after(0, lambda: self._append_jarvis(display))

            # Also speak the result
            try:
                from interface.tts_output import speak
                threading.Thread(target=speak, args=(display,), daemon=True).start()
            except Exception:
                pass

        except Exception as e:
            self.root.after(0, lambda: self._append_error(f"Internal error: {e}"))

        finally:
            self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        self.input_field.config(state=tk.NORMAL)
        self.input_field.focus()
        self._set_status("● Online", self.SUCCESS)

    def _set_status(self, text: str, color: str):
        self.status_label.config(text=text, fg=color)


# -------------------------------------------------
# GUI Launch Entry Point
# -------------------------------------------------

def launch_gui():
    """Launches the Jarvis GUI window."""
    root = tk.Tk()
    root.resizable(True, True)
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    app = JarvisGUI(root)
    root.mainloop()
