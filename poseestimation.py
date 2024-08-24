import cv2
import mediapipe as mp
cap = cv2.VideoCapture("Videos/bicep.mp4")

# Initializing the MediaPipe Pose Estimation Model
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
while True:
    ret, frame = cap.read()
    if ret:
        # Mediapipe library accepts the RGB images as the input
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frameRGB)
        print(results.pose_landmarks)
       # lmList=[]
       # if results.pose_landmarks:
            #mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            #for id, lm in enumerate(results.pose_landmarks.landmark):
              #  h,w, c = frame.shape
               # print(id, lm)
               # cx, cy = int(lm.x*w), int(lm.y*h)
               # lmList.append([id, cx, cy])
                #cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            #cv2.circle(frame, (lmList[14][1], lmList[14][2]),8, (255,0,255), cv2.FILLED)
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('1'):
           break
    else:
        break