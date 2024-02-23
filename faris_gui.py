import tkinter as tk
from tkinter import ttk  
import faris_cli
import threading
import subprocess

cli_process = None

def on_closing() -> None:
    global cli_process
    if cli_process and cli_process.poll() is None:
        cli_process.terminate()
    window.destroy() 

def run_cli() -> None:
    global cli_process
    cli_process = subprocess.Popen(["python3", "faris_cli.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cli_process.wait()
    window.quit()  

def send_input(input_text: str) -> None:
    global cli_process
    cli_process.stdin.write(input_text + '\n')
    cli_process.stdin.flush()

def button_click(option: str) -> None:
    send_input(option)

def set_option(option) -> None:
    selected_option.set(option)

def create_menu(menu: "dict[str, str]") -> None:
    width = max(len(value) for value in menu.values())
    for key, value in menu.items():
        button = tk.Button(text=value, command=lambda v=key: button_click(v), width=width, anchor="w", master=menu_frame)
        button.pack(anchor=tk.W)

def create_rotate_submenu(mode: int, menu: "dict[str, str]") -> None:
    mode_label = tk.Label(text=f"Selected option: {menu_frame.keys(mode)}", master=submenu_frame)
    mode_label.pack(anchor=tk.W)

window = tk.Tk()
window.title("Faris' Automated RotatIng Standa (FARIS) Motor")
window.minsize(400,300)

menu_frame = tk.Frame(master=window)
menu_frame.pack(side=tk.LEFT, padx=10,pady=10)

submenu_frame = tk.Frame(master=window)

cli_thread = threading.Thread(target=run_cli)
cli_thread.start()

label = ttk.Label(text="Select option", master=menu_frame)
label.pack(anchor=tk.W)

selected_option = tk.StringVar()

create_menu(faris_cli.menu_dict)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()