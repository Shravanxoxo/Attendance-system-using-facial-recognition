import sqlite3
import pickle
from datetime import datetime
import hashlib
import os

DB_PATH = 'attendance.db'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    # Create tables (schema as above)
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (...)''')  # Paste full schema here
    # Similarly for other tables
    conn.commit()
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM admins WHERE username=?", ("admin",))
    if not cursor.fetchone():
        hashed_pw = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", hashed_pw))
    conn.commit()
    conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Student functions
def add_student(student_id, name, department, year, email, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO students (student_id, name, department, year, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                       (student_id, name, department, year, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Duplicate student_id
    finally:
        conn.close()

def add_face_encoding(student_id, encoding):
    conn = connect_db()
    cursor = conn.cursor()
    pickled_encoding = pickle.dumps(encoding)
    cursor.execute("INSERT INTO face_encodings (student_id, encoding) VALUES (?, ?)", (student_id, pickled_encoding))
    conn.commit()
    conn.close()

def get_student_encodings(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT encoding FROM face_encodings WHERE student_id=?", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [pickle.loads(row[0]) for row in rows]

def authenticate_student(student_id, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM students WHERE student_id=? AND password=?", (student_id, hashed_pw))
    student = cursor.fetchone()
    conn.close()
    return student

# Admin functions
def authenticate_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, hashed_pw))
    admin = cursor.fetchone()
    conn.close()
    return admin

def add_lecture(subject, date, time, teacher, class_div):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lectures (subject, date, time, teacher, class_div) VALUES (?, ?, ?, ?, ?)",
                   (subject, date, time, teacher, class_div))
    lecture_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lecture_id

def get_lectures(today_date=None):
    conn = connect_db()
    cursor = conn.cursor()
    if today_date:
        cursor.execute("SELECT * FROM lectures WHERE date=?", (today_date,))
    else:
        cursor.execute("SELECT * FROM lectures")
    lectures = cursor.fetchall()
    conn.close()
    return lectures

def mark_attendance(student_id, lecture_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Check if already marked
    cursor.execute("SELECT * FROM attendance WHERE student_id=? AND lecture_id=?", (student_id, lecture_id))
    if cursor.fetchone():
        conn.close()
        return False  # Duplicate
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO attendance (student_id, lecture_id, status, timestamp) VALUES (?, ?, ?, ?)",
                   (student_id, lecture_id, "Present", timestamp))
    conn.commit()
    conn.close()
    return True

def get_attendance_history(student_id=None, lecture_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    if student_id:
        cursor.execute("""
            SELECT a.*, l.subject, l.date, l.time FROM attendance a 
            JOIN lectures l ON a.lecture_id = l.id 
            WHERE a.student_id=?
        """, (student_id,))
    elif lecture_id:
        cursor.execute("""
            SELECT a.*, s.name FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            WHERE a.lecture_id=?
        """, (lecture_id,))
    else:
        cursor.execute("SELECT * FROM attendance")
    history = cursor.fetchall()
    conn.close()
    return history

def export_attendance_to_csv(lecture_id):
    history = get_attendance_history(lecture_id=lecture_id)
    if not history:
        return None
    os.makedirs('exports', exist_ok=True)
    filename = f"exports/attendance_lecture_{lecture_id}.csv"
    with open(filename, 'w') as f:
        f.write("ID,Student ID,Name,Lecture ID,Status,Timestamp\n")
        for row in history:
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n")  # Adjust indices
    return filename

# Add more functions as needed, e.g., for reports