import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext
def connect_db():
    return sqlite3.connect('university.db')

def add_student(student_id, name, age, major):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (student_id, name, age, major) VALUES (?, ?, ?, ?)", (student_id, name, age, major))
        conn.commit()
        return "Student added successfully."
    except sqlite3.IntegrityError:
        return "Student ID already exists."
    finally:
        conn.close()

def update_student(student_id, name, age, major):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE students SET name = ?, age = ?, major = ? WHERE student_id = ?", (name, age, major, student_id))
        if cursor.rowcount == 0:
            return "Student student_id does not exist."
        else:
            conn.commit()
            return "Student updated successfully."
    finally:
        conn.close()

def retrieve_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        data = cursor.fetchone()
        if data:
            return {"student_id": data[0], "name": data[1], "age": data[2], "major": data[3]}
        else:
            return "Student student_id does not exist."
    finally:
        conn.close()

def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id, name, age, major FROM students")
        return cursor.fetchall()  
    finally:
        conn.close()


def add_student_ui():
    response = add_student(
        student_id_entry.get(),
        name_entry.get(),
        age_entry.get(),
        major_entry.get()
    )
    messagebox.showinfo("Add Student", response)
    clear_entries()

def update_student_ui():
    response = update_student(
        student_id_entry.get(),
        name_entry.get(),
        age_entry.get(),
        major_entry.get()
    )
    messagebox.showinfo("Update Student", response)
    clear_entries()

def retrieve_student_ui():
    student_id = student_id_entry.get()
    student_info = retrieve_student(student_id)


    info_text.delete("1.0", tk.END)

    if isinstance(student_info, dict):

        info = f"ID: {student_info['student_id']}\nName: {student_info['name']}\nAge: {student_info['age']}\nMajor: {student_info['major']}"
        info_text.insert(tk.INSERT, info)
    else:
        messagebox.showerror("Error", student_info)

def clear_entries():

    student_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    major_entry.delete(0, tk.END)
    
def display_all_students_ui():
   
    students_info = get_all_students()
    info_text.delete("1.0", tk.END) 
    if students_info:
        for student in students_info:
            info = f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Major: {student[3]}\n"
            info_text.insert(tk.INSERT, info)
    else:
        messagebox.showinfo("Retrieve Students", "No student records found.")
        
root = tk.Tk()
root.title("University System")

tk.Label(root, text="ID").grid(row=0, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=0, column=1)

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

info_text = scrolledtext.ScrolledText(root, height=10, width=50)
info_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

retrieve_button = tk.Button(root, text="Retrieve Student", command=retrieve_student_ui)
retrieve_button.grid(row=4, column=2)

clear_button = tk.Button(root, text="Clear Fields", command=clear_entries)
clear_button.grid(row=5, column=1)

show_all_button = tk.Button(root, text="Show All Students", command=display_all_students_ui)
show_all_button.grid(row=5, column=2)

root.mainloop()