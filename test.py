import tkinter as tk

# Function to set the option variable to the selected value
def set_option(option):
    selected_option.set(option)

# Dictionary representing the menu
menu = {
    'a': 'Option A',
    'b': 'Option B',
    'c': 'Option C'
}

# Create tkinter window
root = tk.Tk()
root.title("Menu")

# Option variable to store the selected value
selected_option = tk.StringVar()

# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Determine the width of the widest button
max_button_width = max(len(value) for value in menu.values())

# Loop through the menu dictionary and create buttons
for key, value in menu.items():
    button = tk.Button(button_frame, text=value, command=lambda v=value: set_option(v), width=max_button_width, anchor="w")
    button.pack(anchor=tk.W)

# Label to display the selected option
selected_label = tk.Label(root, textvariable=selected_option)
selected_label.pack()

root.mainloop()

