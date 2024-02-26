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

cli_thread = threading.Thread(target=run_cli)
cli_thread.start()

window = tk.Tk()
window.title("Faris' Automated RotatIng Standa (FARIS) Motor")
window.minsize(400,300)

main_menu_frame = tk.Frame(master=window)

def main_menu_button_click(option: str) -> None:
    send_input(option)
    try:
        int(option)
    except:
        pass
    else:
        if int(option) >= 1 and int(option) <= 4:
            create_rotate_menu(mode=option, menu=faris_cli.menu_dict)
            show_rotate_menu()

def set_option(option) -> None:
    selected_option.set(option)

def create_main_menu(menu: "dict[str, str]") -> None:
    label = ttk.Label(text="Select option", master=main_menu_frame)
    label.pack(anchor=tk.W)

    width = max(len(value) for value in menu.values())
    for key, value in menu.items():
        button = tk.Button(text=value, command=lambda v=key: main_menu_button_click(v), width=width, anchor="w", master=main_menu_frame)
        button.pack(anchor=tk.W)

def show_main_menu():
    main_menu_frame.pack(side=tk.LEFT, padx=10,pady=10)
    rotate_menu_frame.forget()


def clear_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()

def rotate_menu_quit_click() -> None:
    send_input('q')
    show_main_menu()
    clear_frame(rotate_menu_frame)

def create_rotate_menu(mode: str, menu: "dict[str, str]") -> None:
    mode_label = tk.Label(text=f"Selected option: {menu.get(mode)}", master=rotate_menu_frame)
    mode_label.pack(anchor=tk.W)
    
    quit_button = tk.Button(text="Back", command=rotate_menu_quit_click, master=rotate_menu_frame)
    quit_button.pack(anchor=tk.W)

def show_rotate_menu():
    rotate_menu_frame.pack(side=tk.LEFT, padx=10,pady=10)
    main_menu_frame.forget()

rotate_menu_frame = tk.Frame(master=window)

show_main_menu()

selected_option = tk.StringVar()

create_main_menu(faris_cli.menu_dict)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()