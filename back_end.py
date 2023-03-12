import pygame
import mediapipe as mp
import time
import math
import cv2
import keyboard
import numpy as np
import pyautogui
import pydirectinput

"""
Old Code:
this displays the cv2 input to pygame!
frame = pygame.image.frombuffer(imgRGB.tostring(), imgRGB.shape[1::-1], 'RGB')
frame = pygame.transform.flip(frame, flip_x=True, flip_y=False)
display.blit(frame, (0, 0))
pygame.display.update()
    
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter("wheel.mov", fourcc, 20.0, (250, 250))
for frm in wheel_vid:
    out1.write(frm)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output2.mov", fourcc, 20.0, (1920, 1080))
for frm in video:
    out.write(frm)
"""


def turn(ang):
    if 45 > float(ang) > 15:  # small left
        keyboard.release('right')
        keyboard.press('left')
        time.sleep(0.04)
        keyboard.release('left')
        # results.append(1)
    elif -45 < float(ang) < -15:  # small right
        keyboard.release('left')
        keyboard.press('right')
        time.sleep(0.04)
        keyboard.release('right')

        # results.append(1)
    elif float(ang) > 45:  # big left
        keyboard.release('right')
        keyboard.press('left')
        # results.append('l')
    elif float(ang) < -45:  # big right
        keyboard.release('left')
        keyboard.press('right')
        # results.append('r')
    else:
        keyboard.release('left')
        keyboard.release('right')
        # results.append(0)


def rad(radi):
    if radi > 300:
        keyboard.press('space')
        time.sleep(0.02)
        keyboard.release('space')



