import tkinter as tk
from tkinter import messagebox, ttk
from database import *
from face_utils import *
from datetime import datetime

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Attendance System")
        self.geometry("800x600")
        self.frames = {}
        for F in (WelcomePage, StudentSignupPage, StudentLoginPage, AdminLoginPage, AdminDashboard, LectureSchedulingPage, 
                  StudentDashboard, FaceScanPage, AttendanceConfirmationPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Welcome to Attendance System")
        label.pack()
        tk.Button(self, text="Student Signup", command=lambda: controller.show_frame("StudentSignupPage")).pack()
        tk.Button(self, text="Student Login", command=lambda: controller.show_frame("StudentLoginPage")).pack()
        tk.Button(self, text="Admin Login", command=lambda: controller.show_frame("AdminLoginPage")).pack()

# StudentSignupPage
class StudentSignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Labels and Entries for Name, Student ID, Department, Year, Email, Password
        # Example:
        self.student_id = tk.Entry(self)
        # ...
        tk.Button(self, text="Signup", command=self.signup).pack()

    def signup(self):
        # Get values
        student_id = self.student_id.get()
        # ...
        if add_student(student_id, name, ..., password):
            try:
                encodings = capture_face_encodings(num_samples=5)
                for enc in encodings:
                    add_face_encoding(student_id, enc)
                messagebox.showinfo("Success", "Signup complete!")
                self.controller.show_frame("WelcomePage")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Student ID already exists.")

# Similar classes for other pages: StudentLoginPage (authenticate, go to StudentDashboard)
# AdminLoginPage (authenticate, go to AdminDashboard)
# LectureSchedulingPage (add_lecture, fields for subject, date, etc.)
# StudentDashboard (show lectures, button to mark attendance -> FaceScanPage with lecture selection)
# FaceScanPage (select lecture, check time window, verify_face, if match mark_attendance, go to Confirmation)
# AdminDashboard (schedule lectures, view reports, export CSV)
# AttendanceConfirmationPage (show success, view history)

# For reports, use ttk.Treeview to display tables

# Add back buttons to return to previous pages