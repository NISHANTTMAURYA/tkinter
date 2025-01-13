import tkinter as tk

def on_click(event):
    # Shows coordinates where mouse was clicked
    label.config(text=f"Clicked at x={event.x}, y={event.y}")

def on_key(event):
    # Shows which key was pressed
    label.config(text=f"Key pressed: {event.char}")

def on_enter(event):
    # Changes background when mouse enters
    canvas.config(bg='yellow')
    label.config(text="Mouse entered the canvas")

def on_leave(event):
    # Changes background when mouse leaves
    canvas.config(bg='white')
    label.config(text="Mouse left the canvas")

def on_drag(event):
    # Draws on canvas when mouse is dragged
    x, y = event.x, event.y
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')
    label.config(text=f"Drawing at x={x}, y={y}")

# Create main window
root = tk.Tk()
root.title("Event Handling Demo")
root.geometry("400x500")

# Create a canvas for mouse events
canvas = tk.Canvas(root, width=300, height=300, bg='white')
canvas.pack(pady=20)

# Create a label to show event information
label = tk.Label(root, text="Events will be shown here", font=('Arial', 12))
label.pack(pady=10)

# Bind various events to the canvas
canvas.bind('<Button-1>', on_click)        # Left mouse click
canvas.bind('<Key>', on_key)               # Any key press
canvas.bind('<Enter>', on_enter)           # Mouse enters canvas
canvas.bind('<Leave>', on_leave)           # Mouse leaves canvas
canvas.bind('<B1-Motion>', on_drag)        # Mouse drag with left button

# Canvas needs focus to receive key events
canvas.focus_set()

root.mainloop()
