# -*- encoding: UTF-8 -*-
"""
1号机器人等待出发的线程
"""
from threading import Thread
from naoqi import ALProxy
from sound import Audio


class RobOneStartThread(Thread):
    def __init__(self, robot_conf, start_move_queue, start_vision_queue):
        super(RobOneStartThread, self).__init__()

        self.__robot_conf = robot_conf
        self.__start_move_queue = start_move_queue
        self.__start_vision_queue = start_vision_queue

        self.__touch = ALProxy("ALTouch",
                               self.__robot_conf['basic_param']['ip'],
                               self.__robot_conf['basic_param']['port'])

    def run(self):
        aud = Audio(self.__robot_conf['basic_param']['ip'],
                    self.__robot_conf['basic_param']['port'])

        flog = 0
        while True:
            status = self.__touch.getStatus()
            for e in status:
                if e[0] == 'Head' and e[1]:
                    self.__start_move_queue.put('start')
                    if flog == 0:
                        flog = 1
                        aud.whs_thd()
                    self.__start_vision_queue.put('start')

                    break

