import cv2
import mediapipe as mp
import pyautogui

# screen size
screen_w, screen_h = pyautogui.size()

# mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# camera
cap = cv2.VideoCapture(0)

# smoothing variables
prev_x, prev_y = 0, 0
smoothening = 7

# click cooldown
clicking = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = img.shape

            # index finger
            ix = int(hand_landmarks.landmark[8].x * w)
            iy = int(hand_landmarks.landmark[8].y * h)

            # thumb
            tx = int(hand_landmarks.landmark[4].x * w)
            ty = int(hand_landmarks.landmark[4].y * h)

            # map to screen
            screen_x = int(hand_landmarks.landmark[8].x * screen_w)
            screen_y = int(hand_landmarks.landmark[8].y * screen_h)

            # smoothing formula
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            # draw points
            cv2.circle(img, (ix, iy), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (tx, ty), 10, (0, 255, 0), cv2.FILLED)

            # distance
            distance = ((ix - tx)**2 + (iy - ty)**2) ** 0.5

            # click logic (stable)
            if distance < 40:
                if not clicking:
                    pyautogui.click()
                    clicking = True
            else:
                clicking = False

    cv2.imshow("Atlas Mark II", img)
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()