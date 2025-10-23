import math
import subprocess
import wave
import pymysql as MySQLdb
from entity import *
import edge_tts
import asyncio
import asyncio
import pyttsx3
from io import BytesIO
import os
from pydub import AudioSegment

import base64
from PIL import Image

import json
import random
from dao import *
from dashscope import Generation
from socketServer import *


class LLMUtil:
    # 内部API Key  https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.1e8c7ca0RPxxIZ#/efm/model_center
    _api_key = ""  # 请替换为您的API Key

    # 工具列表
    tools = [
        # 工具1 通过车牌号查询车位号
        {
            "type": "function",
            "function": {
                "name": "get_parking_spot_by_plate",
                "description": "通过车牌号查询车位号，用于帮助车主找到他们的停车位。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "license_plate": {
                            "type": "string",
                            "description": "车主的车牌号，例如：京A12345"
                        }
                    },
                    "required": ["license_plate"]
                }
            }
        },
        # 工具2 提供车位编号实现寻车功能
        {
            "type": "function",
            "function": {
                "name": "find_car_by_parking_spot",
                "description": "通过车位编号实现寻车功能，帮助车主定位到指定车位。(这个函数需要提供点位ID在对应命令下才能用，不提供点位ID不能调用本函数)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parking_spot_id": {
                            "type": "string",
                            "description": "车位编号，用于寻找指定停车位置。"
                        },
                        "point_id": {
                            "type": "int",
                            "description": "点位ID，如：1"
                        }
                    },
                    "required": ["parking_spot_id","point_id"]
                }
            }
        },
        # 工具3 提供车牌号实现寻车功能
        {
            "type": "function",
            "function": {
                "name": "find_car_by_license_plate",
                "description": "通过车牌号实现寻车功能，帮助车主找到他们的停车位置。(这个函数需要提供点位ID在对应命令下才能用，不提供点位ID不能调用本函数)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "license_plate": {
                            "type": "string",
                            "description": "车主的车牌号，例如：京A12345"
                        },
                        "point_id": {
                            "type": "int",
                            "description": "点位ID，如：1"
                        }
                    },
                    "required": ["license_plate","point_id"]
                }
            }
        },
        # 工具4 提供车位编号实现寻车功能
        {
            "type": "function",
            "function": {
                "name": "find_car_by_parking_spot_1",
                "description": "通过车位编号实现寻车功能，帮助车主定位到指定车位。(这个函数需要提供机器码在对应命令下才能用，不提供机器码不能调用本函数)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parking_spot_id": {
                            "type": "string",
                            "description": "车位编号，用于寻找指定停车位置。"
                        },
                        "machine_id": {
                            "type": "string",
                            "description": "机器码,如:SUDIE2DS（长度不定，常见的是15位机器码）"
                        }
                    },
                    "required": ["parking_spot_id","machine_id"]
                }
            }
        },
        # 工具5 提供车牌号实现寻车功能
        {
            "type": "function",
            "function": {
                "name": "find_car_by_license_plate_1",
                "description": "通过车牌号实现寻车功能，帮助车主找到他们的停车位置。(这个函数需要提供机器码在对应命令下才能用，不提供机器码不能调用本函数)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "license_plate": {
                            "type": "string",
                            "description": "车主的车牌号，例如：京A12345"
                        },
                        "machine_id": {
                            "type": "string",
                            "description": "机器码,如:SUDIE2DS（长度不定，常见的是15位机器码）"
                        }
                    },
                    "required": ["license_plate","machine_id"]
                }
            }
        }
    ]

    # 获取模型响应
    @staticmethod
    def get_response(messages):
        response = Generation.call(
            api_key=LLMUtil._api_key,
            model='qwen-max',  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages,
            tools=LLMUtil.tools,
            seed=random.randint(1, 10000),
            result_format='message'
        )
        return response

    # 对话函数：输入消息，返回大语言模型回答
    @staticmethod
    def dialog(user_input):
        print("[Sonaradar-PNR-LLM] User input message:{}.".format(user_input))
        messages = [{"content": user_input, "role": "user"}]
        response = LLMUtil.get_response(messages)
        print("[Sonaradar-PNR-LLM] Server return message:{}.".format(response))
        assistant_output = response.output.choices[0].message
        if(LLMUtil.is_function_call(assistant_output)==True):
            return LLMUtil.call_function(assistant_output)
        else:
            return assistant_output["content"]


    # 判断是否调用FunctionCall函数：根据模型返回消息，判断是否需要调用工具
    @staticmethod
    def is_function_call(assistant_output):
        return 'tool_calls' in assistant_output and len(assistant_output['tool_calls']) > 0

    # 判断调用的是哪个functioncall函数：根据模型返回的消息判断调用的工具
    @staticmethod
    def call_function(assistant_output):
        if LLMUtil.is_function_call(assistant_output):
            tool_name = assistant_output.tool_calls[0]['function']['name']
            print(tool_name)

            if tool_name == 'get_parking_spot_by_plate':
                license_plate = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['license_plate']
                return LLMUtil.get_parking_spot_by_plate(license_plate)

            if tool_name == 'find_car_by_parking_spot':
                parking_spot_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['parking_spot_id']
                point_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['point_id']
                return LLMUtil.find_car_by_parking_spot(parking_spot_id,point_id)


            if tool_name == 'find_car_by_license_plate':
                license_plate = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['license_plate']
                point_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['point_id']
                return LLMUtil.find_car_by_license_plate(license_plate, point_id)

            if tool_name == 'find_car_by_parking_spot_1':
                parking_spot_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['parking_spot_id']
                machine_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['machine_id']
                return LLMUtil.find_car_by_parking_spot_1(parking_spot_id,machine_id)

            if tool_name == 'find_car_by_license_plate_1':
                license_plate = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['license_plate']
                machine_id = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['machine_id']
                return LLMUtil.find_car_by_license_plate_1(license_plate,machine_id)



    @staticmethod
    def get_parking_spot_by_plate(license_plate):
        parkingPlaceDao = ParkingPlaceDao()
        resultStr = ""
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            resultStr = resultStr + "\n" + "车位号:{},是否占用(1-占用，0-空闲)：{},车牌号:{}.".format(parkingPlace.name,parkingPlace.occupying_flag,parkingPlace.car_plate_no)

        message = "以下是该停车场的车位和车牌信息，请你告诉我车牌号为：{}的车辆停放车位的车位号（因为是文字识别可能车牌号有出入，有可能数据给出的车牌号和实际车牌号有出入）。下面是停车场数据：{}。回答按照以下格式：您的爱车<车牌号>停放在<车位号>号车位(此对话不需要使用functioncall)".format(license_plate,resultStr)
        message = LLMUtil.dialog(message)
        return message

    #墙上扫码
    @staticmethod
    def find_car_by_parking_spot(parking_spot_id,point_id):
        parkingPlaceDao = ParkingPlaceDao()
        resultStr = ""
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            resultStr = resultStr + "\n" + "车位号:{},是否占用(1-占用，0-空闲)：{},车牌号:{}.".format(parkingPlace.name,
                                                                                      parkingPlace.occupying_flag,
                                                                                      parkingPlace.car_plate_no)

        message = "以下是该停车场的车位和车牌信息，请你告诉我车位号为：{}的数据库中的最相似的车位号（因为是语音识别可能车牌号有出入，可能格式不对，有可能数据给出的车位号和实际车位号有出入）。下面是停车场数据：{}。请你仅给出数据库中匹配的一个车位号即可，除车位号外你不需要回答任何内容，除车位号字段外的内容回答是禁止的(此对话不需要使用functioncall)".format(
            parking_spot_id, resultStr)
        message = LLMUtil.dialog(message)
        parkingPlaceEntity = None
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            if (parkingPlace.name.replace(" ", "") == message.replace(" ", "")):
                parkingPlaceEntity = parkingPlace
                break
        if (parkingPlaceEntity != None):
            return LLMUtil.remote_find(parkingPlaceEntity, point_id)
        else:
            return "数据库内没有您提供的车位号信息，请您重新尝试！"

    #墙上扫码
    @staticmethod
    def find_car_by_license_plate(license_plate,point_id):
        parkingPlaceDao = ParkingPlaceDao()
        resultStr = ""
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            resultStr = resultStr + "\n" + "车位号:{},是否占用(1-占用，0-空闲)：{},车牌号:{}.".format(parkingPlace.name,
                                                                                      parkingPlace.occupying_flag,
                                                                                      parkingPlace.car_plate_no)

        message = "以下是该停车场的车位和车牌信息，请你告诉我车牌号为：{}的车辆停放车位的车位号（因为是文字识别可能车牌号有出入，有可能数据给出的车牌号和实际车牌号有出入）。下面是停车场数据：{}。请你仅给出数据库中匹配的一个车牌号即可，除车牌号外你不需要回答任何内容，除车牌号字段外的内容回答是禁止的(此对话不需要使用functioncall)".format(
            license_plate, resultStr)
        message = LLMUtil.dialog(message)

        parkingPlaceEntity = None
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            if (parkingPlace.name.replace(" ", "") == message.replace(" ", "")):
                parkingPlaceEntity = parkingPlace
                break
        if (parkingPlaceEntity != None):
            return LLMUtil.remote_find(parkingPlaceEntity, point_id)
        else:
            return "无法为您匹配到您的车辆，请您重新尝试！"

    @staticmethod
    def remote_find(parking_place,point_id):
        carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
        carOwnerWaitZone = carOwnerWaitZoneDao.getCarOwnerWaitZone(point_id)
        pointDao = PointDao()
        currentZonePoint = pointDao.getPoint(carOwnerWaitZone.point_id)

        minDistance = 9999999
        cs = None

        robotDao = RobotDao()
        robots = robotDao.getRobots()

        for robot in robots:
            for ip, machine_id in SocketServer.ip_machine_map.items():
                if (machine_id == robot.machine_id):
                    for client_address, client_socket in SocketServer.clients.items():
                        if (client_address[0] == ip):
                            for position in SocketServer.robotPositionList:
                                distance = math.sqrt((position.point.x-currentZonePoint.x)**2+(position.point.y-currentZonePoint.y)**2)
                                if(minDistance>=distance and robot.mode==1):
                                    minDistance = distance
                                    cs = client_socket

        SocketServer.function_searchOwner(parking_place,carOwnerWaitZone,cs)
        if cs == None:
            return "当前暂无可调度机器人，请您稍后重新尝试。"
        return "已为您匹配距离您当前位置最近的寻车机器人，机器人将在一段时间内抵达，感谢您的耐心等待！"


    #机器人屏幕扫码
    @staticmethod
    def find_car_by_parking_spot_1(parking_spot_id,machine_id):
        parkingPlaceDao = ParkingPlaceDao()
        resultStr = ""
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            resultStr = resultStr + "\n" + "车位号:{},是否占用(1-占用，0-空闲)：{},车牌号:{}.".format(parkingPlace.name,
                                                                                      parkingPlace.occupying_flag,
                                                                                      parkingPlace.car_plate_no)

        message = "以下是该停车场的车位和车牌信息，请你告诉我车位号为：{}的数据库中的最相似的车位号（因为是语音识别可能车牌号有出入，可能格式不对，有可能数据给出的车位号和实际车位号有出入）。下面是停车场数据：{}。请你仅给出数据库中匹配的一个车位号即可，除车位号外你不需要回答任何内容，除车位号字段外的内容回答是禁止的(此对话不需要使用functioncall)".format(parking_spot_id, resultStr)
        message = LLMUtil.dialog(message)
        parkingPlaceEntity = None
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            if (parkingPlace.name.replace(" ", "") == message.replace(" ", "")):
                parkingPlaceEntity = parkingPlace
                break
        if (parkingPlaceEntity != None):
            return LLMUtil.scan_on_robot(parkingPlaceEntity, machine_id)
        else:
            return "数据库内没有您提供的车位号信息，请您重新尝试！"

    #机器人屏幕扫码
    @staticmethod
    def find_car_by_license_plate_1(license_plate,machine_id):
        parkingPlaceDao = ParkingPlaceDao()
        resultStr = ""
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            resultStr = resultStr + "\n" + "车位号:{},是否占用(1-占用，0-空闲)：{},车牌号:{}.".format(parkingPlace.name,parkingPlace.occupying_flag,parkingPlace.car_plate_no)

        message = "以下是该停车场的车位和车牌信息，请你告诉我车牌号为：{}的车辆停放车位的车位号（因为是文字识别可能车牌号有出入，有可能数据给出的车牌号和实际车牌号有出入）。下面是停车场数据：{}。请你仅给出数据库中匹配的一个车牌号即可，除车牌号外你不需要回答任何内容，除车牌号字段外的内容回答是禁止的(此对话不需要使用functioncall)".format(license_plate,resultStr)
        message = LLMUtil.dialog(message)

        parkingPlaceEntity = None
        for parkingPlace in parkingPlaceDao.getParkingPlaces():
            if(parkingPlace.name.replace(" ","")==message.replace(" ","")):
                parkingPlaceEntity = parkingPlace
                break
        if(parkingPlaceEntity!=None):
            return LLMUtil.scan_on_robot(parkingPlaceEntity,machine_id)
        else:
            return "无法为您匹配到您的车辆，请您重新尝试！"

    @staticmethod
    def scan_on_robot(parking_place,machine_id_2):
        robotDao = RobotDao()
        robots = robotDao.getRobots()
        sc = None
        for robot in robots:
            for ip, machine_id in SocketServer.ip_machine_map.items():
                if (machine_id == robot.machine_id):
                    for client_address, client_socket in SocketServer.clients.items():
                        if (client_address[0] == ip):
                            for position in SocketServer.robotPositionList:
                                if (position.robot.machine_id == robot.machine_id and robot.machine_id == machine_id_2):
                                    sc = client_socket
        if sc == None:
            return "当前暂无可调度机器人，请您稍后重新尝试。"
        SocketServer.function_searchCar(parking_place,sc)
        return "已下发寻车任务至当前扫码机器人，请跟随机器人前往车位！"


# # 使用示例
# if __name__ == '__main__':
#     user_input = "现在几点了？"
#
#     assistant_response = LLMUtil.dialog(user_input)
#     print(f"大语言模型回答：{assistant_response}")
#
#     if LLMUtil.is_function_call(assistant_response):
#         result = LLMUtil.call_function(assistant_response)
#         print(f"调用的工具输出：{result}")