# coding=utf-8
import random
from threading import Thread
from naoqi import ALProxy
import cv2
import numpy as np
import time
from PIL import Image


def direction_recognition(lines):
    if lines is None:
        cmd = 'forward'
    else:
        line = lines[0]
        print 'line：  ', line
        # for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 == x2:
            cmd = 'forward'
        else:
            slope = (y1 - y2) * 1.0 / (x1 - x2)
            print "slope:", slope
            theta = np.arctan(slope)
            degrees_theta = np.degrees(theta)
            print '弧度制单位：', theta
            print '角度制单位：', degrees_theta
            if -90 <= degrees_theta <= -57 or 50 <= degrees_theta <= 90:
                cmd = 'forward'
            elif 10 <= degrees_theta < 50:
                cmd = 'left'
            elif -57 < degrees_theta <= -10:
                cmd = 'right'
            elif -10 <= degrees_theta <= 10:
                cmd = 'stop'
            else:
                cmd = 'forward'
            print cmd
    return cmd

def draw_lines( lines, image):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("img", image)

# def image_houghlines(img):
#
#     image = np.frombuffer(img[6], dtype=np.uint8)
#     image = image.reshape(img[1], img[0], img[2])
#     grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     # H, S, V = cv2.split(grayimg)
#     lowerGreen = np.array([0, 0, 150])
#     upperGreen = np.array([120, 17, 255])
#     mask = cv2.inRange(grayimg, lowerGreen, upperGreen)
#     greenThings = cv2.bitwise_and(image, image, mask=mask)
#     img = cv2.GaussianBlur(greenThings, (3, 3), 0)
#     imcan = cv2.Canny(img, 50, 150, apertureSize=3)
#     cv2.imshow('sada', imcan)
#
#     # lines = cv2.HoughLines(imcan, 1, np.pi / 180, 150)
#     lines = cv2.HoughLinesP(imcan, 1, np.pi / 180, 50, minLineLength=150, maxLineGap=10)
#     draw_lines(lines, image)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     return lines

def image_houghlines(img):
    print img.shape
    height, width, channels = img.shape
    image = np.frombuffer(img, dtype=np.uint8)
    image = image.reshape(height, width, channels)
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lowerGreen = np.array([0, 0, 150])
    upperGreen = np.array([168, 204, 165])
    mask = cv2.inRange(grayimg, lowerGreen, upperGreen)
    greenThings = cv2.bitwise_and(image, image, mask=mask)
    img = cv2.GaussianBlur(greenThings, (3, 3), 0)
    imcan = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(imcan, 1, np.pi / 180, 50, minLineLength=150, maxLineGap=10)
    return lines


def p2():
    image_path = "d:\\jbw\\e3.jpg"
    image = cv2.imread(image_path)

    image_data = image.tobytes()

    lines = image_houghlines(image)

    direction_recognition(lines)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("Processed Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def p1():
    videoproxy = ALProxy("ALVideoDevice", "192.168.251.91", 9559)

    AL_kTopCamera = 1
    AL_kVGA = 2
    AL_kBGRColorSpace = 11
    Fps = 30
    subscriber = videoproxy.subscribeCamera(
        "demo", AL_kTopCamera, AL_kVGA, AL_kBGRColorSpace, Fps)

    while True:
        imageNAO = videoproxy.getImageRemote(subscriber)

        if imageNAO == None:
            print('cannot capture.')
        elif imageNAO[6] == None:
            print('no image data string.')
        else:
            frameArray = np.frombuffer(imageNAO[6], dtype=np.uint8).reshape(
                [imageNAO[1], imageNAO[0], imageNAO[2]])
            cv2.imshow("pepper-top-camera-320x240", frameArray)

            img= videoproxy.getImageRemote(subscriber)
            img = img.astype(np.uint8)
            lines = image_houghlines(image)
            draw_lines(lines, image)

            imageWidth = image[0]
            imageHeight = image[1]
            array = image[6]
            im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
            im.save("camImage.png", "PNG")
            cv2.imwrite("temp_hd.jpg", img)
            print('save image')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

p2()


