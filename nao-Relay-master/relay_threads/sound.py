# coding=utf-8
import time


from naoqi import ALProxy

class Audio():

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
    def whs_thd(self):


        # 启动声音检测

        # 循环获取音频数据
        count = 0
        while True:
            sound_proxy = ALProxy("ALSoundDetection", self.IP, self.PORT)
            m = ALProxy("ALMemory", self.IP, self.PORT)
            sound_proxy.setParameter("Sensibility", 0.7)
            sound_proxy.subscribe("SoundDetected")
            time.sleep(0.1)
            if count == 0:
                m.raiseEvent("SoundDetected", None)
                count += 1
                print "已清空"
            sound_val = m.getData("SoundDetected")
            print("听哨声系统准备完毕")
            print '获取哨声强度'
            try:
                print sound_val
                if sound_val[-1][0] > 5000:
                    sound_proxy.unsubscribe("SoundDetected")
                    return True
            except Exception, e:
                print "听哨模块异常，错误为：", e
            sound_proxy.unsubscribe("SoundDetected")







