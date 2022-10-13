import socket, cv2, pickle, os

# https://medium.com/nerd-for-tech/live-streaming-using-opencv-c0ef28a5e497

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

server_ip = "127.0.0.1"
server_port = 6655

video = cv2.VideoCapture(0)

def push_stream(img):
    ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

    img_bytified = pickle.dumps(buffer)
    s.sendto(img_bytified, (server_ip, server_port))


if __name__ == "__main__":
    while True:
        ret, img = video.read()

        cv2.imshow("Sending to server...", img)


        push_stream(img)

        if cv2.waitKey(10) == 13:
            break

    cv2.destroyAllWindows()

