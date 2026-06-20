import cv2
import time
import datetime

from modules.voice import speak


class FaceMonitor:

    def __init__(self):

        self.running = False

        self.user_present = False

        self.last_seen = 0

        self.absence_threshold = 10

        print("[VISION] Loading OpenCV Face Detector...")

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        print("[VISION] Face detector loaded.")

    def greet(self):

        hour = datetime.datetime.now().hour

        if hour < 12:
            speak("Good morning sir. Welcome back.")
        elif hour < 18:
            speak("Good afternoon sir. Welcome back.")
        else:
            speak("Good evening sir. Welcome back.")

    def start(self):

        self.running = True

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            print("[VISION] Camera not detected.")
            return

        print("[VISION] Face monitor online.")

        while self.running:

            success, frame = camera.read()

            if not success:
                continue

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            detected = len(faces) > 0

            if detected:

                for (x, y, w, h) in faces:

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                if not self.user_present:

                    if (
                        time.time() - self.last_seen
                        > self.absence_threshold
                    ):

                        print(
                            "[VISION] Face detected."
                        )

                        self.greet()

                self.user_present = True

                self.last_seen = time.time()

            else:

                if self.user_present:

                    print(
                        "[VISION] Face left scene."
                    )

                self.user_present = False

            cv2.imshow(
                "ATLAS Vision",
                frame
            )

            if cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()

        cv2.destroyAllWindows()

    def stop(self):

        self.running = False