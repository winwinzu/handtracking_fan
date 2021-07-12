import Hand_Face_Detector as Det
import Send_Data as SD
import cv2
import collections


class Fan_Main:
    def __init__(self):
        self.detector = Det.Detector(0)
        self.server = SD.Server()
        self.stack_finger_value = [0 for i in range(10)]

    def main(self):
        while True:
            self.detector.DetectProcess()
            frame = self.detector.frame
            finger_value = self.detector.send_finger
            send_data = '0:'
            if finger_value == '1':
                send_data = '50:'
            elif finger_value == '12':
                send_data = '100:'
            elif finger_value == '123':
                send_data = '150:'
            self.stack_finger_value.pop(0)
            self.stack_finger_value.append(send_data)
            print(self.stack_finger_value)
            most_common = collections.Counter(self.stack_finger_value)
            most_common_value = most_common.most_common()
            print(most_common_value[0][0])
            self.server.send_data(str(most_common_value[0][0]))
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                self.server.close_port()
                exit()


if __name__ == '__main__':
    main = Fan_Main()
    main.main()
