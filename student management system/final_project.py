import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 
import re

# List to hold student data
students = []

# Validation function for Name (first character must be a letter, then allow alphabets and spaces)
def validate_name_input(new_value):
    if not new_value:
        return True
    return bool(re.match("^[A-Za-z][A-Za-z ]*$", new_value))  # Only letters and spaces allowed

# Validation function for Email (validates the email format)
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email)) # Regex to check for valid email format

# Validation function for Contact (only 10 digits allowed)
def validate_contact_input(new_value):
    if new_value == "":  # Allow empty input during typing
        return True
    return new_value.isdigit() and len(new_value) <= 10  # Check if input is numeric and 10 digits or less

# Validation function for Roll No.
def validate_roll_no_input(new_value):
    return new_value.isdigit() or new_value == ""  # Roll No should be numeric or empty



"""========================================CRUD Operation========================================"""
# Functions for CRUD (Create, Read, Update, and Delete) operations
def add_student():
    # Get values from input fields
    roll_no = roll_no_entry.get()
    name = name_entry.get()
    father_name = father_name_entry.get()
    mother_name = mother_name_entry.get()
    email = email_entry.get()
    gender = gender_var.get()
    contact = contact_entry.get()
    dob = dob_entry.get()
    session = session_entry.get()
    course = course_entry.get()
    address = address_text.get("1.0", tk.END).strip()

    # Check if all fields are filled
    if not roll_no or not name or not father_name or not mother_name or not email or not gender or not contact or not dob or not session or not course or not address:
        messagebox.showerror("Error", "All fields are required")
        return

    # Validate email
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
        return

    # Check for duplicate Roll No, Session, and Course combination
    for student in students:
        if roll_no == student[1] and session == student[9] and course == student[10]:
            messagebox.showerror("Error", f"Student with Roll No '{roll_no}', Session '{session}', and Course '{course}' already exists.")
            return

    # Add student to the list
    students.append([len(students) + 1, roll_no, name, father_name, mother_name, email, gender, contact, dob, session, course, address])
    messagebox.showinfo("Success", "Student added successfully")
    display_students()  # Refresh the student display
    clear_fields()  # Clear all input fields



def select_student(event):
    # Get selected row in the tree view and load data into the form fields
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item[0])  # Get index of selected item
        student = students[index]

        # Populate form fields with the selected student's data
        roll_no_entry.delete(0, tk.END)
        roll_no_entry.insert(0, student[1])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, student[2])

        father_name_entry.delete(0, tk.END)
        father_name_entry.insert(0, student[3])

        mother_name_entry.delete(0, tk.END)
        mother_name_entry.insert(0, student[4])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, student[5])

        gender_var.set(student[6])

        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, student[7])

        dob_entry.delete(0, tk.END)
        dob_entry.insert(0, student[8])

        session_entry.delete(0, tk.END)
        session_entry.insert(0, student[9])

        course_entry.delete(0, tk.END)
        course_entry.insert(0, student[10])

        address_text.delete("1.0", tk.END)
        address_text.insert(tk.END, student[11])  # Load multi-line address



def update_student():
    # Get selected row to update
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a student to update")
        return

    # Get updated values from input fields
    roll_no = roll_no_entry.get()
    name = name_entry.get()
    father_name = father_name_entry.get()
    mother_name = mother_name_entry.get()
    email = email_entry.get()
    gender = gender_var.get()
    contact = contact_entry.get()
    dob = dob_entry.get()
    session = session_entry.get()
    course = course_entry.get()
    address = address_text.get("1.0", tk.END).strip()

    # Check if all fields are filled
    if not roll_no or not name or not father_name or not mother_name or not email or not gender or not contact or not dob or not session or not course or not address:
        messagebox.showerror("Error", "All fields are required")
        return

    index = tree.index(selected_item[0])

    
    # Check for duplicate student before update
    for i, student in enumerate(students):
        if i != index and roll_no == student[1] and session == student[9] and course == student[10]:
            messagebox.showerror("Error", f"Student with Roll No '{roll_no}', Session '{session}', and Course '{course}' already exists.")
            return

    # Update the student details
    students[index] = [index + 1, roll_no, name, father_name, mother_name, email, gender, contact, dob, session, course, address]
    
    messagebox.showinfo("Success", "Student updated successfully")
    display_students()  # Refresh the student display
    clear_fields()  # Clear the input fields

def delete_student():
    # Get selected row to delete
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a student to delete")
        return

    # Delete the selected students
    for item in selected_item:
        index = tree.index(item)
        del students[index]  # Remove student from the list

     # Re-index the remaining student
    for i, student in enumerate(students):
        student[0] = i + 1  # Update serial numbers


    messagebox.showinfo("Success", "Student deleted successfully")
    display_students()  # Update serial numbers
    clear_fields()  # Clear the input fields

def display_students(filtered_list=None):
    # Delete all existing rows in the TreeView
    for item in tree.get_children():
        tree.delete(item)

    # Display all students or filtered list
    display_data = filtered_list if filtered_list else students
    for student in display_data:
        tree.insert("", tk.END, values=student)  # Insert each student as a row

def clear_fields():
    # Clear all input fields in the form
    roll_no_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    father_name_entry.delete(0, tk.END)
    mother_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    gender_var.set("")  # Reset gender combobox
    contact_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    session_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    address_text.delete("1.0", tk.END)  # Clear multi-line address

def search_students():
    # Get search criteria and input
    search_text = search_entry.get().strip().lower()
    search_type = search_type_var.get()

    if not search_text or not search_type:
        messagebox.showerror("Error", "Select a search type and enter a keyword")
        return

    # Map search type to student field index
    field_index = {
        "Serial No": 0,
        "Roll No": 1,
        "Name": 2,
        "Father's Name": 3,
        "Mother's Name": 4,
        "Email": 5,
        "Gender": 6,
        "Contact": 7,
        "D.O.B": 8,
        "Session": 9,
        "Course": 10,
        "Address": 11,
        
    }.get(search_type, None)

    if field_index is None:
        messagebox.showerror("Error", "Invalid search type")
        return

    # Filter students based on search text
    filtered_students = [
        student for student in students
        if search_text in str(student[field_index]).lower()  # Case-insensitive search
    ]

    # Display filtered students
    if not filtered_students:
        messagebox.showinfo("Search Result", "No matching records found")
    display_students(filtered_students)

def show_all_students():
    # Show all students (reset the display)
    display_students()


"""========================================GUI Setup========================================"""
# GUI setup for the application
root = tk.Tk()
root.title("Student Management System")
root.geometry("1200x600")
root.iconbitmap('student_management_system.ico')

# Input validation registrations
validate_roll_no = root.register(validate_roll_no_input)
validate_name = root.register(validate_name_input)
validate_contact = root.register(validate_contact_input)

# Form inputs
form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack(side=tk.LEFT, fill=tk.Y)

# Roll No
tk.Label(form_frame, text="Roll No:").grid(row=0, column=0, pady=5, sticky=tk.W)
roll_no_entry = tk.Entry(form_frame, validate="key", validatecommand=(validate_roll_no, "%P"))
roll_no_entry.grid(row=0, column=1, pady=5)

# Name
tk.Label(form_frame, text="Name:").grid(row=1, column=0, pady=5, sticky=tk.W)
name_entry = tk.Entry(form_frame, validate="key", validatecommand=(validate_name, "%P"))
name_entry.grid(row=1, column=1, pady=5)

# Father's Name
tk.Label(form_frame, text="Father's Name:").grid(row=2, column=0, pady=5, sticky=tk.W)
father_name_entry = tk.Entry(form_frame, validate="key", validatecommand=(validate_name, "%P"))
father_name_entry.grid(row=2, column=1, pady=5)

# Mother's Name
tk.Label(form_frame, text="Mother's Name:").grid(row=3, column=0, pady=5, sticky=tk.W)
mother_name_entry = tk.Entry(form_frame, validate="key", validatecommand=(validate_name, "%P"))
mother_name_entry.grid(row=3, column=1, pady=5)

# Email
tk.Label(form_frame, text="Email:").grid(row=4, column=0, pady=5, sticky=tk.W)
email_entry = tk.Entry(form_frame)
email_entry.grid(row=4, column=1, pady=5)

# Gender
tk.Label(form_frame, text="Gender:").grid(row=5, column=0, pady=5, sticky=tk.W)
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(form_frame, textvariable=gender_var, width=16, values=["Male", "Female", "Other"], state="readonly")
gender_combo.grid(row=5, column=1, pady=5)

# Contact
tk.Label(form_frame, text="Contact:").grid(row=6, column=0, pady=5, sticky=tk.W)
contact_entry = tk.Entry(form_frame, validate="key", validatecommand=(validate_contact, "%P"))
contact_entry.grid(row=6, column=1, pady=5)

# D.O.B field with calendar
tk.Label(form_frame, text="D.O.B:").grid(row=7, column=0, pady=5, sticky=tk.W)
dob_entry = DateEntry(form_frame, date_pattern="dd-mm-yyyy", width=16, state="readonly")
dob_entry.grid(row=7, column=1, pady=5)

# Session
tk.Label(form_frame, text="Session:").grid(row=8, column=0, pady=5, sticky=tk.W)
session_entry = tk.Entry(form_frame)
session_entry.grid(row=8, column=1, pady=5)

# Course
tk.Label(form_frame, text="Course:").grid(row=9, column=0, pady=5, sticky=tk.W)
course_entry = tk.Entry(form_frame)
course_entry.grid(row=9, column=1, pady=5)

# Address
tk.Label(form_frame, text="Address:").grid(row=10, column=0, pady=5, sticky=tk.W)
address_text = tk.Text(form_frame, height=10, width=15)
address_text.grid(row=10, column=1, pady=5)





"""========================================Button========================================"""
# Button frame
btn_frame = tk.Frame(form_frame, pady=10)
btn_frame.grid(row=11, column=0, columnspan=2)

# Add button
add_button = tk.Button(btn_frame, text="Add", width=6, command=add_student)
add_button.grid(row=0, column=0, padx=5)

# Update button
update_button = tk.Button(btn_frame, text="Update", command=update_student)
update_button.grid(row=0, column=1, padx=5)

# Delete button
delete_button = tk.Button(btn_frame, text="Delete", command=delete_student)
delete_button.grid(row=0, column=2, padx=5)

# Clear button
clear_button = tk.Button(btn_frame, text="Clear", width=6, command=clear_fields)
clear_button.grid(row=0, column=3, padx=5)





"""========================================Search Section========================================"""
# Search frame
search_frame = tk.Frame(root, padx=10, pady=10)
search_frame.pack(fill=tk.X)

# Search options and input
search_type_var = tk.StringVar()
search_type_combo = ttk.Combobox(search_frame, textvariable=search_type_var, width=20, values=[
    "Serial No", "Roll No", "Name", "Father's Name", "Mother's Name", "Email", "Gender", "Contact", "D.O.B", "Session", "Course", "Address"
], state="readonly")
search_type_combo.pack(side=tk.LEFT, padx=5)

# Search frame
search_entry = tk.Entry(search_frame, width=20)
search_entry.pack(side=tk.LEFT, padx=5)

#Search button
search_button = tk.Button(search_frame, text="Search", command=search_students, width=8)
search_button.pack(side=tk.LEFT, padx=5)

# Show all button
show_all_button = tk.Button(search_frame, text="Show All", command=show_all_students, width=8)
show_all_button.pack(side=tk.LEFT, padx=5)





"""========================================Treeview Section========================================"""
# Treeview frame
tree_frame = tk.Frame(root, padx=10, pady=10)
tree_frame.pack(fill=tk.BOTH, expand=True)

# Scroll bar vertical
tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Scroll bar horizontal
tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Treeview (student table)
columns = ("Serial No", "Roll No", "Name", "Father's Name", "Mother's Name", "Email", "Gender", "Contact", "D.O.B", "Session", "Course", "Address")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15, 
                    yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
tree.pack(fill=tk.BOTH, expand=True)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.bind("<<TreeviewSelect>>", select_student)

root.mainloop()
