from naoqi import ALProxy
from threading import Thread

import time


class Heading(Thread):

    def __init__(self, robot_conf):
        super(Heading, self).__init__()
        self.__robot_conf = robot_conf

        self.head_pitch_angle = 0.4
        self.duration = 1

    def run(self):
        motion_proxy = ALProxy(("ALVideoDevice",
                                self.__robot_conf['basic_param']['ip'],
                                self.__robot_conf['basic_param']['port']))
        motion_proxy.setAngles("HeadPitch", self.head_pitch_angle, 0.2)
        while abs(motion_proxy.getAngles("HeadPitch", True)[0] - self.head_pitch_angle) > 0.01:
            pass
        time.sleep(self.duration)
