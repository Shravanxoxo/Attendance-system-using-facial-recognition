## Installation Guide (Windows)

### Prerequisites

Before installing the Python libraries, install the following software:

#### 1. Python

Download and install Python 3.10 or later:
https://www.python.org/downloads/

While installing, make sure to check **"Add Python to PATH"**.

#### 2. Visual Studio Build Tools

Required for compiling dlib and other C++ dependencies.

Download:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

During installation, select:

* Desktop development with C++
* MSVC Compiler
* Windows SDK

#### 3. CMake

Required for building dlib on some systems.

Download:
https://cmake.org/download/

During installation, select:

* Add CMake to system PATH

---

## Python Package Installation

Install the required libraries:

```bash
pip install opencv-python
pip install face-recognition
pip install dlib
pip install pillow
pip install numpy
```

Or install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Running the Project

1. Clone the repository:


2. Open the project folder:


3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the application:

```bash
python main.py
```

---

## Features

* Face-based attendance marking
* Student Registration
* Admin Dashboard
* Student Dashboard
* SQLite Database Storage
* SHA-256 Password Security
* Real-time Face Recognition
* Offline Operation
* Proxy Attendance Prevention

---

## Technologies Used

* Python
* OpenCV
* face_recognition
* dlib
* Tkinter
* SQLite
* NumPy
* Pillow (PIL)

---

## Author

Shravan Patil


