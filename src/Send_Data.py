import serial


class Server:
    def __init__(self):
        self.__ser = serial.Serial('COM3', 9600)

    def send_data(self, data):
        send_data = data.encode('utf-8')
        self.__ser.write(send_data)

    def close_port(self):
        self.__ser.close()


if __name__ == '__main__':
    server = Server()
    data = input()
    server.send_data(data)
    server.close_port()
