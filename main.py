import sqlite3
import tkinter as tk
from tkinter import messagebox
def connect_db():
    return sqlite3.connect('university.db')

def add_student(id, name, age, major):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (id, name, age, major) VALUES (?, ?, ?, ?)", (id, name, age, major))
        conn.commit()
        return "Student added successfully."
    except sqlite3.IntegrityError:
        return "Student ID already exists."
    finally:
        conn.close()

def update_student(id, name, age, major):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE students SET name = ?, age = ?, major = ? WHERE id = ?", (name, age, major, id))
        if cursor.rowcount == 0:
            return "Student ID does not exist."
        else:
            conn.commit()
            return "Student updated successfully."
    finally:
        conn.close()

def retrieve_student(id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
        data = cursor.fetchone()
        if data:
            return {"id": data[0], "name": data[1], "age": data[2], "major": data[3]}
        else:
            return "Student ID does not exist."
    finally:
        conn.close()


def add_student_ui():
    response = add_student(
        id_entry.get(),
        name_entry.get(),
        age_entry.get(),
        major_entry.get()
    )
    messagebox.showinfo("Add Student", response)
    clear_entries()

def update_student_ui():
    response = update_student(
        id_entry.get(),
        name_entry.get(),
        age_entry.get(),
        major_entry.get()
    )
    messagebox.showinfo("Update Student", response)
    clear_entries()

def retrieve_student_ui():
    student_id = id_entry.get()
    student_info = retrieve_student(student_id)


    info_text.delete("1.0", tk.END)

    if isinstance(student_info, dict):

        info = f"ID: {student_info['id']}\nName: {student_info['name']}\nAge: {student_info['age']}\nMajor: {student_info['major']}"
        info_text.insert(tk.INSERT, info)
    else:
        messagebox.showerror("Error", student_info)

def clear_entries():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    major_entry.delete(0, tk.END)

root = tk.Tk()
root.title("University System")


tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1)

tk.Label(root, text="Major").grid(row=3, column=0)
major_entry = tk.Entry(root)
major_entry.grid(row=3, column=1)

add_button = tk.Button(root, text="Add Student", command=add_student_ui)
add_button.grid(row=4, column=0)

update_button = tk.Button(root, text="Update Student", command=update_student_ui)
update_button.grid(row=4, column=1)

info_text = tk.Text(root, height=4, width=50)
info_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

retrieve_button = tk.Button(root, text="Retrieve Student", command=retrieve_student_ui)
retrieve_button.grid(row=4, column=2)

clear_button = tk.Button(root, text="Clear Fields", command=clear_entries)
clear_button.grid(row=5, column=1)

root.mainloop()