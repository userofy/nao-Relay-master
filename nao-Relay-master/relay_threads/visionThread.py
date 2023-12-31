# -*- encoding: UTF-8 -*-
"""
机器人视觉线程
"""
import random
from threading import Thread
from naoqi import ALProxy
import cv2
import numpy as np
import time
import io
from PIL import Image


class VisionThread(Thread):
    def __init__(self, robot_conf, start_vision_queue, vision_move_queue):
        super(VisionThread, self).__init__()

        self.__robot_conf = robot_conf
        self.__start_vision_queue = start_vision_queue
        self.__vision_move_queue = vision_move_queue

        self.__vision = ALProxy("ALVideoDevice",
                                self.__robot_conf['basic_param']['ip'],
                                self.__robot_conf['basic_param']['port'])

        self.camera_botton = None  # 底部摄像头订阅
        self.init_camera()

    def init_camera(self):
        # 摄像头参数
        cameraName = 'camera' + str(random.randint(0, 100))
        cameraIndex = 1
        resolution = 2
        colorSpace = 11
        fps = 30

        self.camera_botton = self.__vision.subscribeCamera(cameraName,
                                                           cameraIndex,
                                                           resolution,
                                                           colorSpace,
                                                           fps)

    def image_houghlines(self, img):
        # # 转换成numpy数组
        # # image_np = np.array(img, dtype=np.uint8)
        # # img = Image.fromarray(image_np)
        # # stream = io.BytesIO(img)
        # # # 打开图像
        # # img = Image.open(stream)
        # # # 保存为 JPG 格式
        # # img.save('output.jpg')
        # # 保存为 JPG 格式
        # # height, width, channels = img.shape
        # image = np.frombuffer(img[6], dtype=np.uint8)
        # # 切割
        #
        # cv2.imshow('sada_1', image)
        # image = image.reshape(img[1], img[0], img[2])
        # # HSV
        # grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # # 二值化
        # # H, S, V = cv2.split(grayimg)
        # lowerGreen = np.array([0, 0, 150])
        # upperGreen = np.array([120, 17, 255])
        # mask = cv2.inRange(grayimg, lowerGreen, upperGreen)
        # greenThings = cv2.bitwise_and(image, image, mask=mask)
        # # 二值化
        # img = cv2.GaussianBlur(greenThings, (3, 3), 0)
        # imcan = cv2.Canny(img, 50, 150, apertureSize=3)
        # # cv2.imshow('sada', imcan)
        #
        # # 检测霍夫线
        # # lines = cv2.HoughLines(imcan, 1, np.pi / 180, 150)                # 标准霍夫线变换
        # lines = cv2.HoughLinesP(imcan, 1, np.pi / 180, 50, minLineLength=150, maxLineGap=10)  # 统计霍夫变换
        # # self.draw_lines(lines, image)
        # # cv2.waitKey(0)
        # # cv2.destroyAllWindows()

        print img.shape
        height, width, channels = img.shape
        image = np.frombuffer(img, dtype=np.uint8)
        image = image.reshape(height, width, channels)
        grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lowerGreen = np.array([26, 75, 28])
        upperGreen = np.array([200, 229, 204])
        mask = cv2.inRange(grayimg, lowerGreen, upperGreen)
        greenThings = cv2.bitwise_and(image, image, mask=mask)
        img = cv2.GaussianBlur(greenThings, (3, 3), 0)
        imcan = cv2.Canny(img, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(imcan, 1, np.pi / 180, 50, minLineLength=150, maxLineGap=10)
        print lines
        return lines

    def direction_recognition(self, lines):
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
                if -90 <= degrees_theta <= -67 or 60 <= degrees_theta <= 90:
                    cmd = 'forward'
                elif 20 <= degrees_theta < 60:
                    cmd = 'left'
                elif -67 < degrees_theta <= -20:
                    cmd = 'right'
                elif -20 <= degrees_theta <= 20:
                    cmd = 'stop'
                else:
                    cmd = 'forward'
        return cmd

    def draw_lines(self, lines, image):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow("img", image)

    def run(self):
        while True:


            # 设置一个等待时间，以便头部保持低头的姿势


            # 等待一段时间，使头部保持低头的姿势

            if not self.__start_vision_queue.empty():
                msg = self.__start_vision_queue.get()
                if msg == 'start':
                    print 'vision_queue_msg :', msg
                    break

        while True:
            time.sleep(1)
            image = self.__vision.getImageRemote(self.camera_botton)
            # image_path = "d:\\jbw\\e3.jpg"
            # image = cv2.imread(image_path)
            # Get the image size and pixel array.
            imageWidth = image[0]
            imageHeight = image[1]
            array = image[6]

            # Create a PIL Image from our pixel array.
            img = Image.frombytes("RGB", (imageWidth, imageHeight), array)
            # cv2_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            # # Save the image.
            img.save("./camImage.jpg", "JPEG")
            time.sleep(0.5)
            image = cv2.imread('./camImage.jpg')

            lines = self.image_houghlines(image)
            cmd = self.direction_recognition(lines)
            # 队列里只放一条指令，减少延时指令的堆积
            if self.__vision_move_queue.qsize() == 1:
                self.__vision_move_queue.get()
                self.__vision_move_queue.put(cmd)
            else:
                self.__vision_move_queue.put(cmd)
            print 'cmd', cmd

            # 判断停止后，断开摄像头订阅
            if cmd == 'stop':
                self.__vision.unsubscribe(self.camera_botton)
                break


if __name__ == '__main__':
    pass
    # from conf import robot1_conf
    # from Queue import Queue
    #
    # queue1 = Queue()
    # queue2 = Queue()
    # core = ALProxy("ALAutonomousLife", "192.168.43.250", 9559)
    # if core.getState() != "disabled":
    #     core.setState("disabled")
    # vision = VisionThread(robot1_conf, queue1, queue2)
    # vision.start()
    # vision.join()
