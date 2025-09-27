import streamlit as st
import face_recognition
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# 1. Loading student face encodings
st.title("Class Attendance System")

STUDENTS_FOLDER = "students"
student_encodings = {}
student_names = []

for file in os.listdir(STUDENTS_FOLDER):
    if file.endswith((".jpg",".png")):
        name = ''.join([i for i in file if not i.isdigit()]).replace(".jpg","").replace(".png","").strip()
        image_path = os.path.join(STUDENTS_FOLDER, file)
        img = face_recognition.load_image_file(image_path)
        enc = face_recognition.face_encodings(img)
        if enc:
            if name not in student_encodings:
                student_encodings[name] = []
            student_encodings[name].append(enc[0])
            if name not in student_names:
                student_names.append(name)

# 2. Getting User Inputs
subject_name = st.text_input("Enter Subject Name")
uploaded_files = st.file_uploader("Upload Class Photos (up to 5)", type=["jpg","png"], accept_multiple_files=True)

if st.button("Mark Attendance"):

    if not subject_name:
        st.warning("Please enter subject name")
    elif not uploaded_files:
        st.warning("Please upload at least 1 photo")
    else:
        # 3. Processing Photos
        present_students = set()
        for uploaded_file in uploaded_files:
            # Converting uploaded file to OpenCV format
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detecting faces
            face_locations = face_recognition.face_locations(rgb_img)
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

            for face_enc in face_encodings:
                # Comparing with student encodings
                for name, enc_list in student_encodings.items():
                    matches = face_recognition.compare_faces(enc_list, face_enc, tolerance=0.5)
                    if True in matches:
                        present_students.add(name)

        # 4. Marking Absent / Present
        attendance = []
        for name in student_names:
            status = "Present" if name in present_students else "Absent"
            attendance.append([name, status])

        df = pd.DataFrame(attendance, columns=["Name", "Status"])

        # 5. Save Attendance CSV
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M")
        filename = f"{subject_name}_{date_str}_{time_str}.csv"
        df.to_csv(filename, index=False)

        # 6. Display Results
        st.success(f"Attendance saved as {filename}")
        st.write("### Summary")
        st.write(f"Total Students: {len(student_names)}")
        st.write(f"Present: {len(present_students)}")
        st.write(f"Absent: {len(student_names) - len(present_students)}")

        st.write("### Attendance List")
        st.dataframe(df)
