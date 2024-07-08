**python** **二次开发指南**

**一、前言**

此文档介绍了如何通过python sdk 操作哮天。您可以按照我们提供的接口和例程，学习机器人控制，完成哮天的二次开发。在阅读本文档前，请先阅读以下文档，对哮天有一定了解。

[240623_SPARKY 开箱指南](https://wsvrat1klt.feishu.cn/docx/UlIzdMlV9oxy5txKCIJcJJm2nVe) 

**二、准备工作**

**2.1** **硬件**

•     准备一只更新至最新镜像哮天

**2.2** **软件**

•     使用环境

￮    哮天：与电脑连接同一局域网，从屏幕上获取 IP 地址

￮    PC端：已安装 Python 环境，并且使用以下指令获取 python sdk

```
pip install SparkySdk
```

**三、使用人群**

•     想要了解与学习python开发的学生、爱好者、创客等。

•     想要使用python二次开发哮天的学生、爱好者、创客等。

**四、建议具备背景知识**

•     有过 Python 语言编程基础，了解基本语法，如面向对象、交互解释等概念。

•     对哮天情况有所了解，能够使用app控制哮天。

**五、上手运行程序**

**5.1** **测试程序**

演示使用 SparkySdk 获取哮天信息

```python
# 导入 SparkySdk
import SparkySdk
# 定义一个消息回调函数
def msgCallback(self, ws, message):
    print(message)
# 通过 ip 连接上哮天
with SparkySdk.RobotControl('192.168.8.212') as robot:
    # 添加消息回调函数
    robot.add_message_callback(msgCallback)
    # 获取哮天信息
    robot.get_status()
    input('回车退出程序，哮天将恢复默认状态')
```

演示使用 SparkySdk 进入遥控模式，并控制哮天全速前进

```python
# 导入 SparkySdk
import SparkySdk
# 定义一个消息回调函数
def msgCallback(self, ws, message):
    print(message)
# 通过 ip 连接上哮天
with SparkySdk.RobotControl('192.168.8.212') as robot:
    # 添加消息回调函数
    robot.add_message_callback(msgCallback)
    # 切换成遥控模式，并返回遥控模式操作对象
    ctrl = robot.switch_mode(SparkySdk.MODE_CTRL)
    # 使用遥控模式操作对象设定 x 轴速度
    ctrl.movex = 1
    # 同步到哮天
    ctrl.sync()
    input('回车退出程序，哮天将恢复默认状态')
```

演示使用 SparkySdk 在编辑模式下，编写摇摆的关键帧，并保存

```python
# 导入 SparkySdk
import SparkySdk
import time
# 定义一个消息回调函数
def msgCallback(self, ws, message):
    print(message)
# 通过 ip 连接上哮天
with SparkySdk.RobotControl('192.168.8.212') as robot:
    # 添加消息回调函数
    robot.add_message_callback(msgCallback)
    # 切换成编辑模式，并返回编辑模式操作对象
    edit = robot.switch_mode(SparkySdk.MODE_EDIT)
    # 设置 pitch 为 0.6
    edit.pitch = 0.6
    # 延时一段时间，让哮天来得及动
    time.sleep(1)
    # 设置 pitch 为 -0.6 ， 实现摇摆
    edit.pitch = -0.6
    time.sleep(1)
    edit.pitch = 0.6
    input('回车退出程序，哮天将恢复默认状态')
```

演示使用 SparkySdk 在示教模式下，录制动作，播放动作

```python
from SparkySdk import RobotControl
import time
import SparkySdk

with RobotControl('192.168.8.212') as robot:
    # 切换成示教模式，并返回示教模式操作对象
    teach = robot.switch_mode(SparkySdk.MODE_TEACH)
    teach.start_record()
    input('回车结束录制')
    teach.stop_record()
    input('回车开始播放')
    teach.start_play()
    input('回车退出程序，哮天将恢复默认状态')
```

