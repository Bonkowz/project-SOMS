import tkinter as tk

class Utils:
    def __init__(self):
        pass

    def clear_widgets(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def add_hover_effect(self, widget, bg_normal, bg_hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))