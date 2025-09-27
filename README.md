# SmartFace Group Attendance System

SmartFace Group Attendance System is a Python-based application that uses face recognition to automatically mark attendance for students from **group photos**. The system generates a CSV file for record-keeping and provides a quick summary of present and absent students. Built with Streamlit for an interactive user interface.

---

## Features

- Upload multiple **group photos** at once (up to 5 images)
- Automatically detect faces in group photos
- Match detected faces with registered student images
- Mark students as Present or Absent
- Save attendance as a CSV file with date, time, and subject
- Display a summary and detailed attendance list

---

## Requirements

- Python 3.8+
- Libraries:
  - `streamlit`
  - `face_recognition`
  - `opencv-python`
  - `numpy`
  - `pandas`

Install required libraries using:

```bash
pip install streamlit face_recognition opencv-python numpy pandas
