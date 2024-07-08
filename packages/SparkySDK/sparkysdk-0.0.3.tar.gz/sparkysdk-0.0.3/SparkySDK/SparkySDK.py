import time
import websocket
import json
import threading
import numpy as np

MODE_CTRL, MODE_TEACH, MODE_EDIT, MODE_WAVE = "Remote_Control_Mode", "Teach_Mode", "Edit_Mode", "WAVE_Mode"
PARM_TYPE_HEAD, PARM_TYPE_FRONTLEFT, PARM_TYPE_FRONTRIGHT, PARM_TYPE_BACKLEFT, PARM_TYPE_BACKRIGHT = "AIA_Head", \
                                                                                                     "AIA_FrontLeft", "AIA_FrontRight", "AIA_BackLeft", "AIA_BackRight "
PARM_VALUE_ENABLE, PARM_VALUE_DISABLE, PARM_VALUE_LIMIT, PARM_VALUE_UNLIMIT = "Enable", "Disable", "Limit", "UnLimit"


class RobotControl(threading.Thread):

    def __enter__(self):
        t = time.time()
        while time.time() - t < 3:
            if self.state:
                return self
        raise TimeoutError('connect timeout')

    def __init__(self, ip, getInterval=0.001):
        super().__init__()
        self.ip = ip
        self.msgCallback = []
        self.errCallback = []
        self.clsCallback = []
        self.openCallback = []
        self.modObj = None
        # self.loopstate = True
        self.state = False
        self.interval = getInterval
        # ws://{self.ip}:10710/getjson
        self.ws = websocket.WebSocketApp(f'ws://{self.ip}:10710/getjson',
                                         on_message=self.on_message, on_open=self.on_open,
                                         on_error=self.on_error, on_close=self.on_close)
        # self.ws = websocket.WebSocket()
        # self.ws.connect(f"ws://{self.ip}:10710/getjson")
        self.start()

    def run(self):
        self.ws.run_forever(reconnect=3)
        # while self.loopstate:
        #     data = self.ws.recv()
        #     if self.msgCallback:
        #         for call in self.msgCallback:
        #             call(self, self.ws, data)
        #     time.sleep(self.interval)

    def on_message(self, ws, message):
        if self.msgCallback:
            for call in self.msgCallback:
                call(self, message)

    def on_error(self, ws, error):
        if self.errCallback:
            for call in self.errCallback:
                call(self, error)

    def on_close(self, ws, close_status_code, close_msg):
        if self.clsCallback:
            for call in self.clsCallback:
                call(self, close_msg)

    def on_open(self, ws):
        self.state = True
        if self.openCallback:
            for call in self.openCallback:
                call(self)

    def close(self):
        if self.modObj:
            self.modObj.close()

        self.reset()
        # self.loopstate = False
        self.ws.keep_running = False
        self.join()
        self.ws.close()

    def add_message_callback(self, function):
        self.msgCallback.append(function)

    def del_message_callback(self, function=None):
        self.msgCallback.remove(function) if function else self.msgCallback.pop()

    def add_error_callback(self, function):
        self.errCallback.append(function)

    def del_error_callback(self, function=None):
        self.errCallback.remove(function) if function else self.errCallback.pop()

    def add_close_callback(self, function):
        self.clsCallback.append(function)

    def del_close_callback(self, function=None):
        self.clsCallback.remove(function) if function else self.clsCallback.pop()

    def add_connected_callback(self, function):
        self.openCallback.append(function)

    def del_connected_callback(self, function=None):
        self.openCallback.remove(function) if function else self.openCallback.pop()

    def switch_mode(self, target):
        if target == MODE_WAVE:
            self.ws.send('{"cmd": "Mode_Switch", "target": "' + MODE_EDIT + '"}')
        else:
            self.ws.send('{"cmd": "Mode_Switch", "target": "' + target + '"}')
        self.reset()
        if self.modObj:
            self.modObj.close()
        if target == MODE_CTRL:
            self.modObj = CtrlMode(self)
        elif target == MODE_TEACH:
            self.modObj = TeachMode(self)
        elif target == MODE_EDIT:
            self.modObj = EditMode(self)
        elif target == MODE_WAVE:
            self.modObj = WaveMode(self)
        return self.modObj

    def reset(self):
        self.ws.send('{"cmd":"Reset_Robot_Position"}')

    def get_status(self):
        self.ws.send('{"cmd":"Get_Status"}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class TeachMode:
    def __init__(self, robotControl):
        self.RobotControl = robotControl
        self.RobotControl.add_message_callback(self.recordMsg)
        self.recordState = False
        self.save_path = None
        self.recordJson = []
        self.playJson = []
        self.closeState = False

    def close(self):
        self.closeState = True
        self.RobotControl.del_message_callback(self.recordMsg)

    def recordMsg(self, super, message):
        if self.recordState and 'AIA' in message:
            if self.save_path:
                with open(self.save_path, 'a', encoding='utf-8') as f:
                    f.write(message + '\n')
                    f.flush()
            else:
                self.recordJson.append(message)

    def start_record(self, save_path=None):
        if self.recordState:
            return
        self.recordState = True
        self.recordJson = []
        self.save_path = save_path
        self.RobotControl.ws.send('{"cmd":"Start_Record"}')

    def stop_record(self):
        if not self.recordState:
            return
        self.recordState = False
        self.RobotControl.ws.send('{"cmd":"Stop_Record"}')

    def start_play(self, play_path=None):
        self.playJson = []
        if not play_path:
            for Json in self.recordJson:
                a = Json.replace('"feedback":"Recording"', '"cmd":"Playing"')
                self.playJson.append(a)
        else:
            with open(play_path) as file:
                lines = file.readlines()
            for line in lines:
                a = line.replace('"feedback":"Recording"', '"cmd":"Playing"')
                self.playJson.append(a)
        self.RobotControl.ws.send('{"cmd":"Start_Play"}')
        threading.Thread(target=self.sendKeyframe).start()

    def sendKeyframe(self):
        for Keyframe in self.playJson:
            if self.closeState:
                break
            self.RobotControl.ws.send(Keyframe)
            time.sleep(0.01)

    def set_parameter(self, type, value):
        self.RobotControl.ws.send(
            '{"cmd": "Set_Parameter", "type": "' + type + '", "parameter": "Output_Torque", "value": "' + value + '"}')


class CtrlMode:
    def __init__(self, robotControl):
        self.RobotControl = robotControl
        self.movex = 0
        self.movey = 0
        self.movew = 0
        self.moveh = 0
        self.tranx = 0
        self.trany = 0
        self.tranz = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.headpitch = 0
        self.headyaw = 0
        self.speed = 'fast'

    def close(self):
        self.movex = 0
        self.movey = 0
        self.movew = 0
        self.moveh = 0
        self.tranx = 0
        self.trany = 0
        self.tranz = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.headpitch = 0
        self.headyaw = 0
        self.speed = 'fast'
        self.sync()

    def sync(self):
        data = {
            "cmd": "Control_Move",
            "movex": self.movex,
            "movey": self.movey,
            "movew": self.movew,
            "moveh": self.moveh,
            "tranx": self.tranx,
            "trany": self.trany,
            "tranz": self.tranz,
            "roll": self.roll,
            "pitch": self.pitch,
            "yaw": self.yaw,
            "headpitch": self.headpitch,
            "headyaw": self.headyaw,
            "speed": self.speed
        }
        # print(data)
        self.RobotControl.ws.send(json.dumps(data))


class EditMode(threading.Thread):
    def __init__(self, robotControl, sendInterval=0.1):
        super().__init__()
        self.RobotControl = robotControl
        self.pitch = 0
        self.roll = 0
        self.tran_x = 0
        self.tran_y = 0
        self.tran_z = 141
        self.yaw = 0.0
        self.pitch_head = 0.0
        self.yaw_head = 0.0

        self.front_left_leg_x = 75
        self.front_left_leg_y = 55
        self.front_left_leg_z = 0
        self.front_right_leg_x = 75
        self.front_right_leg_y = -55
        self.front_right_leg_z = 0
        self.back_left_leg_x = -75
        self.back_left_leg_y = 55
        self.back_left_leg_z = 0
        self.back_right_leg_x = -75
        self.back_right_leg_y = -55
        self.back_right_leg_z = 0

        self.acc = 'Slowest'
        self.speed = 'Slowest'
        self.loopstate = True
        self.interval = sendInterval
        self.start()

    def run(self):
        while self.loopstate:
            self.send()
            time.sleep(self.interval)

    def close(self):
        self.loopstate = False
        self.join()

    def reset(self):
        self.pitch = 0
        self.roll = 0
        self.tran_x = 0
        self.tran_y = 0
        self.tran_z = 141
        self.yaw = 0.0
        self.pitch_head = 0.0
        self.yaw_head = 0.0

        self.front_left_leg_x = 75
        self.front_left_leg_y = 55
        self.front_left_leg_z = 0
        self.front_right_leg_x = 75
        self.front_right_leg_y = -55
        self.front_right_leg_z = 0
        self.back_left_leg_x = -75
        self.back_left_leg_y = 55
        self.back_left_leg_z = 0
        self.back_right_leg_x = -75
        self.back_right_leg_y = -55
        self.back_right_leg_z = 0

        self.acc = 'Slowest'
        self.speed = 'Slowest'
        self.RobotControl.ws.send('{"cmd":"Reset_Robot_Position"}')

    def form(self):
        data = {
            "cmd": "Play_Keyframe",
            "acc": self.acc,
            "speed": self.speed,
            "time": 10,  # GUI演示用时间固定为10ms
            "Body": {
                "pitch": self.pitch,
                "roll": self.roll,
                "tran_x": self.tran_x,
                "tran_y": self.tran_y,
                "tran_z": self.tran_z,
                "yaw": self.yaw
            },
            "FootPoint": {
                "FrontLeftLeg": {
                    "x": self.front_left_leg_x,
                    "y": self.front_left_leg_y,
                    "z": self.front_left_leg_z
                },
                "FrontRightLeg": {
                    "x": self.front_right_leg_x,
                    "y": self.front_right_leg_y,
                    "z": self.front_right_leg_z
                },
                "BackLeftLeg": {
                    "x": self.back_left_leg_x,
                    "y": self.back_left_leg_y,
                    "z": self.back_left_leg_z
                },
                "BackRightLeg": {
                    "x": self.back_right_leg_x,
                    "y": self.back_right_leg_y,
                    "z": self.back_right_leg_z
                }
            },
            "Head": {
                "pitch": self.pitch_head,
                "yaw": self.yaw_head
            }
        }
        return data

    def set_parameter(self, type, value):
        self.RobotControl.ws.send(
            '{"cmd": "Set_Parameter", "type": "' + type + '", "parameter": "Output_Torque", "value": "' + value + '"}')

    def send(self):
        data = json.dumps(self.form())
        self.RobotControl.ws.send(data)
        print(data)

    def save(self, path='keyframe.txt', index=None):
        if not index:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(self.form()) + '\n')
                f.flush()
        else:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines[index] = data + '\n'
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

    def read(self, path='keyframe.txt', index=0):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        data = json.loads(lines[index])
        self.pitch = data['Body']['pitch']
        self.roll = data['Body']['roll']
        self.tran_x = data['Body']['tran_x']
        self.tran_y = data['Body']['tran_y']
        self.tran_z = data['Body']['tran_z']
        self.yaw = data['Body']['yaw']
        self.pitch_head = data['Head']['pitch']
        self.yaw_head = data['Head']['yaw']
        self.front_left_leg_x = data['FootPoint']['FrontLeftLeg']['x']
        self.front_left_leg_y = data['FootPoint']['FrontLeftLeg']['y']
        self.front_left_leg_z = data['FootPoint']['FrontLeftLeg']['z']
        self.front_right_leg_x = data['FootPoint']['FrontRightLeg']['x']
        self.front_right_leg_y = data['FootPoint']['FrontRightLeg']['y']
        self.front_right_leg_z = data['FootPoint']['FrontRightLeg']['z']
        self.back_left_leg_x = data['FootPoint']['BackLeftLeg']['x']
        self.back_left_leg_y = data['FootPoint']['BackLeftLeg']['y']
        self.back_left_leg_z = data['FootPoint']['BackLeftLeg']['z']
        self.back_right_leg_x = data['FootPoint']['BackRightLeg']['x']
        self.back_right_leg_y = data['FootPoint']['BackRightLeg']['y']
        self.back_right_leg_z = data['FootPoint']['BackRightLeg']['z']
        self.time = data['time']
        self.acc = data['acc']
        self.speed = data['speed']


class WaveMode(EditMode):
    def __init__(self, robotControl):
        threading.Thread.__init__(self)
        self.RobotControl = robotControl
        self.pitch = 0
        self.roll = 0
        self.tran_x = -20
        self.tran_y = 0
        self.tran_z = 140
        self.yaw = 0.0
        self.pitch_head = 0.0
        self.yaw_head = 0.0

        self.front_left_leg_x = 75
        self.front_left_leg_y = 55
        self.front_left_leg_z = 0
        self.front_right_leg_x = 75
        self.front_right_leg_y = -55
        self.front_right_leg_z = 0
        self.back_left_leg_x = -75
        self.back_left_leg_y = 55
        self.back_left_leg_z = 0
        self.back_right_leg_x = -75
        self.back_right_leg_y = -55
        self.back_right_leg_z = 0

        self.acc = 'Fastest'
        self.speed = 'Fastest'
        # 控制全局bpm 默认下每分钟60个节拍
        self.bpm = 60
        # 控制波形类型
        self.wave_mode = 1  # 1: 正弦波, 2: 方波, 3: S型曲线
        # 正半周期占整个周期的比例，0 < ratio <= 1
        self.positive_ratio = 0.1  # 例如，0.75表示正半周期占整个周期的75%

        self.amplitude_1 = 0.5
        self.frequency_1 = 1.0

        self.amplitude_2 = 0.5
        self.frequency_2 = 1.0

        self.amplitude_3 = 0.5
        self.frequency_3 = 1.0

        self.phase_1 = 0
        self.phase_2 = 0
        self.phase_3 = 0

        self.init_time = time.time()
        self.last_time = 0

        self.loopstate = True
        self.start()

    def run(self):
        while self.loopstate:
            self.updata()
            time.sleep(0.004)

    def updata(self):

        if time.time() - self.last_time < 0.01:
            return

        self.last_time = time.time()
        timestep = time.time() - self.init_time

        # 运行震荡周期
        time_ratio = self.bpm / 60
        # 计算周期和正半周期的持续时间
        period = 1 / (self.frequency_1 * time_ratio)
        positive_duration = period * self.positive_ratio
        y_1 = 0
        if timestep > period:
            timestep = timestep % period  # 运行时间对运行周期取余
        if timestep < positive_duration:
            if self.wave_mode == 1:  # 计算方波对应的y值
                y_1 = self.amplitude_1
            if self.wave_mode == 2:  # 计算正弦波对应的y值
                y_1 = self.amplitude_1 * np.sin(2 * np.pi * self.frequency_1 * time_ratio * timestep + self.phase_1)
            if self.wave_mode == 3:  # 计算三角波对应的y值
                y_1 = 0.5 * timestep * self.amplitude_1

        y_2 = self.amplitude_2 * np.sin(2 * np.pi * self.frequency_2 * time_ratio * timestep + self.phase_2)  # 计算对应的y值
        y_3 = self.amplitude_3 * np.sin(2 * np.pi * self.frequency_3 * time_ratio * timestep + self.phase_3)  # 计算对应的y值

        # 发送数据到websocket服务器
        # pitch的范围是-1~1，需要进行映射
        self.yaw = y_2 / 5
        self.pitch = y_3 / 5

        self.yaw_head = - y_2 / 3
        self.pitch_head = y_1 / 3

        self.tran_z = y_1 * 20 + 140

        self.send()
