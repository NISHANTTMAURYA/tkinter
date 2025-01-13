import tkinter as tk
root = tk.Tk()
entry = tk.Entry(root, width=30)
def show_entry():
    label.config(text = f"Hello, {entry.get()}")
    submit_button.destroy()
    button.destroy()
    entry.destroy()
    btn = tk.Button(root,text = "Click to exit",command = close)
    btn.pack()
def close():
    root.destroy()
    
def on_click():
    try:
        global submit_button
        entry.pack()
        submit_button = tk.Button(root, text="Submit", command=show_entry)
        submit_button.pack()
        name = entry.get()
        label.config(text = f"Hello, {name}!")
    except:
        label.config(text = "Please enter a name")



root.title("hello")
root.geometry("400x300")
label = tk.Label(root,text = "NOTHING",font = ('Arial',16))
label.pack(side="top", fill="x")
button = tk.Button(root,text = "Click to enter name",command = on_click)
button.pack()



root.mainloop()
