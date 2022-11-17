import cv2, pickle, socket, os

# https://medium.com/nerd-for-tech/live-streaming-using-opencv-c0ef28a5e497

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = "0.0.0.0"
server_port = 6655

print(f"Binding server at {server_ip}:{server_port}")

s.bind((server_ip, server_port))

override = False

while True:
    read_socket = s.recvfrom(1000000)

    pusher_ip = read_socket[1][0]
    img_data_raw = read_socket[0]

    img_data = pickle.loads(img_data_raw)

    #print(f"Received data from {pusher_ip}: {img_data}")



    img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    cv2.imshow("DroneDisplay", img)

    key = cv2.waitKey(1)

    #print(f"Key pressed: {key}")

    if key == ord(" "):
        override = not override
        print(f"Override toggled: {override}")

        with open("override.txt", "w") as override_file:
            override_file.write(str(override))

    if override:
        if key == ord("w"):
            print("Override FORWARD")
        elif key == ord("s"):
            print("Override BACKWARD")
        elif key == ord("a"):
            print("Override LEFT")
        elif key == ord("d"):
            print("Override RIGHT")

    if key == ord("q"):
        break


cv2.destroyAllWindows()


