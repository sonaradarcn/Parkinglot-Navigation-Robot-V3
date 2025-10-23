#!/usr/bin/env python
# encoding: utf-8

import json

class SocketMessage:
    COMMANDCODE_SHAKEHAND = 'shakehand'
    COMMANDCODE_GETROBOTPOSITION = 'get_robot_position'
    COMMANDCODE_SEARCHCAR = 'search_car'
    COMMANDCODE_UPDATESTANDBYPOSITION = 'update_standby_position'
    COMMANDCODE_UPDATEROBOTCORESTATUS = 'update_robot_core_status'
    COMMANDCODE_SCANWAIT = 'scan_wait'
    COMMANDCODE_SEARCHOWMER = 'search_owner'

    def __init__(self, machineID, commandCode, parameters):
        self.machineID = machineID
        self.commandCode = commandCode
        self.parameters = parameters

    def to_json(self):
        """将 SocketMessage 对象转换为 JSON 字符串"""
        # 使用 ensure_ascii=False 保证非 ASCII 字符（如中文）能够正确处理
        return json.dumps({
            'machineID': self.machineID,
            'commandCode': self.commandCode,
            'parameters': self.parameters
        }, ensure_ascii=False)  # 确保输出的 JSON 可以正确处理非 ASCII 字符

    @staticmethod
    def from_json(json_str):
        """从 JSON 字符串创建 SocketMessage 对象"""
        data = json.loads(json_str)  # 默认解析为 unicode
        return SocketMessage(
            machineID=data['machineID'],
            commandCode=data['commandCode'],
            parameters=data['parameters']
        )
