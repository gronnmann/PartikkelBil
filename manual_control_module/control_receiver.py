import socket
import pickle
import RPi.GPIO as gpio

servo_forward_left = 17
servo_forward_right = 27
servo_back_left = 22
servo_back_right = 26


# gpio.setmode(gpio.BCM)
#
# gpio.setup(servo_forward_left, gpio.OUT)
# gpio.setup(servo_forward_right, gpio.OUT)
# gpio.setup(servo_back_left, gpio.OUT)
# gpio.setup(servo_back_right, gpio.OUT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = "0.0.0.0"
server_port = 6655

print(f"Binding server at {server_ip}:{server_port}")

s.bind((server_ip, server_port))

override = False

while True:
    read_socket = s.recvfrom(1000000)
    data_raw = pickle.loads(read_socket[0])


    if data_raw == "FORWARD":
        gpio.output(servo_forward_left, True)
        gpio.output(servo_forward_right, True)
        gpio.output(servo_back_left, True)
        gpio.output(servo_back_right, True)
    elif data_raw == "RIGHT":
        gpio.output(servo_forward_left, True)
        gpio.output(servo_forward_right, False)
        gpio.output(servo_back_left, True)
        gpio.output(servo_back_right, False)
    elif data_raw == "LEFT":
        gpio.output(servo_forward_left, False)
        gpio.output(servo_forward_right, True)
        gpio.output(servo_back_left, False)
        gpio.output(servo_back_right, True)
    else:
        gpio.output(servo_forward_left, False)
        gpio.output(servo_forward_right, False)
        gpio.output(servo_back_left, False)
        gpio.output(servo_back_right, False)
