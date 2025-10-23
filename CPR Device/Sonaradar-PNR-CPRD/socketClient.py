
import socket
import threading
from utils import *
import json
import time
from function import *
import requests

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
        try:
            self.client_socket.send(message.encode('utf-8'))
            print("[Sonaradar-PNR-SocketServer] Sent message to server: {}".format(message))
        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error sending message to server: {}".format(e))
    
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
                    
                    data = json.loads(message)
                    
                    #车牌识别
                    if(data['commandCode']=='carplate_detection'):
                        cpri_coordinates = []
                        parameters = json.loads(data['parameters'])
                        for coordinate in parameters:
                            cpri_coordinate={
                                'x1':coordinate['x1'],
                                'y1':coordinate['y1'],
                                'x2':coordinate['x2'],
                                'y2':coordinate['y2'],
                                'id':coordinate['id']
                            }
                            cpri_coordinates.append(cpri_coordinate)
                        print(cpri_coordinates)
                        CarPlateDetection.autorun(cpri_coordinates)
                        
                    
                else:
                    print("[Sonaradar-PNR-SocketServer] Connection to server closed.")
                    break
            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error receiving message: {}".format(e))
                break
    
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
    def start_socket(server_ip='127.0.0.1', server_port=12000):
        """静态方法，启动客户端并建立连接"""
        if SocketClientCommand.socket_client is None:
            SocketClientCommand.socket_client = SocketClient(server_ip, server_port)
            SocketClientCommand.socket_client.start()
            print("[Sonaradar-PNR-IDCertification] Socket client started and connected.")
            SocketClientCommand.function_shakehand()
            thread = threading.Thread(target=SocketClientCommand.function_sendImage)
            thread.start()
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
    def is_socket_running() -> bool:
        """检查 socket 是否在运行"""
        return SocketClientCommand.socket_client is not None
    
    @staticmethod
    def function_shakehand():
        data = {
            'machineID': SocketClientCommand.machine_code,
            'commandCode': 'shakehand',
            'parameters': ''
        }
        data = json.dumps(data)

        SocketClientCommand.send_to_server(data)
    
    @staticmethod
    def capture_and_upload_image():
        """处理图像捕捉、转换为Base64并上传到服务器"""
        configUtil = ConfigUtil()

        try:
            # 获取图片
            image = CarPlateDetection.capture_image_from_camera(int(configUtil.read('camera', 'index')))
            
            if image is not None:
                # 将图片转换为Base64
                image_base64 = CarPlateDetection.image_to_base64(image)
                
                # 将Base64解码为二进制数据
                image_binary = base64.b64decode(image_base64)
                
                # 准备文件数据上传
                files = {
                    'image': ('image.jpg', image_binary, 'image/jpeg')  # 指定图片类型
                }
                
                # 上传其他数据
                data = {
                    'machine_id': SocketClientCommand.machine_code
                }
                
                # 发送 POST 请求上传文件
                response = requests.post('http://{}:8080/api/cprd_image_upload'.format(configUtil.read('server', 'ip')), files=files, data=data)
                
                if response.status_code == 200:
                    print(f"[Sonaradar-PNR] Image uploaded successfully for machine {SocketClientCommand.machine_code}")
                else:
                    print(f"[Sonaradar-PNR] Error uploading image: {response.status_code}")
        
        except Exception as e:
            print(f"[Sonaradar-PNR-SocketServer] Error while sending image to server: {e}")
    
    @staticmethod
    def function_sendImage():
        """控制每10秒调用一次 capture_and_upload_image"""
        while True:
            SocketClientCommand.capture_and_upload_image()  # 调用上传图像的功能
            time.sleep(5)  # 每10秒上传一次

        