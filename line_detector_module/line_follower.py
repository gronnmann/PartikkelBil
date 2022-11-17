import cv2
import numpy as np
import cv_display_pusher
import os
import RPi.GPIO as gpio
import time

video = cv2.VideoCapture(0)
detection_offset = 100

servo_forward_left = 17
servo_forward_right = 27
servo_back_left = 22
servo_back_right = 26

gpio.setmode(gpio.BCM)

gpio.setup(servo_forward_left, gpio.OUT)
gpio.setup(servo_forward_right, gpio.OUT)
gpio.setup(servo_back_left, gpio.OUT)
gpio.setup(servo_back_right, gpio.OUT)

# Drive modes 0 -
class DriveMode:
    STATIC = 0
    CENTER = 1
    LEFT = 2
    RIGHT = 3


mode = DriveMode.STATIC

while True:

    ret, img = video.read()

    override = False
    if os.path.exists("override.txt"):
        with open("override.txt") as over_f:
            override_line = over_f.readline().strip()
            override = True if override_line == "True" else False

    dimensions = img.shape
    w, h = dimensions[1], dimensions[0]

    # boundaries for commands
    boundaries = ((w // 2) - detection_offset, (w // 2) + detection_offset)

    preview = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    (threshold, thresholded_img) = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    thresholded_img = cv2.erode(thresholded_img, None, iterations=3)

    thresholded_img = 255 - thresholded_img

    contours, hierarchy = cv2.findContours(thresholded_img, 1, cv2.CHAIN_APPROX_NONE)

    # preview shit
    #preview = cv2.cvtColor(thresholded_img, cv2.COLOR_GRAY2BGR)
    preview_line_thickness = 1

    # text_scanning_dots = "." * (j % 4)
    # text_scanning = f"Scanning area{text_scanning_dots}"
    # cv2.putText(preview, text_scanning, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), preview_line_thickness)

    #cv2.drawContours(preview, contours, -1, (0, 255, 0), preview_line_thickness)

    # show offset lines
    cv2.line(preview, (boundaries[0], 0), (boundaries[0], h), (255, 255, 255), preview_line_thickness)
    cv2.line(preview, (boundaries[1], 0), (boundaries[1], h), (255, 255, 255), preview_line_thickness)

    #show current status
    drive_status = "Standing still"
    if override:
        drive_status = "Override"
    else:
        if mode == DriveMode.CENTER:
            drive_status = "Forward"
            gpio.output(servo_forward_left, True)
            gpio.output(servo_forward_right, True)
            gpio.output(servo_back_left, True)
            gpio.output(servo_back_right, True)
        elif mode == DriveMode.LEFT:
            drive_status = "Going left"
            gpio.output(servo_forward_left, True)
            gpio.output(servo_forward_right, False)
            gpio.output(servo_back_left, True)
            gpio.output(servo_back_right, False)
        elif mode == DriveMode.RIGHT:
            drive_status = "Going right"
            gpio.output(servo_forward_left, False)
            gpio.output(servo_forward_right, True)
            gpio.output(servo_back_left, False)
            gpio.output(servo_back_right, True)
        elif mode == DriveMode.STATIC:
            gpio.output(servo_forward_left, False)
            gpio.output(servo_forward_right, False)
            gpio.output(servo_back_left, False)
            gpio.output(servo_back_right, False)
    cv2.putText(preview, drive_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), preview_line_thickness)


    if len(contours) > 0:
        biggest_contour = max(contours, key=cv2.contourArea)

        c_x, c_y, c_w, c_h = cv2.boundingRect(biggest_contour)

        # draw biggest in different color
        cv2.rectangle(preview, (c_x, c_y), (c_x + c_w, c_y + c_h), (0, 0, 255), preview_line_thickness)

        moments = cv2.moments(biggest_contour)

        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        rotated_rect = cv2.minAreaRect(biggest_contour)
        rotated_rect_as_box = cv2.boxPoints(rotated_rect)
        rotated_rect_as_box = np.int0(rotated_rect_as_box)

        cv2.line(preview, (cx, 0), (cx, h), (255, 0, 0), preview_line_thickness)


        if override:
            mode = DriveMode.STATIC
        else:
            if cx < boundaries[0]:
                mode = DriveMode.RIGHT
            elif cx > boundaries[1]:
                mode = DriveMode.LEFT
            else:
                mode = DriveMode.CENTER

        rotation = rotated_rect[2]

        cv2.drawContours(preview, [rotated_rect_as_box], 0, (0, 255, 255), 2)

        # eitlanna_punkt = rotated_rect[1]
        # cv2.circle(preview, eitlanna_punkt, 5, (255, 0, 0), preview_line_thickness)

        # cv2.line(preview, (cx, 0), (cx, h), (255, 0, 0), preview_line_thickness)
        # cv2.line(preview, (0, cy), (w, cy), (255, 0, 0), preview_line_thickness)



    cv_display_pusher.push_stream(preview)
    cv2.imshow("Video preview", preview)

    time.sleep(0.5)
    gpio.output(servo_forward_left, False)
    gpio.output(servo_forward_right, False)
    gpio.output(servo_back_left, False)
    gpio.output(servo_back_right, False)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

video.release()
cv2.destroyAllWindows()
