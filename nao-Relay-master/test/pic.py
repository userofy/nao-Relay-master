# coding=utf-8
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
        print 'line:  ', line
        # for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 == x2:
            cmd = 'forward'
        else:
            slope = (y1 - y2) * 1.0 / (x1 - x2)
            print "slope:", slope
            theta = np.arctan(slope)
            degrees_theta = np.degrees(theta)
            print '弧度制单位:', theta
            print '角度制单位:', degrees_theta
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


def draw_lines(lines, image):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("img", image)


def image_houghlines(img):
    print img.shape
    height, width, channels = img.shape
    image = np.frombuffer(img, dtype=np.uint8)
    image = image.reshape(height, width, channels)
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lowerGreen = np.array([26, 75, 28])
    # upperGreen = np.array([200, 229, 204])
    lowerGreen = np.array([26, 75, 28])
    upperGreen = np.array([200, 229, 204])
    mask = cv2.inRange(grayimg, lowerGreen, upperGreen)
    greenThings = cv2.bitwise_and(image, image, mask=mask)
    img = cv2.GaussianBlur(greenThings, (3, 3), 0)
    imcan = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(imcan, 1, np.pi / 180, 50, minLineLength=150, maxLineGap=10)
    return lines


def p2():
    # image_path = "../1.png"
    image_path = "../2.png"
    img1 = Image.open(image_path)
    # img = Image.frombytes("RGB", (imageWidth, imageHeight), array)
    cv2_img = cv2.cvtColor(np.asarray(img1), cv2.COLOR_RGB2BGR)

    image = cv2_img
    # image = cv2.imread(image_path)

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


if __name__ == '__main__':
    p2()
