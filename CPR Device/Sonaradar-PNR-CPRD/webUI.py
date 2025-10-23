import base64
import json
import os
from bottle import Bottle, request, redirect, run, template, static_file, response
from utils import *
from socketClient import *
from function import *

class BottleApp:
    def __init__(self):
        self.app = Bottle()  # 创建一个Bottle应用实例

        # 路由配置
        self.setup_routes()

    def setup_routes(self):
        # 静态文件路由
        self.app.route('/static/<filepath:path>')(self.serve_static)
        # 管理面板模板
        self.app.route('/page/manage')(self.page_manage)
        # 管理面板模板
        self.app.route('/page/login')(self.page_login)
        # 登录处理接口
        self.app.get('/api/login')(self.login)
        # 设置页面
        self.app.route('/page/manage_settings')(self.page_manage_settings)
        # 获取摄像头图像的路由
        self.app.route('/api/get_camera_image')(self.get_camera_image_route)
        # 设置服务器IP接口
        self.app.route('/api/set_server_ip')(self.set_server_ip)
        # 设置摄像头索引接口
        self.app.route('/api/set_camera_index')(self.set_camera_index)
        # 设置识别开关接口
        self.app.route('/api/set_recognization_enable')(self.set_recognization_enable)
        # 设置用户接口
        self.app.route('/api/set_user')(self.set_user)

    # 静态文件路由
    def serve_static(self, filepath):
        static_folder = os.path.join(os.path.dirname(__file__), 'views', 'static')
        return static_file(filepath, root=static_folder)

    # 管理面板模板
    def page_manage(self):
        return template('manage_index')

    # 登录页面模板
    def page_login(self):
        return template('login')

    # 登录处理接口
    def login(self):
        username = request.query.getunicode('username')
        password = request.query.getunicode('password')

        configUtil = ConfigUtil()
        real_username = configUtil.read('user', 'username')
        real_password = configUtil.read('user', 'password')

        if real_username is None or real_password is None:
            real_password = '123456'
            real_username = 'administrator'
            configUtil.write('user', 'username', real_username)
            configUtil.write('user', 'password', real_password)
        
        if username == real_username and password == real_password:
            return template('messageBox_login', message='登录成功!', redirectURL='../page/manage')
        else:
            return template('messageBox_login', message='用户名或密码错误，请重新尝试!', redirectURL='../page/login')

    # 设置页面
    def page_manage_settings(self):
        configUtil = ConfigUtil()
        localIP = SocketClientCommand.get_local_ip()
        machineCode = MachineCodeUtil.get_machine_code()
        serverIp = configUtil.read('server', 'ip')
        if serverIp is None:
            serverIp = ''
        cameraIndex = configUtil.read('camera', 'index')
        if cameraIndex is None:
            cameraIndex = 0
        cameraList = CarPlateDetection.get_camera_info()

        recognizationEnable = configUtil.read('function', 'recognization_enable')
        recognizationEnable = True if recognizationEnable == '1' else False

        return template('manage_settings',
                       data_localIP=localIP,
                       data_machineCode=machineCode,
                       data_serverIP=serverIp,
                       data_cameraList=cameraList,
                       data_cameraIndex=cameraIndex,
                       data_username=configUtil.read('user', 'username'),
                       data_password=configUtil.read('user', 'password'),
                       data_recognization_enable=recognizationEnable)

    # 获取摄像头图像的路由
    def get_camera_image_route(self):
        camera_index = int(request.query.get('camera_index'))

        try:
            image_base64 = CarPlateDetection.capture_image_from_camera(camera_index)
            image_base64 = CarPlateDetection.image_to_base64(image_base64)
            return {"image_base64": image_base64}
        except Exception as e:
            return {"error": str(e)}

    # 设置服务器IP接口
    def set_server_ip(self):
        server_ip = request.query.get('server_ip')
        configUtil = ConfigUtil()
        configUtil.write('server', 'ip', server_ip)
        return template('messageBox', message='修改成功!', redirectURL='../page/manage_settings')

    # 设置摄像头索引接口
    def set_camera_index(self):
        camera_index = request.query.get('camera_index')
        configUtil = ConfigUtil()
        configUtil.write('camera', 'index', camera_index)
        return template('messageBox', message='修改成功!', redirectURL='../page/manage_settings')

    # 设置识别开关接口
    def set_recognization_enable(self):
        recognization_enable = int(request.query.get('cp_mode'))
        recognization_enable = '0' if recognization_enable == 0 else '1'
        configUtil = ConfigUtil()
        configUtil.write('function', 'recognization_enable', recognization_enable)
        return template('messageBox', message='修改成功!', redirectURL='../page/manage_settings')

    # 设置用户接口
    def set_user(self):
        username = request.query.get('username')
        password = request.query.get('password')
        configUtil = ConfigUtil()
        configUtil.write('user', 'username', username)
        configUtil.write('user', 'password', password)
        return template('messageBox', message='修改成功!', redirectURL='../page/manage_settings')

    def run(self, host='localhost', port=8080):
        # 启动Bottle服务端
        run(self.app, host=host, port=port)
