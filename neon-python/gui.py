import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection details
DATABASE_CONFIG = {
    "host": "ep-icy-sunset-a5w4vk1z.us-east-2.aws.neon.tech",
    "database": "tkinter_app",
    "user": "tkinter_app_owner",
    "password": "StEJAv6Lp4Kc",
    "sslmode": "require"
}

# Function to get a database connection
def get_database_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        print(conn)
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to the database: {e}")
        return None

# Function to fetch all users from the database
def fetch_data():
    conn = get_database_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users;")  # Query to fetch all users
        rows = cursor.fetchall()
        
        # Clear the Listbox
        listbox.delete(0, tk.END)
        
        # Insert data into the Listbox
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to add a new user to the database
def add_user():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    age = age_entry.get().strip()
    
    if not name or not email or not age:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be a number!")
        return

    conn = get_database_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Insert user into the database
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s);",
            (name, email, age)
        )
        conn.commit()
        messagebox.showinfo("Success", "User added successfully!")
        
        # Clear input fields
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        
        # Refresh the listbox
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add user: {e}")
    finally:
        cursor.close()
        conn.close()

# Tkinter application setup
root = tk.Tk()
root.title("User Management")
root.geometry("500x400")

# Input fields for adding a user
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack(pady=5)

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

tk.Label(root, text="Age:").pack(pady=5)
age_entry = tk.Entry(root, width=40)
age_entry.pack(pady=5)

# Button to add a user
add_button = tk.Button(root, text="Add User", activebackground="lightblue", activeforeground="red", command=add_user)
add_button.pack(pady=10)

# Fetch Data Button
fetch_button = tk.Button(root, text="Show All Users", activebackground="lightblue", activeforeground="red", command=fetch_data)
fetch_button.pack(pady=10)

# Listbox to display the users
listbox = tk.Listbox(root, width=70, height=15)
listbox.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
