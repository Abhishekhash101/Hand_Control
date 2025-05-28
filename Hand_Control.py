import cv2
import mediapipe as mp  #by google
import time
import pyautogui
  
cap=cv2.VideoCapture(0)


mphands=mp.solutions.hands

hands=mphands.Hands(max_num_hands=1)
mpDraw=mp.solutions.drawing_utils

pTime=0
cTime=0

# 4- thumb
# 8=1st finger
# 12-2nd
# 16-3rd
# 20- last fingure

tips_ki_id=[4,8,12,16,20]


def Check_Finger_up_down(hand_landmarks):
    finger=[]

    if hand_landmarks.landmark[tips_ki_id[0]].x< hand_landmarks.landmark[tips_ki_id[0]-1].x:
        finger.append(1)

    else:
        finger.append(0)

    
    for id in range(1,5):
        if hand_landmarks.landmark[tips_ki_id[id]].y < hand_landmarks.landmark[tips_ki_id[id]-2].y:
            finger.append(1)
        else:
            finger.append(0)

    return finger

prev_action_done_any=None

while True:

    isTrue,img=cap.read()
    img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(imgRGB)
    # print(result.multi_hand_landmarks)

    detection_by_camera="NOPE"

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLms,mphands.HAND_CONNECTIONS)

            fingers=Check_Finger_up_down(handLms)
            if fingers==[1,1,1,1,1]:
                detection_by_camera="Full fist open (Full Screen Mode)"
                if prev_action_done_any!=detection_by_camera:
                    pyautogui.press('f')
                    prev_action_done_any=detection_by_camera
                    print(detection_by_camera)

            elif fingers==[0,0,0,0,0]:
                detection_by_camera="Full fist close (pause the screen)"
                if prev_action_done_any!=detection_by_camera:
                    pyautogui.press('space')
                    prev_action_done_any=detection_by_camera
                    print(detection_by_camera)

                    #HERE I AM GOING AND HAND COOL DOWN FOR THE SEEK RIGHT/LEFT 
                    
            # elif fingers==[0,1,1,0,0]:
            #     detection_by_camera="Two Fingure detected (Right)"
            #     if prev_action_done_any!=detection_by_camera:
            #         pyautogui.press('right')
            #         prev_action_done_any=detection_by_camera
            #         print(detection_by_camera)

            # elif fingers==[0,1,0,0,0]:
            #     detection_by_camera="1 fingure (Left)"
            #     if prev_action_done_any!=detection_by_camera:
            #         pyautogui.press('left')
            #         prev_action_done_any=detection_by_camera
            #         print(detection_by_camera)

            else:
                prev_action_done_any=None

            


    cTime=time.time()
    fps=1/(cTime-pTime)

    pTime=cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow('cap',img)

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()