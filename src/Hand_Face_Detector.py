import mediapipe as mp
import cv2


class Detector:
    def __init__(self, camera_number):
        self.__cap = cv2.VideoCapture(camera_number)
        self.__frame = None
        self.__drawed_frame = None

        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_hands = mp.solutions.hands
        self.__hands = self.__mp_hands.Hands(max_num_hands=1,
                                             min_detection_confidence=0.5,
                                             min_tracking_confidence=0.5)
        self.__detected = False
        self.__hand_result = []
        self.__face_result = None

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
        pass

    def __calc_finger_status(self):
        pass

    def DetectProcess(self):
        _, self.__frame = self.__cap.read()
        self.__calc_hand_status()
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


if __name__ == '__main__':
    det = Detector(0)
    while True:
        det.DetectProcess()
        frame = det.frame
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:
            exit()
        if det.detected:
            for i in det.hand_status:
                for j in i:
                    print(j)
