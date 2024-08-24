import cv2
import time
import numpy as np
import pyttsx3
import csv
import poseestimationmodule as pm

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize video capture and pose detector
cap = cv2.VideoCapture("../Videos/pushup.mp4")  # Ensure this path is correct
detector = pm.poseDetector()

# Initialize counters and direction
dir = 0
count = 0
total_sets = 3
reps_per_set = 10
current_set = 1
ptime = 0

# CSV logging
logfile = "pushup_workout_log.csv"
header = ['Date', 'Time', 'Exercise', 'Total Sets', 'Total Reps']

# Check if log file exists and write header if not
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
            angle = detector.findAngle(frame, 11, 13, 15, draw=True)
            per = np.interp(angle, (195, 280), (0, 100))
            bar = np.interp(angle, (195, 280), (650, 100))
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

            # Displaying Current Exercise and Sets/Reps Count
            cv2.putText(frame, f'Push-Ups', (30, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            #cv2.putText(frame, f'Set: {current_set}/{total_sets}', (30, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            cv2.putText(frame, f'Reps: {count % reps_per_set}/{reps_per_set}', (30, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.putText(frame, f'Total Reps: {count}', (30, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

            # Displaying the Bar Count
            cv2.rectangle(frame, (1600, 100), (1675, 650), color, 3)
            cv2.rectangle(frame, (1600, int(bar)), (1675, 650), color, cv2.FILLED)
            cv2.putText(frame, f'{int(per)}%', (1600, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

            # Displaying the FPS
            ctime = time.time()
            fps = 1 / (ctime - ptime)
            ptime = ctime
            cv2.putText(frame, f'FPS: {int(fps)}', (30, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        frame = cv2.resize(frame, (0, 0), None, fx=0.6, fy=0.6)
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('1'):
            break
    else:
        print("Video capture failed or video ended.")
        break

# Log the workout data
with open(logfile, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), 'Push-Ups', total_sets, count])

cap.release()
cv2.destroyAllWindows()
