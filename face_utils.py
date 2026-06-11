import cv2
import face_recognition
import face_recognition_models
import numpy as np
from datetime import datetime, timedeltaP

def capture_face_encodings(num_samples=5):
    video_capture = cv2.VideoCapture(0)
    encodings = []
    print("Capturing faces. Look at the camera...")
    while len(encodings) < num_samples:
        ret, frame = video_capture.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            encodings.append(face_encoding)
            print(f"Captured {len(encodings)}/{num_samples}")
        cv2.imshow('Capture Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    if len(encodings) < num_samples:
        raise ValueError("Failed to capture enough face samples.")
    return encodings  # List of encodings

def verify_face(student_id, confidence_threshold=0.6):
    video_capture = cv2.VideoCapture(0)
    known_encodings = get_student_encodings(student_id)  # From database.py
    if not known_encodings:
        video_capture.release()
        return False
    matched = False
    print("Scanning face for verification...")
    while not matched:
        ret, frame = video_capture.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            unknown_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            distances = face_recognition.face_distance(known_encodings, unknown_encoding)
            min_distance = np.min(distances)
            if min_distance < confidence_threshold:
                matched = True
        cv2.imshow('Verify Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return matched

def is_within_time_window(lecture_date, lecture_time, window_minutes=30):
    lecture_datetime = datetime.strptime(f"{lecture_date} {lecture_time}", "%Y-%m-%d %H:%M")
    now = datetime.now()
    start = lecture_datetime - timedelta(minutes=window_minutes)
    end = lecture_datetime + timedelta(minutes=window_minutes)
    return start <= now <= end