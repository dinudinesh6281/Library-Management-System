import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# -----------------------------
# Database Setup
# -----------------------------
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    if title and author:
        cursor.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", (title, author, "Available"))
        conn.commit()
        messagebox.showinfo("Success", f"Book '{title}' added successfully.")
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        view_books()
    else:
        messagebox.showwarning("Input Error", "Please enter both title and author.")

def view_books():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    for book in books:
        tree.insert("", tk.END, values=book)

def borrow_book():
    selected = tree.selection()
    if selected:
        book_id = tree.item(selected[0])["values"][0]
        status = tree.item(selected[0])["values"][3]
        if status == "Available":
            cursor.execute("UPDATE books SET status=? WHERE id=?", ("Borrowed", book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book borrowed successfully!")
        else:
            messagebox.showwarning("Unavailable", "This book is already borrowed.")
        view_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book.")

def return_book():
    selected = tree.selection()
    if selected:
        book_id = tree.item(selected[0])["values"][0]
        status = tree.item(selected[0])["values"][3]
        if status == "Borrowed":
            cursor.execute("UPDATE books SET status=? WHERE id=?", ("Available", book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
        else:
            messagebox.showwarning("Error", "This book was not borrowed.")
        view_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book.")

def delete_book():
    selected = tree.selection()
    if selected:
        book_id = tree.item(selected[0])["values"][0]
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Book deleted successfully!")
        view_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book.")

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("📘 Library Management System")
root.geometry("700x500")
root.configure(bg="#f4f6f9")

# Title
tk.Label(root, text="Library Management System", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#007bff").pack(pady=10)

# Input Frame
frame_input = tk.Frame(root, bg="#f4f6f9")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Title:", font=("Arial", 12), bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_title = tk.Entry(frame_input, font=("Arial", 12), width=30)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Author:", font=("Arial", 12), bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_author = tk.Entry(frame_input, font=("Arial", 12), width=30)
entry_author.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Add Book", command=add_book, bg="#007bff", fg="white", font=("Arial", 12), width=12).grid(row=0, column=2, rowspan=2, padx=10)

# Book List
columns = ("ID", "Title", "Author", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=20)

# Buttons
frame_buttons = tk.Frame(root, bg="#f4f6f9")
frame_buttons.pack()

tk.Button(frame_buttons, text="Borrow", command=borrow_book, bg="#28a745", fg="white", font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Return", command=return_book, bg="#ffc107", fg="black", font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Delete", command=delete_book, bg="#dc3545", fg="white", font=("Arial", 12), width=12).grid(row=0, column=2, padx=10)

# Load initial data
view_books()

root.mainloop()
conn.close()
