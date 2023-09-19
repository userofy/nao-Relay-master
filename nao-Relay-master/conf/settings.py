# -*- encoding: UTF-8 -*-
"""
配置文件 机器人ip、运动参数等都写在这里
"""

robot1_conf = {                                         # 1号机器人参数
    'basic_param': {                                    # 基础参数
        'ip': '192.168.251.122',
        'port': 9559,
    },
        'motion_param': {                                   # 运动参数
        'forward': {                                    # 前进
            'x': 1,
            'y': -0.01,
            'theta': -0.0533,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.02],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'left': {                                       # 左转
            'x': 1,
            'y': 0.02,
            'theta': -0.03,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.03],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'right': {                                      # 右转
            'x': 1,
            'y': -0.01,
            'theta': -0.08,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.03],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'final': {                                      # 右转
            'x': 1,
            'y': 0,
            'theta': 0.06,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.4],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.03],
                ["StepHeight", 0.02],
                ["TorsoWx", 0],
                ["TorsoWy", 0]
            ]
        }
    },
    'tcp': {
        'host': '127.0.0.1',
        'port': 50007
    }
}
robot2_conf ={   # 基础参数

    'basic_param': {                                    # 基础参数
        'ip': '192.168.251.122',
        'port': 9559,
    },
        'motion_param': {                                   # 运动参数
        'forward': {                                    # 前进
            'x': 1,
            'y': 0.01,
            'theta': 0.0433,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.02],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'left': {                                       # 左转
            'x': 1,
            'y': 0,
            'theta': 0.0633,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.03],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'right': {                                      # 右转
            'x': 1,
            'y': -0.01,
            'theta': -0.01,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.3],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.02],
                ["StepHeight", 0.013],
                ["TorsoWx", 0.01],
                ["TorsoWy", 0.01]
            ]
        },
        'final': {                                      # 右转
            'x': 1,
            'y': 0,
            'theta': 0.0433,
            'config': [
                ["MaxStepFrequency", 3],
                ["MaxStepTheta", 0.4],
                ["MaxStepX", 0.06],
                ["MaxStepY", 0.02],
                ["StepHeight", 0.02],
                ["TorsoWx", 0],
                ["TorsoWy", 0]
            ]
        }
    },
    'tcp': {
        'host': '127.0.0.1',
        'port': 50007
    }
}
