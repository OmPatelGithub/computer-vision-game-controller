import cv2
import pygame 
import mediapipe as mp
import time
import math


def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

# Video camera input
cap = cv2.VideoCapture("Input_2.mp4")
# cap = cv.VideoCapture(0)
pygame.init()
display = pygame.display.set_mode((250, 250))
pygame.display.set_caption('Wheel Visualizer')
wheel = pygame.image.load("wheel.png")

video = []

# Hand computations
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpdraw = mp.solutions.drawing_utils
pTime = 0
acc = 0

while True:
    
    try:
        success, img = cap.read()
        img.flags.writeable = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        display.fill((255,255,255))
        rotation_angle = 0
    except:
        break

    
    # this displays the cv2 input to pygame!
    # frame = pygame.image.frombuffer(imgRGB.tostring(), imgRGB.shape[1::-1], 'RGB')
    # frame = pygame.transform.flip(frame, flip_x = True, flip_y = False)
    # display.blit(frame, (0, 0))
    # pygame.display.update()
    

    

# if results.multi_hand_landmarks: # This has two indexes -> one for each hand
    hand1_base = (0, 0, 0)
    hand2_base = (0, 0, 0)
    angle = '0'


    try:

        if len(results.multi_hand_landmarks) == 2: # This connects the two hand bases
            hand1_base = results.multi_hand_landmarks[0].landmark[0]
            hand2_base = results.multi_hand_landmarks[1].landmark[0]
            h, w, c = img.shape

            hand1x, hand1y = int(hand1_base.x * w), int(hand1_base.y * h)
            hand2x, hand2y = int(hand2_base.x * w), int(hand2_base.y * h)
            
            cv2.line(img, (hand1x, hand1y), (hand2x, hand2y), (255, 0, 255), 3)
            mid_x, mid_y = int(hand1x + ((hand2x - hand1x) / 2)), int(hand1y + ((hand2y - hand1y) / 2))
            cv2.circle(img, (mid_x, mid_y), 10, (255, 0, 255), cv2.FILLED)
            x, y = hand2x - hand1x, hand2y - hand1y
        
            angle = str(round(math.degrees(math.atan(y/x)), 6))
            rotation_angle = float(angle)
            radius = math.hypot(hand2x - mid_x, hand2y - mid_y)

    
        # wheel = pygame.transform.scale(wheel, (250, 250))
        # blitRotateCenter(display, wheel, (0, 0), rotation_angle)
        # pygame.display.update()

        
        for node in results.multi_hand_landmarks: # This draws connections between individual hands
            for id, lm in enumerate(node.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            mpdraw.draw_landmarks(img, node, mpHands.HAND_CONNECTIONS, connection_drawing_spec = mpdraw.DrawingSpec(color=(28, 235, 76)))

        img = cv2.flip(img, 1)
        

        cv2.putText(img, "Angle: " + angle, (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime



        


        cv2.putText(img, "FPS:" + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # cv.imshow("Image", img)
        video.append(img)
        cv2.waitKey(1)

    except:

        img = cv2.flip(img, 1)
        # cv.imshow("Image", img)
        video.append(img)
        cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output2.mov", fourcc, 20.0, (1920,1080))
for frm in video:
    out.write(frm)

cap.release()
out.release()
cv2.destroyAllWindows
