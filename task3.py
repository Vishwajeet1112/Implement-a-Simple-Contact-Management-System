import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("700x650")
        self.root.configure(bg="#f5f5f5")

        self.contacts = self.load_contacts()

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Contact Manager", font=('Arial', 16), bg="#f5f5f5").pack(pady=10)

        # Add Contact Frame
        frame_add = tk.Frame(self.root, bg="#f5f5f5")
        frame_add.pack(pady=10, padx=10, fill='x')

        tk.Label(frame_add, text="Name:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_add, text="Phone:", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_add, text="Email:", bg="#f5f5f5").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.entry_name = tk.Entry(frame_add, font=('Arial', 12))
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.entry_phone = tk.Entry(frame_add, font=('Arial', 12))
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        self.entry_email = tk.Entry(frame_add, font=('Arial', 12))
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        btn_add = tk.Button(frame_add, text="Add Contact", font=('Arial', 12), command=self.add_contact, bg="#0288d1", fg="white")
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Contact List Frame
        frame_list = tk.Frame(self.root, bg="#f5f5f5")
        frame_list.pack(pady=10, padx=10, fill='both', expand=True)

        self.contact_listbox = tk.Listbox(frame_list, font=('Arial', 12))
        self.contact_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side='right', fill='y')

        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_listbox.yview)

        self.contact_listbox.bind('<Double-1>', self.load_contact_to_edit)

        # Edit Contact Frame
        frame_edit = tk.Frame(self.root, bg="#f5f5f5")
        frame_edit.pack(pady=10, padx=10, fill='x')

        tk.Label(frame_edit, text="Name:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_edit, text="Phone:", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_edit, text="Email:", bg="#f5f5f5").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.edit_name = tk.Entry(frame_edit, font=('Arial', 12))
        self.edit_name.grid(row=0, column=1, padx=5, pady=5)

        self.edit_phone = tk.Entry(frame_edit, font=('Arial', 12))
        self.edit_phone.grid(row=1, column=1, padx=5, pady=5)

        self.edit_email = tk.Entry(frame_edit, font=('Arial', 12))
        self.edit_email.grid(row=2, column=1, padx=5, pady=5)

        btn_save = tk.Button(frame_edit, text="Save Changes", font=('Arial', 12), command=self.save_contact, bg="#0288d1", fg="white")
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)

        btn_delete = tk.Button(frame_edit, text="Delete Contact", font=('Arial', 12), command=self.delete_contact, bg="#d32f2f", fg="white")
        btn_delete.grid(row=4, column=0, columnspan=2, pady=10)

        self.update_contact_list()

    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if not name or not phone or not email:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        if name in self.contacts:
            messagebox.showerror("Duplicate Contact", "A contact with this name already exists.")
            return

        self.contacts[name] = {'phone': phone, 'email': email}
        self.save_contacts()
        self.update_contact_list()
        self.clear_add_fields()

    def clear_add_fields(self):
        self.entry_name.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.entry_email.delete(0, 'end')

    def update_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, contact)

    def load_contact_to_edit(self, event):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if selected_contact:
            contact = self.contacts[selected_contact]
            self.edit_name.delete(0, tk.END)
            self.edit_name.insert(0, selected_contact)
            self.edit_phone.delete(0, tk.END)
            self.edit_phone.insert(0, contact['phone'])
            self.edit_email.delete(0, tk.END)
            self.edit_email.insert(0, contact['email'])

    def save_contact(self):
        name = self.edit_name.get()
        phone = self.edit_phone.get()
        email = self.edit_email.get()

        if not name or not phone or not email:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        if name not in self.contacts:
            messagebox.showerror("Contact Not Found", "The contact does not exist.")
            return

        self.contacts[name] = {'phone': phone, 'email': email}
        self.save_contacts()
        self.update_contact_list()
        self.clear_edit_fields()

    def clear_edit_fields(self):
        self.edit_name.delete(0, 'end')
        self.edit_phone.delete(0, 'end')
        self.edit_email.delete(0, 'end')

    def delete_contact(self):
        name = self.edit_name.get()

        if name not in self.contacts:
            messagebox.showerror("Contact Not Found", "The contact does not exist.")
            return

        del self.contacts[name]
        self.save_contacts()
        self.update_contact_list()
        self.clear_edit_fields()

    def save_contacts(self):
        with open('contacts.json', 'w') as file:
            json.dump(self.contacts, file)

    def load_contacts(self):
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as file:
                return json.load(file)
        return {}

# Set up the GUI window
root = tk.Tk()
app = ContactManager(root)
root.mainloop()
