from gui import AttendanceApp
from database import init_db

if __name__ == "__main__":
    init_db()
    app = AttendanceApp()
    app.mainloop()