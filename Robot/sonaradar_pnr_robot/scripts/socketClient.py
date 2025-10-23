#!/usr/bin/env python
# encoding: utf-8

import socket
import threading
from entity import *
from utils import *
import json
from robotFunction import *
from core import *
import time

class SocketClient:
    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 启动客户端并连接服务器
    def start(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("[Sonaradar-PNR-SocketServer] Connected to server at {}:{}".format(self.server_ip, self.server_port))

            # 启动接收服务器消息的线程
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error connecting to server: {}".format(e))
    
    # 发送消息给服务器
    def send_message(self, message):
        # try:
            self.client_socket.send(message.encode('utf-8'))
            print("[Sonaradar-PNR-SocketServer] Sent message to server: {}".format(message))
        # except Exception as e:
        #     print("[Sonaradar-PNR-SocketServer] Error sending message to server: {}".format(e))
    
    # 接收来自服务器的消息
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    
                    # json 标准化
                    #message = message.replace("\\\"", "\"")
                    if message.startswith('\"') and message.endswith('\"'):
                        message = message[1:-1]
                    #message = message.replace("\\\\\"", "\\\"")
                    print("[Sonaradar-PNR-SocketServer] Received from server: {}".format(message))
                    
                    socketMessage = SocketMessage.from_json(message)
                    # 判断命令
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_SHAKEHAND:
                        # 接收到不做反应
                        pass
                    
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_SEARCHCAR:
                        """
        parameters = {
            'car_plate_no':parkingPlace.car_plate_no,
            'parking_place_no':parkingPlace.name,
            'x':parkingPlace.point_x,
            'y':parkingPlace.point_y
        }
                        """
                        data = json.loads(socketMessage.parameters)
                        Core.car_plate_no = data['car_plate_no']
                        Core.parking_place_no = data['parking_place_no']
                        # Core.search_car(data['x'],data['y'])
                        thread = threading.Thread(target=self.start_search_car, args=(data['x'], data['y']))
                        thread.start()  # 启动线程
                    
                    #更新机器人待机位置命令
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_UPDATESTANDBYPOSITION:
                        data = json.loads(socketMessage.parameters)
                        Core.standby_position_x = data['x']
                        Core.standby_position_y = data['y']
                        Core.robot_mode = int(data['robot_mode'])
                        print("[Sonaradar-PNR-SocketServer] Set robot standby position, location:({},{}).".format(data['x'],data['y']))
                        
                    #扫码机器人等待
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_SCANWAIT:
                        Core.search_scan_wait()
                        
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_SEARCHOWMER:
                        """
                        parameters = {
                           'car_plate_no':parkingPlace.car_plate_no,
                            'parking_place_no':parkingPlace.name,
                            'x':parkingPlace.point_x,
                            'y':parkingPlace.point_y,
                            'pre_x':carOwnerWaitZone.x,
                            'pre_y':carOwnerWaitZone.y
                        }
                        """ 
                        data = json.loads(socketMessage.parameters)
                        Core.car_plate_no = data['car_plate_no']
                        Core.parking_place_no = data['parking_place_no']
                        # Core.search_driver(data['pre_x'],data['pre_y'])
                        # Core.search_car(data['x'],data['y'])
                        thread = threading.Thread(target=self.start_search_car_owner, args=(data['pre_x'],data['pre_y'],data['x'], data['y']))
                        thread.start()  # 启动线程
                       
                    
                        
                    
                        
                        
                else:
                    print("[Sonaradar-PNR-SocketServer] Connection to server closed.")
            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error receiving message: {}".format(e))
                
    # 启动线程并传递参数
    def start_search_car(self, x, y):
        Core.search_car(x,y)
        
    # 启动线程并传递参数
    def start_search_car_owner(self, pre_x,pre_y,x,y):
        Core.search_driver(pre_x,pre_y)
        Core.search_car(x,y)
    
    # 断开连接
    def disconnect(self):
        try:
            self.client_socket.close()
            print("[Sonaradar-PNR-SocketServer] Disconnected from server.")
        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error disconnecting from server: {}".format(e))


class SocketClientCommand:
    # 静态保存的 SocketClient 实例
    socket_client = None
    machine_code = MachineCodeUtil.get_machine_code()

    @staticmethod
    def start_socket(server_ip='127.0.0.1', server_port=12345):
        """静态方法，启动客户端并建立连接"""
        if SocketClientCommand.socket_client is None:
            SocketClientCommand.socket_client = SocketClient(server_ip, server_port)
            SocketClientCommand.socket_client.start()
            print("[Sonaradar-PNR-IDCertification] Socket client started and connected.")
            SocketClientCommand.function_shakehand()
            thread = threading.Thread(target=SocketClientCommand.function_sendPosition)
            thread.start()
            time.sleep(2.5)
            thread2 = threading.Thread(target=SocketClientCommand.function_sendCoreStatus)
            thread2.start()
        else:
            print("[Sonaradar-PNR-IDCertification] Socket client already running.")
    
    @staticmethod
    def send_to_server(message):
        """静态方法，向服务器发送消息"""
        if SocketClientCommand.socket_client is not None:
            SocketClientCommand.socket_client.send_message(message)
        else:
            print("[Sonaradar-PNR-IDCertification] No active connection to server.")
    
    @staticmethod
    def stop_socket():
        """静态方法，断开连接"""
        if SocketClientCommand.socket_client is not None:
            SocketClientCommand.socket_client.disconnect()
            SocketClientCommand.socket_client = None
        else:
            print("[Sonaradar-PNR-IDCertification] No active connection to close.")

    @staticmethod
    def function_shakehand():
        socketMessage = SocketMessage(SocketClientCommand.machine_code,SocketMessage.COMMANDCODE_SHAKEHAND,'');
        socketMessage = socketMessage.to_json()
        json_string = json.dumps(socketMessage)
        SocketClientCommand.send_to_server(json_string)
        
    @staticmethod
    def function_sendPosition():
        while(True):
            try:
                x,y,z = RobotNavigation.get_current_position()
                positionParameter = {
                    'x':x,
                    'y':y
                }
                socketMessage = SocketMessage(SocketClientCommand.machine_code,SocketMessage.COMMANDCODE_GETROBOTPOSITION,json.dumps(positionParameter));
                socketMessage = socketMessage.to_json()
                json_string = json.dumps(socketMessage)
                SocketClientCommand.send_to_server(json_string)
                print("[Sonaradar-PNR-SocketServer] Send position to server.")
            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error while send position to server, reason: {}.".format(e))
            time.sleep(5)
            
    @staticmethod
    def function_sendCoreStatus():
        while(True):
            try:
                data={
                    'is_searching_car': Core.is_searching_car,
                    'is_searching_driver':Core.is_searching_driver,
                    'is_searching_scan_wait':Core.is_searching_scan_wait
                }
                socketMessage = SocketMessage(SocketClientCommand.machine_code,SocketMessage.COMMANDCODE_UPDATEROBOTCORESTATUS,json.dumps(data));
                socketMessage = socketMessage.to_json()
                json_string = json.dumps(socketMessage)
                SocketClientCommand.send_to_server(json_string)
                print("[Sonaradar-PNR-SocketServer] Send robot status to server.")
            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error while send robot status to server, reason: {}.".format(e))
            time.sleep(5)
            
    @staticmethod
    def get_local_ip():
        """获取本机的 IP 地址"""
        try:
            # 获取本机的主机名
            host_name = socket.gethostname()
            # 根据主机名获取本机的 IP 地址
            local_ip = socket.gethostbyname(host_name)
            return local_ip
        except socket.error as err:
            
            return None
        

    

# # 示例：使用 SocketClientCommand 启动和停止 SocketClient
# if __name__ == "__main__":
#     rospy.init_node('sonaradar_pnr_robot')
#     # 启动客户端并连接服务器
#     SocketClientCommand.start_socket('192.168.3.175', 12000)
    
#     #核心启动
#     Core.init()
    
#     # # 停止客户端并断开连接
#     # SocketClientCommand.stop_socket()
#     while(True):
#         pass