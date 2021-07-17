import mediapipe as mp
import cv2
import numpy as np


class Detector:
    def __init__(self, camera_number):
        self.__cap = cv2.VideoCapture(camera_number)
        self.__frame = None
        self.__drawed_frame = None

        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_hands = mp.solutions.hands
        self.__hands = self.__mp_hands.Hands(max_num_hands=1,
                                             min_detection_confidence=0.7,
                                             min_tracking_confidence=0.5)
        
        self.__detected = False
        self.__hand_result = []
        self.__face_result = None
        self.__finger_result = {}
        self.__finger_names = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'PINKY']
        self.__send_finger = None
        self.__send_face = None
        self.__threshold = 50
        self.__resized_x = 640
        self.__resized_y = 640
        self.__cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def __calc_hand_status(self):
        # draw hand landmarks, and get coordinates of landmarks
        process_frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB)
        process_frame.flags.writeable = False
        process_result = self.__hands.process(process_frame)

        if process_result.multi_hand_landmarks:
            # only if detected
            self.__detected = True
            self.__frame.flags.writeable = True
            for hand_landmarks in process_result.multi_hand_landmarks:
                self.__mp_drawing.draw_landmarks(self.__frame, hand_landmarks, self.__mp_hands.HAND_CONNECTIONS)
                # draw landmarks on show frame
                self.__hand_result.clear()
                self.__hand_result.append(hand_landmarks.landmark)
                # append result to list
            # self.__hand_result = process_result
        else:
            self.__detected = False

    def __calc_face_status(self):
        grayed_frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2GRAY)
        face_rect = self.__cascade.detectMultiScale(grayed_frame)
        for x, y, w, h in face_rect:
            cv2.rectangle(self.__frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            center_x = x + (w / 2)
            center_y = y + (h / 2)
            print(center_x / self.__resized_x, center_y / self.__resized_y)
            self.__send_face = [center_x, center_y]

    def __calc_finger_status(self):
        for hand in self.__hand_result:
            # loop in each hand
            # for counter in range(len(self.__finger_names)):
            for counter, name in enumerate(self.__finger_names):
                lower = hand[4 * counter + 1]
                upper = hand[4 * counter + 4]
                origin = hand[0]

                lower_vec = np.array([lower.x, lower.y, lower.z]) - np.array([origin.x, origin.y, origin.z])
                # upper_vec = np.array([lower.x, lower.y, lower.z]) - np.array([upper.x, upper.y, upper.z])
                upper_vec = np.array([upper.x, upper.y, upper.z]) - np.array([lower.x, lower.y, lower.z])

                lower_abs = np.linalg.norm(lower_vec)
                upper_abs = np.linalg.norm(upper_vec)

                dot = np.inner(lower_vec, upper_vec)
                rad = np.arccos(dot / (lower_abs * upper_abs))
                theta = np.rad2deg(rad)
                self.__finger_result[name] = theta
                # add deg to dict obj key is each finger's name

    def __convert_finger_status(self):
        if self.detected:
            self.__send_finger = ''
            # initialize send string
            for number, finger_name in enumerate(self.__finger_names):
                if self.__finger_result[finger_name] < self.__threshold:
                    # if finger turned add string the number
                    # eg. 01234 means all fingers are turned
                    self.__send_finger += str(number)
            print(self.__send_finger)

    def __resize_window(self):
        self.__frame = cv2.resize(self.__frame, (self.__resized_x, self.__resized_y))

    def DetectProcess(self):
        _, self.__frame = self.__cap.read()
        self.__calc_hand_status()
        self.__calc_finger_status()
        # self.__calc_face_status()
        self.__convert_finger_status()
        self.__resize_window()
    # public method

    @property
    def detected(self):
        return self.__detected

    @property
    def frame(self):
        return self.__frame

    @property
    def drawed_frame(self):
        return self.__drawed_frame

    @property
    def hand_status(self):
        return self.__hand_result

    @property
    def face_status(self):
        return self.__face_result

    @property
    def send_finger(self):
        return self.__send_finger

    @property
    def send_face(self):
        return self.__send_face


if __name__ == '__main__':
    det = Detector(0)
    while True:
        det.DetectProcess()
        frame = det.frame
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:
            exit()
