import socket
import cv2
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

server_ip = "172.20.10.5"
server_port = 6655
# 172.20.10.5

img = cv2.imread("background.png")


while True:
    cv2.imshow("Control", img)
    key = cv2.waitKey(1)

    drivingStatus = None

    if key == ord("w"):
        drivingStatus = "FORWARD"
    elif key == ord("s"):
        drivingStatus = "BACK"
    elif key == ord("a"):
        drivingStatus = "LEFT"
    elif key == ord("d"):
        drivingStatus = "RIGHT"
    elif key == ord("q"):
        break

    if drivingStatus is not None:
        toSend = pickle.dumps(drivingStatus)
        s.sendto(toSend, (server_ip, server_port))