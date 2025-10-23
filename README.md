# Parkinglot Navigation Robot V3（基于SLAM的停车场智能寻车机器人）

**声明：**
**如果您从第三方平台通过购买途径得到本项目相关材料，请要求退款！**

## 1.项目介绍
该项目是一个面向大型停车场环境中“寻车难”问题的解决方案。项目通过融合机器人技术、实时定位与地图构建（SLAM）、车牌识别、语音交互等关键技术，构建了一套完整的软硬件系统，实现从车辆停放识别到引导车主寻车的全流程自动化服务。

本项目获得奖项如下：
| 获奖时间 | 奖项名称 |
| :--- | :--- |
| 2023/06 | 第二十五届中国机器人及人工智能大赛机器人创新赛省赛三等奖 |
| 2023/11 | 山东省大学生软件设计大赛智能硬件与机器人软件开发一等奖 |
| 2023/11 | 山东省大学生智能技术应用设计大赛智能技术自由探索一等奖 |
| 2024/06 | 第二十六届中国机器人及人工智能大赛(山东赛区)人工智能创新赛一等奖 |
| 2024/07 | 2024中国大学生计算机设计大赛山东省级赛一等奖 |
| 2024/07 | 2024年(第17届)中国大学生计算机设计大赛二等奖 |
| 2024/07 | 2024睿抗机器人开发者大赛(RAICOM)山东赛区智能系统竞赛项目二等奖 |
| 2024/08 | 第二十六届中国机器人及人工智能大赛全国总决赛人工智能创新赛一等奖 |
| 2024/08 | 2024睿抗机器人开发者大赛(RAICOM)智能系统竞赛项目三等奖 |
| 2023/06 - 2024/06 | 国家级大学生创新训练计划立项 |
| 2025/09 | 优秀毕业论文 |

PS：本项目开发完成时间为2025年2月，之前参赛版本为V1(2023.04-2023.06)和V2(2023.09-2024.08)

在本项目仓库中，提供了项目三个端的源代码。除此之外，在Documents文件夹中提供了项目报告(毕业论文删减版)，演示文档。上述文件均为可编辑版本。

本项目代码部分分为三个主要部分，分别为：**服务器端、机器人端、CPR端(车牌识别设备端，部分文件可能显示为CPRD端，属于早期命名问题)**，均已上传至本项目仓库。项目框架图下图所示：

![项目框架图](https://github.com/sonaradarcn/Parkinglot-Navigation-Robot-V3/blob/main/Picture/4-1.png?raw=true)

本系统以智能寻车服务为核心目标，采用模块化分层架构，整合服务器端、CPR（Car Plate Recognizing）端与机器人端三部分协同工作。系统整体实现过程始于用户交互层，用户通过语音或文本输入寻车请求，服务器端基于Qwen大模型解析语义并识别意图，调用机器人调度功能。CPR设备通过摄像头实时采集车位图像，结合YOLOv11模型检测车牌位置，并利用Paddle OCR完成文字识别，将车位状态至服务器数据库。机器人端利用ROS框架实现机器人导航控制，并设计两种寻车方式：定点扫码寻车与非定点扫码寻车两种寻车模式。

## 2.项目部署说明
**如果您仅使用本项目参赛，可跳过本步骤**
### 2.1 服务器部署说明
本项目服务器建议部署在Windows环境（Windows 10或者Windows 11，其他版本易导致语音合成模块故障。本项目语音合成功能依赖于Edge-TTS。）

部署流程
- 安装Anaconda，创建虚拟环境。
- 启动Anaconda虚拟环境，使用pip安装下述依赖：
```pip
pip install bottle pymysql edge-tts pyttsx3 pydub Pillow dashscope aip
```
- 对项目源码中的参数进行配置
```python
#打开llm.py文件进行配置
class LLMUtil: 
    _api_key = ""  # 请替换为您的API Key,访问https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.1e8c7ca0RPxxIZ#/efm/model_center申请
```
```python
#打开utils.py进行配置
class DBUtil:
    def __init__(self):
        self.host = "127.0.0.1" #你的MySQL服务器地址
        self.user = "pnr_root" #MySQL用户名
        self.password = "abc123456" #MySQL密码
        self.database = "sonaradar_pnr_v3" #数据库名称
        self.connection = None
```
```python
#打开webServer.py
if __name__ == '__main__':
    SocketServer.start_server_thread()
    run(app, host='192.168.149.18', port=8080)#配置为本机地址，或者0.0.0.0
```
- 将数据表导入MySQL(本步骤会尽快完善说明，因为开发电脑损坏导致数据库丢失，数据表将会在后期上传)。
- 启动 webServer.py
### 2.2 机器人部署说明
本项目机器人使用的是幻尔机器人的JetAuto型号（带有触摸显示屏，激光雷达）。ROS话题可能和其他环境不一样，如果需要部署在其他机器人上请自行适配。

部署流程：

- 安装所有项目所需的依赖项（默认使用幻尔机器人JetAuto，并且ROS1已经完成配置流程）。
```pip
pip install bottle Pillow qrcode[pil]
```
- 切换到项目所在路径，对settings.ini文件进行配置
```ini
[server]
server-url = http://192.168.149.18:8080/ #这里填写服务器Bottle服务器的IP和端口
server-ip = 192.168.149.18 #这里填写服务器Bottle服务器的IP
```
- 打开项目源码，对项目代码参数进行配置
```python
# 打开webUI.py,找到这一行进行配置
if __name__ == '__main__':
    rospy.init_node('sonaradar_pnr_robot')
    configUtil = ConfigUtil()
    SocketClientCommand.start_socket(configUtil.read("server","server-ip"), 12000)
    Core.init()
    run(app, host='192.168.149.1', port=12002) #替换成机器人的IP，端口可以随意调整
```
- 启动 webUI.py。
### 2.3 CPR端部署说明
CPR设备端由树莓派4B外加一台摄像头组成，每个车位前面放置一个。树莓派应当采用Ubuntu 22.04。如果因为经费限制，可以使用虚拟机安装Ubuntu 22.04外加摄像头来替代实现。
- 安装所有项目所需的依赖项
```pip
pip install bottle opencv-python ultralytics paddlepaddle paddleocr requests configparser
```
- 启动 webUI.py
- 在CPR设备上，使用浏览器打开 http://localhost:8080/page/login ，登录到系统中对相关参数进行配置，初始登录信息：username = administrator，password = 123456

当您要测试本程序时，请按照服务器端、CPR端、机器人端顺序进行启动，否则会导致机器人无法连接至服务器。

## 3.项目详细介绍
该部分请参考Documents文件夹中的项目报告文档或演示幻灯片。

## [可选部分]关于重复参赛说明
**声明：不鼓励使用本项目重复参加其他比赛，参加各类创新类比赛请遵守比赛规定，造成的任何后果请使用者自行承担。**

经实际测试，CRAIC比赛（即中国机器人及人工智能大赛）对于重复参赛项目检测力度较小，而中国大学生计算机设计大赛对于重复参赛项目检测力度较大（一般默认重复参赛项目给予省赛三等奖，不进入答辩）。对于各类省级比赛（本处所指省级比赛均为只有省赛没有国赛的比赛）大部分比赛不会检测重复参赛。

本项目仅V2版本参加过国赛，V3版本尚未参加过比赛。

由于Github平台限制上传文件大小，故本仓库不提供演示视频，演示视频请前往Bilibili平台搜索下载（演示视频请搜索关键词：基于SLAM的停车场智能寻车机器人）。


<p align="center" style="font-size:12px;font-weight:bold">
    <img src="https://github.com/sonaradarcn/Sonaradar_Copyright_Assets/blob/main/SEL%20LOGO%20github%20copyright.png?raw=true" alt="描述" style="height:32px;align-content:center;margin-left:10px;">
</p>







