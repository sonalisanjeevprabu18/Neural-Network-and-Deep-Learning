import cv2
import csv
from datetime import datetime
import os
YOUR_NAME = "Sonali"
ATTENDANCE_FILE = "attendance.csv"
FONT_MAIN = cv2.FONT_HERSHEY_DUPLEX
FONT_SMALL = cv2.FONT_HERSHEY_SIMPLEX
COLOR_PRIMARY = (0, 255, 0)
COLOR_WARNING = (0, 0, 255)
COLOR_INFO = (255, 255, 255)
COLOR_BOX_IDLE = (255, 120, 0)
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time", "Status"])
def mark_attendance(name):
    now = datetime.now()
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            name,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            "Present"
        ])
    print(f"✓ Attendance marked for {name}")
def draw_panel(frame, alpha=0.6):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 90), (0, 0, 0), -1)
    return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
def main():
    print("=" * 55)
    print(" SMART FACE ATTENDANCE SYSTEM ")
    print("=" * 55)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam not accessible")
        return
    attendance_marked = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        frame = draw_panel(frame)

        cv2.putText(frame, "ATTENDANCE SYSTEM",
                    (15, 30), FONT_MAIN, 0.9, COLOR_INFO, 2)

        cv2.putText(frame, f"Detected Faces: {len(faces)}",
                    (15, 60), FONT_SMALL, 0.7, COLOR_INFO, 2)

        status_text = "Attendance Marked ✓" if attendance_marked else "Press SPACE to Mark Attendance"
        status_color = COLOR_PRIMARY if attendance_marked else COLOR_WARNING

        cv2.putText(frame, status_text,
                    (350, 60), FONT_SMALL, 0.7, status_color, 2)
        for (x, y, w, h) in faces:
            box_color = COLOR_PRIMARY if attendance_marked else COLOR_BOX_IDLE
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)

            label = "Present ✓" if attendance_marked else "Face Detected"
            cv2.putText(frame, label,
                        (x, y - 10), FONT_SMALL, 0.7, box_color, 2)
        cv2.imshow("Attendance | SPACE = Mark | Q = Quit", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" ") and len(faces) > 0 and not attendance_marked:
            mark_attendance(YOUR_NAME)
            attendance_marked = True

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not attendance_marked:
        print("⚠ Attendance not marked")
    else:
        print("✓ System closed successfully")

if __name__ == "__main__":
    main()
