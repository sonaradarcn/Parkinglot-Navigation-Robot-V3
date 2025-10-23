import socket
import threading
import json
import time

from entity import *
from dao import *
from utils import *


class SocketServer:
    host = ''
    port = 12000
    clients = {}
    ip_machine_map = {}  # 存储 IP 和 machineID
    robot_core_status_map = {}  # 存储 机器人状态
    server = None  # 将 server 变量定义为类的全局变量
    robotPositionList = []

    @staticmethod
    def start():
        # 获取本机 IP 地址并设置
        #SocketServer.host = '192.168.3.175'
        SocketServer.host = '192.168.149.18'
        # SocketServer.host = SocketServer.get_local_ip()

        # 创建并启动服务器
        SocketServer.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketServer.server.bind((SocketServer.host, SocketServer.port))
        SocketServer.server.listen(5)
        print("[Sonaradar-PNR-SocketServer] Server listening on {}:{}...".format(SocketServer.host, SocketServer.port))

        thread = threading.Thread(target=SocketServer.carPlateDetection)
        thread.start()

        while True:
            client_socket, client_address = SocketServer.server.accept()
            print("[Sonaradar-PNR-SocketServer] New connection from {}:{}".format(client_address[0], client_address[1]))

            # 将客户端存入 clients 字典
            SocketServer.clients[client_address] = client_socket

            # 启动线程处理该客户端消息
            client_thread = threading.Thread(target=SocketServer.handle_client, args=(client_socket, client_address))
            client_thread.start()

    # 用线程启动 SocketServer
    @staticmethod
    def start_server_thread():
        server_thread = threading.Thread(target=SocketServer.start)
        server_thread.daemon = True  # 设置为守护线程，主线程退出时，守护线程也会退出
        server_thread.start()

    @staticmethod
    def handle_client(client_socket, client_address):
        while True:
            try:
                # 接收客户端发送的数据
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                #JSON标准化
                message = message.replace("\\\"", "\"")
                if message.startswith('\"') and message.endswith('\"'):
                    message = message[1:-1]
                message = message.replace("\\\\\"", "\\\"")


                print("[Sonaradar-PNR-SocketServer] Received message from {}:{}: {}".format(client_address[0],
                                                                                            client_address[1], message))

                try:
                    socketMessage = SocketMessage.from_json(message)
                    machine_id = socketMessage.machineID
                    # 如果获取到 machineID，存储到 ip_machine_map 中
                    if machine_id:
                        SocketServer.ip_machine_map[client_address[0]] = machine_id
                        print("[Sonaradar-PNR-SocketServer] Updated machineID for IP {}: {}".format(client_address[0],
                                                                                                    machine_id))
                    # 判断命令
                    if socketMessage.commandCode == SocketMessage.COMMANDCODE_SHAKEHAND:
                        # 接收到不做反应
                        pass

                    if(socketMessage.commandCode==SocketMessage.COMMANDCODE_GETROBOTPOSITION):
                        robotDao = RobotDao()
                        robot = robotDao.getRobotByMachineId(socketMessage.machineID)
                        data = socketMessage.parameters
                        data = json.loads(data)
                        point = Point(0,data['x'],data['y'],'')
                        positionUpdate = RobotPosition(robot,point)
                        for position in SocketServer.robotPositionList:
                            if(position.robot.machine_id==socketMessage.machineID):
                                SocketServer.robotPositionList.remove(position)
                                break
                        SocketServer.robotPositionList.append(positionUpdate)
                        print("[Sonaradar-PNR-SocketServer] Update robot(MID:{},Position:({},{})) position successfully.".format(socketMessage.machineID,data['x'],data['y']))
                        #更新待机位置
                        robotStandbyPositionDao = RobotStandbyPositionDao()
                        robotStandbyPosition = robotStandbyPositionDao.getRobotStandbyPositionsByRobotId(robot.id)
                        SocketServer.function_sendStandbyPosition(robotStandbyPosition[0],robot,client_socket)

                    if(socketMessage.commandCode==SocketMessage.COMMANDCODE_UPDATEROBOTCORESTATUS):
                        SocketServer.robot_core_status_map[socketMessage.machineID] = json.loads(socketMessage.parameters)
                        print("[Sonaradar-PNR-SocketServer] Update robot(MID:{}) status successfully, details:{}.".format(socketMessage.machineID,SocketServer.robot_core_status_map[socketMessage.machineID]))


                    # if(socketMessage.commandCode==SocketMessage.COMMANDCODE_CPRDUPDATEIMAGE):
                    #     data = socketMessage.parameters
                    #     data = json.loads(data)
                    #     image = ImageUtil.base64_to_image(data['imageBase64'])
                    #     ImageUtil.save_image(image,'cprdImage/{}.jpg'.format(socketMessage.machineID))



                except Exception as e:
                    print("[Sonaradar-PNR-SocketServer] Error with dealing json. Reason:{}.".format(e))

            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error with client {}:{}: {}".format(client_address[0],
                                                                                        client_address[1], e))
                break

        # 关闭客户端连接
        client_socket.close()
        print("[Sonaradar-PNR-SocketServer] Connection with {}:{} closed.".format(client_address[0], client_address[1]))
        del SocketServer.clients[client_address]

    @staticmethod
    def send_to_client(client_socket, message):
        try:
            client_socket.send(message.encode('utf-8'))
            print("[Sonaradar-PNR-SocketServer] Sent message to client: {}".format(message))
        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error sending message to client: {}".format(e))

    @staticmethod
    def broadcast_message(message):
        for client_address, client_socket in SocketServer.clients.items():
            try:
                client_socket.send(message.encode('utf-8'))
                print(f"[Sonaradar-PNR-SocketServer] Broadcast message sent to {client_address[0]}:{client_address[1]}")
            except Exception as e:
                print(
                    f"[Sonaradar-PNR-SocketServer] Error sending broadcast to {client_address[0]}:{client_address[1]}: {e}")

    @staticmethod
    def get_local_ip() -> str:
        """获取本机的 IP 地址"""
        try:
            # 获取本机的主机名
            host_name = socket.gethostname()
            # 根据主机名获取本机的 IP 地址
            local_ip = socket.gethostbyname(host_name)
            return local_ip
        except socket.error as err:
            print(f"获取 IP 地址失败: {err}")
            return None


    @staticmethod
    def carPlateDetection():

        """
        后门程序
        开启暂停车牌识别，保存识别车辆信息
        """
        if(True):
            return

        cprdDao = CPRDeviceDao()
        cpriDao = CPRInfoDao()

        while(SocketServer.server!=None):
            CPRDevices = cprdDao.getCPRDevices()
            for cprDevice in CPRDevices:
                for ip, machine_id in SocketServer.ip_machine_map.items():
                    if cprDevice.machine_id == machine_id:
                        for client_address, client_socket in SocketServer.clients.items():
                            if client_address[0] == ip:
                                # TCPRDevice.description = client_address[0]
                                # availableCPRDevice.append(TCPRDevice)
                                cpris = cpriDao.getCPRInfoByCPRDId(cprDevice.id)
                                parameters = []
                                for cpri in cpris:
                                    tdata = {
                                        'x1': cpri.x1,
                                        'y1': cpri.y1,
                                        'x2': cpri.x2,
                                        'y2': cpri.y2,
                                        'id': cpri.id
                                    }
                                    parameters.append(tdata)
                                parameters = json.dumps(parameters)
                                socketMessage = SocketMessage("", SocketMessage.COMMANDCODE_CARPLATEDETECTION,
                                                              parameters)
                                socketMessage = SocketMessage.to_json(socketMessage)
                                SocketServer.send_to_client(client_socket, socketMessage)
            time.sleep(5)

    @staticmethod
    def function_searchCar(parkingPlace,client_socket):
        parameters = {
            'car_plate_no':parkingPlace.car_plate_no,
            'parking_place_no':parkingPlace.name,
            'x':parkingPlace.point_x,
            'y':parkingPlace.point_y
        }
        parameters = json.dumps(parameters)
        socketMessage = SocketMessage("", SocketMessage.COMMANDCODE_SEARCHCAR,
                                      parameters)
        socketMessage = SocketMessage.to_json(socketMessage)
        SocketServer.send_to_client(client_socket, socketMessage)

    @staticmethod
    def function_sendStandbyPosition(robotStandbyPosition,robot,client_socket):
        parameters = {
            'x':robotStandbyPosition.point_x,
            'y':robotStandbyPosition.point_y,
            'robot_mode':robot.mode
        }
        parameters = json.dumps(parameters)
        socketMessage = SocketMessage("", SocketMessage.COMMANDCODE_UPDATESTANDBYPOSITION,
                                      parameters)
        socketMessage = SocketMessage.to_json(socketMessage)
        SocketServer.send_to_client(client_socket, socketMessage)

    @staticmethod
    def function_scanWait(client_socket):
        socketMessage = SocketMessage("", SocketMessage.COMMANDCODE_SCANWAIT,'')
        socketMessage = SocketMessage.to_json(socketMessage)
        SocketServer.send_to_client(client_socket, socketMessage)

    @staticmethod
    def function_searchOwner(parkingPlace,carOwnerWaitZone,client_socket):
        parameters = {
            'car_plate_no':parkingPlace.car_plate_no,
            'parking_place_no':parkingPlace.name,
            'x':parkingPlace.point_x,
            'y':parkingPlace.point_y,
            'pre_x':carOwnerWaitZone.x,
            'pre_y':carOwnerWaitZone.y
        }
        parameters = json.dumps(parameters)
        socketMessage = SocketMessage("", SocketMessage.COMMANDCODE_SEARCHOWMER,
                                      parameters)
        socketMessage = SocketMessage.to_json(socketMessage)
        SocketServer.send_to_client(client_socket, socketMessage)