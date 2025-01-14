import customtkinter as ctk
from tkinter import messagebox
import psycopg2

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Modern To-Do App")
root.geometry("400x500")


def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="tkinter_app",
            user="tkinter_app_owner",
            password="StEJAv6Lp4Kc",
            host="ep-icy-sunset-a5w4vk1z.us-east-2.aws.neon.tech",
            port="5432",
        )
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        exit()


def add_task():
    task = task_entry.get().strip()
    if task:
        try:
            cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
            conn.commit()
            task_entry.delete(0, ctk.END)
            refresh_task_list()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error adding task:\n{e}")
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")


def delete_task(task_id, task_frame):
    try:
        cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
        conn.commit()
        task_frame.destroy()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting task:\n{e}")


def complete_task(task_id, task_label):
    try:
        cursor.execute("UPDATE todos SET completed = TRUE WHERE id = %s", (task_id,))
        conn.commit()
        task_label.configure(text_color="#888")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error completing task:\n{e}")


def clear_all_tasks():
    try:
        cursor.execute("DELETE FROM todos")
        conn.commit()
        for widget in task_list_frame.winfo_children():
            widget.destroy()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error clearing tasks:\n{e}")


def refresh_task_list():
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    try:
        cursor.execute("SELECT id, task, completed FROM todos ORDER BY id ASC")
        tasks = cursor.fetchall()
        for task_id, task_text, completed in tasks:
            add_task_to_ui(task_id, task_text, completed)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching tasks:\n{e}")


def add_task_to_ui(task_id, task_text, completed=False):
    task_frame = ctk.CTkFrame(task_list_frame, fg_color="#333")
    task_frame.pack(fill="x", pady=5, padx=10)

    task_label = ctk.CTkLabel(
        task_frame,
        text=task_text,
        text_color="#fff" if not completed else "#888",
        font=("Arial", 14),
    )
    task_label.pack(side="left", padx=10, fill="x", expand=True)

    ctk.CTkButton(
        task_frame,
        text="Complete",
        fg_color="#4caf50",
        text_color="#fff",
        width=80,
        command=lambda: complete_task(task_id, task_label),
    ).pack(side="right", padx=5)

    ctk.CTkButton(
        task_frame,
        text="Delete",
        fg_color="#f44336",
        text_color="#fff",
        width=80,
        command=lambda: delete_task(task_id, task_frame),
    ).pack(side="right", padx=5)




header = ctk.CTkFrame(root)
header.pack(padx=5, pady=5, fill="x")


ctk.CTkButton(
    header, text="Add Task", fg_color="#4caf50", text_color="#fff", command=add_task
).pack(side="right", pady=5, padx=5)

task_entry = ctk.CTkEntry(header, placeholder_text="Enter a task", font=("Arial", 14))
task_entry.pack(fill="x", padx=5, pady=5)


task_list_frame = ctk.CTkScrollableFrame(root, fg_color="#222", width=380, height=300)
task_list_frame.pack(fill="both", expand=True, padx=10, pady=10)


ctk.CTkButton(
    root,
    text="Clear All",
    fg_color="#f44336",
    text_color="#fff",
    command=clear_all_tasks,
).pack(pady=10)


conn = connect_to_db()
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    task TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
""")
conn.commit()


refresh_task_list()

root.mainloop()


cursor.close()
conn.close()

