import customtkinter
import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def compute_average():
    prelims = entry_prelims.get()
    midterms = entry_midterms.get()
    finals = entry_finals.get()

    if not is_float(prelims):
        messagebox.showerror("Invalid Input", "Prelims value must be a number.")
        return
    if not is_float(midterms):
        messagebox.showerror("Invalid Input", "Midterms value must be a number.")
        return
    if not is_float(finals):
        messagebox.showerror("Invalid Input", "Finals value must be a number.")
        return

    prelims = float(prelims)
    midterms = float(midterms)
    finals = float(finals)

    average = (prelims + midterms + finals) / 3

    entry_average.delete(0, "end")
    entry_average.insert(0, str(average))

    grade = ""
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"

    entry_grade.delete(0, "end")
    entry_grade.insert(0, grade)

def insert_data():
    student_number = entry_student_number.get()
    full_name = entry_full_name.get()
    prelims = entry_prelims.get()
    midterms = entry_midterms.get()
    finals = entry_finals.get()
    average = entry_average.get()
    grade = entry_grade.get()

    if not student_number or not full_name or not prelims or not midterms or not finals:
        messagebox.showerror("Incomplete Input", "Please fill in all the required fields.")
        return

    if len(student_number) != 9 or not student_number.isdigit():
        messagebox.showerror("Invalid Input", "Student number must be a 9-digit number.")
        return

    if not is_float(prelims):
        messagebox.showerror("Invalid Input", "Prelims value must be a number.")
        return
    if not is_float(midterms):
        messagebox.showerror("Invalid Input", "Midterms value must be a number.")
        return
    if not is_float(finals):
        messagebox.showerror("Invalid Input", "Finals value must be a number.")
        return

    prelims = float(prelims)
    midterms = float(midterms)
    finals = float(finals)
    average = float(average)

    try:
        con = mysql.connector.connect(host='localhost', database='scoresensei', user='root', password='')
        cur = con.cursor()

        # Check if the student number already exists
        query = f"SELECT * FROM grading_system WHERE Student_Number = '{student_number}'"
        cur.execute(query)

        if cur.fetchone() is not None:
            messagebox.showerror("Duplicate Entry", "Student number already exists.")
        else:
            # Check if the student name already exists
            query = f"SELECT * FROM grading_system WHERE Full_Name = '{full_name}'"
            cur.execute(query)

            if cur.fetchone() is not None:
                messagebox.showerror("Duplicate Entry", "Student name already exists.")
            else:
                # Insert the data into the database
                query = f"INSERT INTO grading_system (Student_Number, Full_Name, Prelims, Midterms, Finals, student_avg, Grade) VALUES ('{student_number}', '{full_name}', {prelims}, {midterms}, {finals}, {average}, '{grade}')"
                cur.execute(query)
                con.commit()
                # Clear the text fields
                entry_student_number.delete(0, 'end')
                entry_full_name.delete(0, 'end')
                entry_prelims.delete(0, 'end')
                entry_midterms.delete(0, 'end')
                entry_finals.delete(0, 'end')
                entry_average.delete(0, 'end')
                entry_grade.delete(0, 'end')

                messagebox.showinfo("Success", "Imported Successfully")


        cur.close()

    except Error as error:
        print("Insert data failed: {}".format(error))
    finally:
        if con.is_connected():
            con.close()
            print("MySQL Connection is now CLOSED")

def retrieve_record():
    student_number = entry_search.get()

    if not student_number:
        messagebox.showerror("Incomplete Input", "Please enter a student number.")
        return

    try:
        con = mysql.connector.connect(host='localhost', database='scoresensei', user='root', password='')
        cur = con.cursor()

        # Retrieve the record from the database based on the student number
        query = f"SELECT * FROM grading_system WHERE Student_Number = '{student_number}'"
        cur.execute(query)

        record = cur.fetchone()

        if record is None:
            messagebox.showinfo("Record Not Found", "No record found for the given student number.")
        else:
            # Display the retrieved record
            entry_student_number.delete(0, 'end')
            entry_full_name.delete(0, 'end')
            entry_prelims.delete(0, 'end')
            entry_midterms.delete(0, 'end')
            entry_finals.delete(0, 'end')
            entry_average.delete(0, 'end')
            entry_grade.delete(0, 'end')

            entry_student_number.insert(0, str(record[1]))  # Displaying student number instead of ID
            entry_full_name.insert(0, record[2])
            entry_prelims.insert(0, str(record[3]))
            entry_midterms.insert(0, str(record[4]))
            entry_finals.insert(0, str(record[5]))
            entry_average.insert(0, str(record[6]))
            entry_grade.insert(0, record[7])

        cur.close()

    except Error as error:
        print("Retrieve record failed: {}".format(error))
    finally:
        if con.is_connected():
            con.close()
            print("MySQL Connection is now CLOSED")

def clear_search_results():
    entry_student_number.delete(0, 'end')
    entry_full_name.delete(0, 'end')
    entry_prelims.delete(0, 'end')
    entry_midterms.delete(0, 'end')
    entry_finals.delete(0, 'end')
    entry_average.delete(0, 'end')
    entry_grade.delete(0, 'end')
    entry_search.delete(0, 'end')



def open_main_page():
    title_frame.pack_forget()
    main_frame.pack(pady=20, padx=60, fill="both", expand=True)

def exit_program():
    root.quit()

root = ctk.CTk()
root.geometry("900x800")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

# Title Page
title_frame = ctk.CTkFrame(master=root)
title_frame.pack(pady=300)

label_title = ctk.CTkLabel(master=title_frame, text="MAM SAYO", font=("Roboto", 50, "bold"))
label_title.pack(pady=30)

button_start = ctk.CTkButton(master=title_frame, text="Start", command=open_main_page)
button_start.pack()

# Main Page
main_frame = ctk.CTkFrame(master=root)
main_frame.pack_forget()  # Hide initially

label_student_number = ctk.CTkLabel(master=main_frame, text="Student Number:" )
label_student_number.pack()

entry_student_number = ctk.CTkEntry(master=main_frame,)
entry_student_number.pack()

label_full_name = ctk.CTkLabel(master=main_frame, text="Full Name:")
label_full_name.pack()

entry_full_name = ctk.CTkEntry(master=main_frame)
entry_full_name.pack()

label_prelims = ctk.CTkLabel(master=main_frame, text="Prelims:")
label_prelims.pack()

entry_prelims = ctk.CTkEntry(master=main_frame)
entry_prelims.pack()

label_midterms = ctk.CTkLabel(master=main_frame, text="Midterms:")
label_midterms.pack()

entry_midterms = ctk.CTkEntry(master=main_frame)
entry_midterms.pack()

label_finals = ctk.CTkLabel(master=main_frame, text="Finals:")
label_finals.pack()

entry_finals = ctk.CTkEntry(master=main_frame)
entry_finals.pack()

button_compute = ctk.CTkButton(master=main_frame, text="Compute Average", command=compute_average)
button_compute.pack(pady=12)

label_average = ctk.CTkLabel(master=main_frame, text="Average:")
label_average.pack()

entry_average = ctk.CTkEntry(master=main_frame)
entry_average.pack()

label_grade = ctk.CTkLabel(master=main_frame, text="Grade:")
label_grade.pack()

entry_grade = ctk.CTkEntry(master=main_frame)
entry_grade.pack()

button_insert = ctk.CTkButton(master=main_frame, text="Import to MySQL", command=insert_data)
button_insert.pack(pady=12)

label_search = ctk.CTkLabel(master=main_frame, text="Search by Student Number:")
label_search.pack()

entry_search = ctk.CTkEntry(master=main_frame)
entry_search.pack()

button_retrieve = ctk.CTkButton(master=main_frame, text="Retrieve Record", command=retrieve_record)
button_retrieve.pack(pady=12)


button_done = ctk.CTkButton(master=main_frame, text="Clear", command=clear_search_results)
button_done.pack(pady=12)

button_exit = ctk.CTkButton(master=main_frame, text="Exit", command=exit_program)
button_exit.pack(pady=12)

root.mainloop()