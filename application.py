import pygame
import mediapipe as mp
import time
import math
import cv2
import keyboard
import threading
import numpy as np
import pyautogui
import pydirectinput
import back_end as be

global cap, display, wheel, lastkey, old_angle, video, wheel_vid, comp_vid, mpHands, hands, mpdraw, pTime, acc, results
# Video camera input


def init_vars():
    # cap = cv2.VideoCapture("Input_2.mp4") <- this uses file
    global cap, display, wheel, lastkey, old_angle, video, wheel_vid, comp_vid, mpHands, hands, mpdraw, pTime, acc
    cap = cv2.VideoCapture(0)  # <- this uses camera
    pygame.init()
    display = pygame.display.set_mode((250, 250))
    pygame.display.set_caption('Wheel Visualizer')
    wheel = pygame.image.load("wheel.png")
    lastkey = None
    old_angle = 0

    video = []
    wheel_vid = []
    comp_vid = []

    # Hand computations
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mpdraw = mp.solutions.drawing_utils
    pTime = 0
    acc = 0


def blitRotateCenter(surf, image, tl, ang):

    rotated_image = pygame.transform.rotate(image, ang)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=tl).center)

    surf.blit(rotated_image, new_rect)


init_vars()
thread_start = True
rad_thread_start = True

while True:
    try:
        success, img = cap.read()
        img.flags.writeable = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        display.fill((255, 255, 255))
        rotation_angle = 0
    except IndexError:
        break

# if results.multi_hand_landmarks: # This has two indexes -> one for each hand
    hand1_base = (0, 0, 0)
    hand2_base = (0, 0, 0)
    angle = '0'
    radius = 0
    try:
        rotation_angle = 0
        a = results is not None
        ans = []
        if results.multi_hand_landmarks is not None:
            if len(results.multi_hand_landmarks) == 2:
                # This connects the two hand bases
                hand1_base = results.multi_hand_landmarks[0].landmark[0]
                hand2_base = results.multi_hand_landmarks[1].landmark[0]
                h, w, c = img.shape

                hand1x, hand1y = int(hand1_base.x * w), int(hand1_base.y * h)
                hand2x, hand2y = int(hand2_base.x * w), int(hand2_base.y * h)

                cv2.line(img, (hand1x, hand1y), (hand2x, hand2y), (255, 0, 255), 3)
                mid_x, mid_y = int(hand1x + ((hand2x - hand1x) / 2)), int(hand1y + ((hand2y - hand1y) / 2))
                cv2.circle(img, (mid_x, mid_y), 10, (255, 0, 255), cv2.FILLED)
                x, y = hand2x - hand1x, hand2y - hand1y
                if x != 0:
                    angle = str(round(math.degrees(math.atan(y / x)), 6))

                else:
                    angle = "0"
                angle = float(angle)
                radius = math.hypot(hand2x - mid_x, hand2y - mid_y)
        # wheel functionality
        wheel = pygame.transform.scale(wheel, (250, 250))
        rotation_angle = float(angle)
        if rotation_angle == 0:
            blitRotateCenter(display, wheel, (0, 0), old_angle)
        else:
            blitRotateCenter(display, wheel, (0, 0), rotation_angle)
            old_angle = rotation_angle
        wheel_array = pygame.surfarray.array3d(wheel)
        pygame.display.update()

        if results.multi_hand_landmarks is not None:
            for node in results.multi_hand_landmarks:
                # This draws connections between individual hands
                for i, lm in enumerate(node.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                mpdraw.draw_landmarks(img, node, mpHands.HAND_CONNECTIONS,
                                      connection_drawing_spec=mpdraw.DrawingSpec(color=(28, 235, 76)))

        turn_thread1 = threading.Thread(target=be.turn, args=(angle,))
        turn_thread2 = threading.Thread(target=be.turn, args=(angle,))

        img = cv2.flip(img, 1)
        cv2.putText(img, "Angle: " + str(angle), (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, "Radius: " + str(int(radius)), (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        if thread_start:
            turn_thread1.start()
            thread_start = False
        else:
            turn_thread2.start()
            thread_start = True

        rad_thread1 = threading.Thread(target=be.rad, args=(radius,))
        rad_thread2 = threading.Thread(target=be.rad, args=(radius,))

        if rad_thread_start:
            rad_thread1.start()
            rad_thread_start = False
        else:
            rad_thread2.start()
            rad_thread_start = True

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, "FPS:" + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        # comp_vid.append(img)
        # video.append(img)
        cv2.waitKey(1)

    except IndexError:

        img = cv2.flip(img, 1)
        cv2.imshow("Image", img)
        # video.append(img)
        cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


pygame.display.quit()
cap.release()
