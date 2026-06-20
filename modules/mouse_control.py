import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time

pyautogui.FAILSAFE = False


class HandMouseController:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.detector = HandDetector(
            maxHands=1,
            detectionCon=0.8
        )

        self.screen_w, self.screen_h = pyautogui.size()

        self.prev_x = 0
        self.prev_y = 0

        self.last_click = 0
        self.last_right = 0

    def run(self):

        while True:

            success, img = self.cap.read()

            if not success:
                continue

            hands, img = self.detector.findHands(img)

            if hands:

                hand = hands[0]

                lm = hand["lmList"]

                index_x, index_y = lm[8][:2]

                cam_h, cam_w, _ = img.shape

                target_x = (
                    index_x / cam_w
                ) * self.screen_w

                target_y = (
                    index_y / cam_h
                ) * self.screen_h

                smooth_x = self.prev_x + (
                    target_x - self.prev_x
                ) / 5

                smooth_y = self.prev_y + (
                    target_y - self.prev_y
                ) / 5

                pyautogui.moveTo(
                    smooth_x,
                    smooth_y
                )

                self.prev_x = smooth_x
                self.prev_y = smooth_y

                fingers = self.detector.fingersUp(hand)

                # LEFT CLICK
                length, _, img = self.detector.findDistance(
                    lm[4][:2],
                    lm[8][:2],
                    img
                )

                if length < 35:

                    if time.time() - self.last_click > 0.7:
                        pyautogui.click()
                        self.last_click = time.time()

                # RIGHT CLICK
                length2, _, img = self.detector.findDistance(
                    lm[4][:2],
                    lm[12][:2],
                    img
                )

                if length2 < 35:

                    if time.time() - self.last_right > 0.7:
                        pyautogui.rightClick()
                        self.last_right = time.time()

                # SCROLL MODE
                if fingers == [0, 1, 1, 0, 0]:

                    pyautogui.scroll(
                        int((240 - index_y) / 10)
                    )

                # DRAG MODE
                if fingers == [0, 0, 0, 0, 0]:

                    pyautogui.mouseDown()

                else:
                    pyautogui.mouseUp()

            cv2.imshow(
                "Atlas Hand Mouse",
                img
            )

            if cv2.waitKey(1) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


def start():
    HandMouseController().run()


if __name__ == "__main__":
    start()