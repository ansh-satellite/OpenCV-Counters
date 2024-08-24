import tkinter as tk
from tkinter import ttk
import cv2
import time
import numpy as np
import pyttsx3
import poseestimationmodule as pm

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def start_counter(exercise):
    cap = cv2.VideoCapture(f"../Videos/{exercise}.mp4")  # Ensure this path is correct
    detector = pm.poseDetector()
    dir = 0
    count = 0
    total_sets = 3
    reps_per_set = 10
    current_set = 1
    ptime = 0

    logfile = f"{exercise}_workout_log.csv"
    header = ['Date', 'Time', 'Exercise', 'Total Sets', 'Total Reps']

    try:
        with open(logfile, 'x') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass

    while True:
        ret, frame = cap.read()
        if ret:
            frame = detector.findPose(frame)
            lmList = detector.findPosition(frame, draw=False)

            if len(lmList) != 0:
                if exercise == "pushup":
                    angle = detector.findAngle(frame, 11, 13, 15, draw=True)
                    per = np.interp(angle, (195, 280), (0, 100))
                    bar = np.interp(angle, (195, 280), (650, 100))
                elif exercise == "bicep":
                    angle = detector.findAngle(frame, 12, 14, 16, draw=True)
                    per = np.interp(angle, (190, 300), (0, 100))
                    bar = np.interp(angle, (190, 300), (650, 100))

                color = (255, 100, 100)

                if per == 100:
                    color = (100, 255, 100)
                    if dir == 0:
                        count += 1
                        speak(f'Rep {count} complete')
                        dir = 1
                        if count % reps_per_set == 0:
                            speak(f'Set {current_set} complete')
                            current_set += 1
                if per == 0:
                    color = (100, 100, 255)
                    if dir == 1:
                        dir = 0

                cv2.putText(frame, f'{exercise.capitalize()}', (30, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                cv2.putText(frame, f'Set: {current_set}/{total_sets}', (30, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                cv2.putText(frame, f'Reps: {count % reps_per_set}/{reps_per_set}', (30, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                cv2.putText(frame, f'Total Reps: {count}', (30, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                cv2.rectangle(frame, (1600, 100), (1675, 650), color, 3)
                cv2.rectangle(frame, (1600, int(bar)), (1675, 650), color, cv2.FILLED)
                cv2.putText(frame, f'{int(per)}%', (1600, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

                ctime = time.time()
                fps = 1 / (ctime - ptime)
                ptime = ctime
                cv2.putText(frame, f'FPS: {int(fps)}', (30, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

            frame = cv2.resize(frame, (0, 0), None, fx=0.6, fy=0.6)
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                break
        else:
            print("Video capture failed or video ended.")
            break

    with open(logfile, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), exercise.capitalize(), total_sets, count])

    cap.release()
    cv2.destroyAllWindows()

def on_start_button_click():
    exercise = selected_exercise.get().lower()
    start_counter(exercise)

# Create the main window
root = tk.Tk()
root.title("Exercise Counter")

# Create a label and dropdown menu for exercise selection
label = tk.Label(root, text="Select Exercise:")
label.pack(pady=10)

selected_exercise = tk.StringVar()
exercise_options = ["Pushup", "Bicep"]
dropdown = ttk.Combobox(root, textvariable=selected_exercise, values=exercise_options)
dropdown.pack(pady=10)

# Create a start button
start_button = tk.Button(root, text="Start", command=on_start_button_click)
start_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
