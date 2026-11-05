
import tkinter as tk

from tkinter import ttk, messagebox

import requests

from datetime import date

API_URL = "http://localhost/powell_gym/api.php"

root = tk.Tk()

root.title("POWELL POWER WELLNESS GYM")

root.geometry("1100x650")

root.configure(bg="#f2f2f2")

# -------------------- LOGIN SYSTEM --------------------

LOGIN_USERNAME = "admin"

LOGIN_PASSWORD = "admin123"

login_window = None

def show_login():

    global login_window

    root.withdraw()

    login_window = tk.Toplevel(root)

    login_window.title("POWELL POWER WELLNESS GYM - LOGIN")

    login_window.geometry("480x480")

    login_window.configure(bg="#222222")

    login_window.resizable(False, False)

    login_box = tk.Frame(

        login_window,

        bg="white",

        padx=40,

        pady=30

    )

    login_box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(

        login_box,

        text="POWELL POWER",

        font=("Arial", 23, "bold"),

        bg="white",

        fg="#222222"

    ).pack()

    tk.Label(

        login_box,

        text="WELLNESS GYM",

        font=("Arial", 14, "bold"),

        bg="white",

        fg="#198754"

    ).pack(pady=3)

    tk.Label(

        login_box,

        text="ADMINISTRATOR LOGIN",

        font=("Arial", 11, "bold"),

        bg="white",

        fg="#555555"

    ).pack(pady=18)

    tk.Label(

        login_box,

        text="Username",

        bg="white",

        font=("Arial", 10, "bold")

    ).pack(anchor="w")

    username_entry = tk.Entry(

        login_box,

        font=("Arial", 12),

        width=30

    )

    username_entry.pack(pady=(5, 12), ipady=5)

    tk.Label(

        login_box,

        text="Password",

        bg="white",

        font=("Arial", 10, "bold")

    ).pack(anchor="w")

    password_row = tk.Frame(login_box, bg="white")

    password_row.pack(pady=(5, 12))

    password_entry = tk.Entry(

        password_row,

        font=("Arial", 12),

        width=22,

        show="*"

    )

    password_entry.pack(side="left", ipady=5)

    def toggle_password():

        if password_entry.cget("show") == "*":

            password_entry.config(show="")

            show_button.config(text="Hide")

        else:

            password_entry.config(show="*")

            show_button.config(text="Show")

    show_button = tk.Button(

        password_row,

        text="Show",

        width=6,

        command=toggle_password

    )

    show_button.pack(side="left", padx=5)

    def attempt_login():

        username = username_entry.get().strip()

        password = password_entry.get()

        if not username or not password:

            messagebox.showwarning(

                "Login Validation",

                "Please enter username and password.",

                parent=login_window

            )

            return

        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:

            login_window.destroy()

            root.deiconify()

            load_members()

        else:

            messagebox.showerror(

                "Login Failed",

                "Incorrect username or password.",

                parent=login_window

            )

    tk.Button(

        login_box,

        text="LOGIN",

        font=("Arial", 12, "bold"),

        bg="#198754",

        fg="white",

        width=27,

        pady=8,

        command=attempt_login

    ).pack(pady=12)

    tk.Label(

        login_box,

        text="Authorized Personnel Only",

        font=("Arial", 9),

        fg="gray",

        bg="white"

    ).pack()

    login_window.protocol(

        "WM_DELETE_WINDOW",

        root.destroy

    )

    login_window.bind(

        "<Return>",

        lambda event: attempt_login()

    )

    username_entry.focus_set()

def logout():

    if messagebox.askyesno(

        "Logout",

        "Are you sure you want to logout?"

    ):

        clear_fields()

        search_var.set("")

        show_login()

# -------------------- FUNCTIONS --------------------

def clear_fields():

    member_id_var.set("")

    name_var.set("")

    age_var.set("")

    gender_var.set("Male")

    contact_var.set("")

    address_var.set("")

    membership_var.set("Monthly")

    start_var.set("")

    expiration_var.set("")

def validate_data():

    name = name_var.get().strip()

    age = age_var.get().strip()

    gender = gender_var.get()

    contact = contact_var.get().strip()

    address = address_var.get().strip()

    membership = membership_var.get()

    start = start_var.get().strip()

    expiration = expiration_var.get().strip()

    if not all([

        name, age, gender, contact,

        address, membership, start, expiration

    ]):

        messagebox.showwarning(

            "Validation",

            "Please complete all fields."

        )

        return False

    if not all(

        char.isalpha() or char in " .'-"

        for char in name

    ):

        messagebox.showwarning(

            "Validation",

            "Enter a valid full name."

        )

        return False

    try:

        age_number = int(age)

    except ValueError:

        messagebox.showwarning(

            "Validation",

            "Age must be a number."

        )

        return False

    if age_number < 1 or age_number > 120:

        messagebox.showwarning(

            "Validation",

            "Age must be from 1 to 120."

        )

        return False

    if gender not in ["Male", "Female", "Other"]:

        messagebox.showwarning(

            "Validation",

            "Select a valid gender."

        )

        return False

    if not (

        contact.startswith("09")

        and len(contact) == 11

        and contact.isdigit()

    ) and not (

        contact.startswith("+639")

        and len(contact) == 13

        and contact[1:].isdigit()

    ):

        messagebox.showwarning(

            "Validation",

            "Contact must be 09XXXXXXXXX or +639XXXXXXXXX."

        )

        return False

    if len(address) > 255:

        messagebox.showwarning(

            "Validation",

            "Address is too long."

        )

        return False

    try:

        start_date = date.fromisoformat(start)

        expiration_date = date.fromisoformat(expiration)

    except ValueError:

        messagebox.showwarning(

            "Validation",

            "Use YYYY-MM-DD for both dates."

        )

        return False

    if expiration_date < start_date:

        messagebox.showwarning(

            "Validation",

            "Expiration date cannot be before start date."

        )

        return False

    return True

def get_member_data():

    return {

        "full_name": name_var.get().strip(),

        "age": age_var.get().strip(),

        "gender": gender_var.get(),

        "contact_number": contact_var.get().strip(),

        "address": address_var.get().strip(),

        "membership_type": membership_var.get(),

        "start_date": start_var.get().strip(),

        "expiration_date": expiration_var.get().strip()

    }

def load_members():

    for item in member_table.get_children():

        member_table.delete(item)

    try:

        response = requests.get(API_URL, timeout=10)

        response.raise_for_status()

        result = response.json()

        if not result.get("success"):

            messagebox.showerror(

                "API Error",

                result.get("message", "Unable to load records.")

            )

            return

        members = result.get("members", [])

        for member in members:

            member_table.insert(

                "",

                "end",

                values=(

                    member["member_id"],

                    member["full_name"],

                    member["age"],

                    member["gender"],

                    member["contact_number"],

                    member["address"],

                    member["membership_type"],

                    member["start_date"],

                    member["expiration_date"]

                )

            )

        total_label.config(

            text="Total Members: " + str(len(members))

        )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(

            "Connection Error",

            str(error)

        )

    except ValueError:

        messagebox.showerror(

            "API Error",

            "The API did not return valid JSON."

        )

def add_member():

    if not validate_data():

        return

    try:

        response = requests.post(

            API_URL,

            json=get_member_data(),

            timeout=10

        )

        result = response.json()

        if response.ok and result.get("success"):

            messagebox.showinfo(

                "Success",

                "Member added successfully."

            )

            clear_fields()

            load_members()

        else:

            messagebox.showerror(

                "Error",

                result.get("message", "Unable to add member.")

            )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(

            "Connection Error",

            str(error)

        )

    except ValueError:

        messagebox.showerror(

            "API Error",

            "Invalid API response."

        )

def update_member():

    member_id = member_id_var.get().strip()

    if not member_id:

        messagebox.showwarning(

            "Validation",

            "Select a member first."

        )

        return

    if not validate_data():

        return

    try:

        response = requests.put(

            API_URL + "?id=" + member_id,

            json=get_member_data(),

            timeout=10

        )

        result = response.json()

        if response.ok and result.get("success"):

            messagebox.showinfo(

                "Success",

                "Member updated successfully."

            )

            clear_fields()

            load_members()

        else:

            messagebox.showerror(

                "Error",

                result.get("message", "Unable to update member.")

            )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(

            "Connection Error",

            str(error)

        )

    except ValueError:

        messagebox.showerror(

            "API Error",

            "Invalid API response."

        )

def delete_member():

    member_id = member_id_var.get().strip()

    if not member_id:

        messagebox.showwarning(

            "Validation",

            "Select a member first."

        )

        return

    confirm = messagebox.askyesno(

        "Confirm Delete",

        "Are you sure you want to delete this member?"

    )

    if not confirm:

        return

    try:

        response = requests.delete(

            API_URL + "?id=" + member_id,

            timeout=10

        )

        result = response.json()

        if response.ok and result.get("success"):

            messagebox.showinfo(

                "Success",

                "Member deleted successfully."

            )

            clear_fields()

            load_members()

        else:

            messagebox.showerror(

                "Error",

                result.get("message", "Unable to delete member.")

            )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(

            "Connection Error",

            str(error)

        )

    except ValueError:

        messagebox.showerror(

            "API Error",

            "Invalid API response."

        )

def search_member():

    keyword = search_var.get().strip()

    if not keyword:

        load_members()

        return

    for item in member_table.get_children():

        member_table.delete(item)

    try:

        response = requests.get(

            API_URL,

            params={"search": keyword},

            timeout=10

        )

        response.raise_for_status()

        result = response.json()

        if not result.get("success"):

            messagebox.showerror(

                "Error",

                result.get("message", "Search failed.")

            )

            return

        members = result.get("members", [])

        for member in members:

            member_table.insert(

                "",

                "end",

                values=(

                    member["member_id"],

                    member["full_name"],

                    member["age"],

                    member["gender"],

                    member["contact_number"],

                    member["address"],

                    member["membership_type"],

                    member["start_date"],

                    member["expiration_date"]

                )

            )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(

            "Connection Error",

            str(error)

        )

    except ValueError:

        messagebox.showerror(

            "API Error",

            "Invalid API response."

        )

def select_member(event):

    selected = member_table.selection()

    if not selected:

        return

    values = member_table.item(

        selected[0],

        "values"

    )

    member_id_var.set(values[0])

    name_var.set(values[1])

    age_var.set(values[2])

    gender_var.set(values[3])

    contact_var.set(values[4])

    address_var.set(values[5])

    membership_var.set(values[6])

    start_var.set(values[7])

    expiration_var.set(values[8])

# -------------------- VARIABLES --------------------

member_id_var = tk.StringVar()

name_var = tk.StringVar()

age_var = tk.StringVar()

gender_var = tk.StringVar(value="Male")

contact_var = tk.StringVar()

address_var = tk.StringVar()

membership_var = tk.StringVar(value="Monthly")

start_var = tk.StringVar()

expiration_var = tk.StringVar()

search_var = tk.StringVar()

# -------------------- TITLE --------------------

title = tk.Label(

    root,

    text="POWELL POWER WELLNESS GYM",

    font=("Arial", 22, "bold"),

    bg="#222222",

    fg="white",

    pady=15

)

title.pack(fill="x")

tk.Button(

    root,

    text="LOGOUT",

    font=("Arial", 9, "bold"),

    bg="#dc3545",

    fg="white",

    command=logout

).pack(anchor="e", padx=15, pady=(5, 0))

subtitle = tk.Label(

    root,

    text="MEMBERSHIP RECORD MANAGEMENT SYSTEM",

    font=("Arial", 12, "bold"),

    bg="#f2f2f2"

)

subtitle.pack(pady=10)

# -------------------- FORM --------------------

form = tk.LabelFrame(

    root,

    text="Member Information",

    font=("Arial", 11, "bold"),

    bg="#f2f2f2",

    padx=10,

    pady=10

)

form.pack(fill="x", padx=15, pady=5)

def add_field(label, variable, row, column, width=25):

    tk.Label(

        form,

        text=label,

        bg="#f2f2f2"

    ).grid(

        row=row,

        column=column,

        sticky="w",

        padx=5,

        pady=5

    )

    entry = tk.Entry(

        form,

        textvariable=variable,

        width=width

    )

    entry.grid(

        row=row,

        column=column + 1,

        padx=5,

        pady=5

    )

    return entry

add_field("Member ID:", member_id_var, 0, 0)

add_field("Full Name:", name_var, 0, 2)

add_field("Age:", age_var, 0, 4)

tk.Label(

    form,

    text="Gender:",

    bg="#f2f2f2"

).grid(

    row=1,

    column=0,

    sticky="w",

    padx=5,

    pady=5

)

ttk.Combobox(

    form,

    textvariable=gender_var,

    values=["Male", "Female", "Other"],

    state="readonly",

    width=22

).grid(

    row=1,

    column=1,

    padx=5,

    pady=5

)

add_field("Contact Number:", contact_var, 1, 2)

add_field("Address:", address_var, 1, 4)

tk.Label(

    form,

    text="Membership Type:",

    bg="#f2f2f2"

).grid(

    row=2,

    column=0,

    sticky="w",

    padx=5,

    pady=5

)

ttk.Combobox(

    form,

    textvariable=membership_var,

    values=[

        "Daily",

        "Weekly",

        "Monthly",

        "Quarterly",

        "Yearly"

    ],

    state="readonly",

    width=22

).grid(

    row=2,

    column=1,

    padx=5,

    pady=5

)

add_field("Start Date (YYYY-MM-DD):", start_var, 2, 2)

add_field("Expiration Date (YYYY-MM-DD):", expiration_var, 2, 4)

# -------------------- BUTTONS --------------------

button_frame = tk.Frame(

    root,

    bg="#f2f2f2"

)

button_frame.pack(pady=10)

tk.Button(

    button_frame,

    text="ADD MEMBER",

    width=15,

    bg="#198754",

    fg="white",

    command=add_member

).grid(row=0, column=0, padx=5)

tk.Button(

    button_frame,

    text="UPDATE",

    width=15,

    bg="#0d6efd",

    fg="white",

    command=update_member

).grid(row=0, column=1, padx=5)

tk.Button(

    button_frame,

    text="DELETE",

    width=15,

    bg="#dc3545",

    fg="white",

    command=delete_member

).grid(row=0, column=2, padx=5)

tk.Button(

    button_frame,

    text="CLEAR",

    width=15,

    command=clear_fields

).grid(row=0, column=3, padx=5)

tk.Button(

    button_frame,

    text="REFRESH",

    width=15,

    command=load_members

).grid(row=0, column=4, padx=5)

# -------------------- SEARCH --------------------

search_frame = tk.Frame(

    root,

    bg="#f2f2f2"

)

search_frame.pack(

    fill="x",

    padx=15,

    pady=5

)

tk.Label(

    search_frame,

    text="Search Member:",

    bg="#f2f2f2",

    font=("Arial", 10, "bold")

).pack(side="left", padx=5)

tk.Entry(

    search_frame,

    textvariable=search_var,

    width=35

).pack(side="left", padx=5)

tk.Button(

    search_frame,

    text="SEARCH",

    command=search_member

).pack(side="left", padx=5)

tk.Button(

    search_frame,

    text="SHOW ALL",

    command=load_members

).pack(side="left", padx=5)

# -------------------- TABLE --------------------

table_frame = tk.Frame(root)

table_frame.pack(

    fill="both",

    expand=True,

    padx=15,

    pady=5

)

columns = (

    "ID",

    "Full Name",

    "Age",

    "Gender",

    "Contact",

    "Address",

    "Membership",

    "Start Date",

    "Expiration Date"

)

member_table = ttk.Treeview(

    table_frame,

    columns=columns,

    show="headings",

    height=10

)

for column in columns:

    member_table.heading(

        column,

        text=column

    )

    member_table.column(

        column,

        width=120,

        anchor="center"

    )

member_table.column("ID", width=50)

member_table.pack(

    side="left",

    fill="both",

    expand=True

)

scrollbar = ttk.Scrollbar(

    table_frame,

    orient="vertical",

    command=member_table.yview

)

scrollbar.pack(

    side="right",

    fill="y"

)

member_table.configure(

    yscrollcommand=scrollbar.set

)

member_table.bind(

    "<<TreeviewSelect>>",

    select_member

)

# -------------------- FOOTER --------------------

total_label = tk.Label(

    root,

    text="Total Members: 0",

    font=("Arial", 11, "bold"),

    bg="#f2f2f2"

)

total_label.pack(pady=8)

# -------------------- START APPLICATION --------------------

# Hide dashboard until successful login.

root.withdraw()

# Show login window first.

show_login()

root.mainloop()
