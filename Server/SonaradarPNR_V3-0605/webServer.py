import base64
import json
import os
import time
import traceback

from bottle import Bottle, request, redirect, run, template, static_file , response
from dao import *
from utils import *
import re
from difflib import SequenceMatcher
import io
from  socketServer import *

import os
from bottle import Bottle, request, response, run, static_file
from aip import AipSpeech
import json
from llm import *

app = Bottle()#bottle init

# 静态文件路由
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    static_folder = os.path.join(os.path.dirname(__file__), 'views', 'static')
    return static_file(filepath, root=static_folder)

#登录/注册页面
@app.route('/')
def verification():
    return template('verification')

#登录/注册页面
@app.route('/page/verification')
def verification():
    return template('verification')
#登录函数
@app.route('/api/login')
def api_login():
    username = request.query.getunicode('username')
    password = request.query.getunicode('password')
    userDao = UserDao()
    if(userDao.getUserByUsername(username) is not None):
        if (userDao.getUserByUsername(username).password == password):
            return template('messageBox_login',message='登录成功!',redirectURL='../page/manage')
    return template('messageBox_login',message='用户名或密码错误,请重新尝试登录!',redirectURL='../page/verification')

@app.route('/page/dev')
def dev():
    return template('devshow_frame')

@app.route('/page/dev_inner')
def front_findcar_inputcarplate():
    #print("{},{}".format(len(devShowCore.tempList),len(devShowCore.devList)))
    devShow.count = (devShow.count + 1)%len(devShow.devList)
    item = devShow.devList[devShow.count]
    #devShowCore.tempList.remove(item)
    return template('devshow_inner',head=item['image'],name=item['name'],nick=item['nick'],description=item['description'],version='V3X-2503')

#管理面板模板
@app.route('/page/manage')
def page_manage():
    return template('manage_index')

#用户列表页面
@app.route('/page/manage_user_list')
def page_manage_user_list():
    userDao = UserDao()
    return template('manage_user_list',data = userDao.getUsers())

#用户添加页面
@app.route('/page/manage_user_add')
def page_manage_user_list():
    return template('manage_user_add')

#用户添加api
@app.route('/api/user_add')
def api_user_add():
    username = request.query.getunicode('username')
    password = request.query.getunicode('password')
    role = int(request.query.getunicode('role'))
    enable = int(request.query.getunicode('enable'))
    userDao = UserDao()
    userDao.addUser(User(None,username,password,role,enable))
    return template('messageBox',message='添加用户成功!',redirectURL='../page/manage_user_list')

#用户修改页面
@app.route('/page/manage_user_edit')
def page_manage_user_edit():
    id = int(request.query.getunicode('id'))
    userDao = UserDao()
    return template('manage_user_edit',data = userDao.getUser(id))

#用户修改api
@app.route('/api/user_edit')
def api_user_edit():
    id = int(request.query.getunicode('id'))
    username = request.query.getunicode('username')
    password = request.query.getunicode('password')
    role = int(request.query.getunicode('role'))
    enable = int(request.query.getunicode('enable'))
    userDao = UserDao()
    userDao.setUser(User(id,username,password,role,enable))
    return template('messageBox', message='修改用户信息成功!', redirectURL='../page/manage_user_list')

#用户删除api
@app.route('/api/user_remove')
def api_user_remove():
    id = int(request.query.getunicode('id'))
    userDao = UserDao()
    userDao.removeUser(id)
    return template('messageBox', message='删除用户成功!', redirectURL='../page/manage_user_list')

'''
点位管理
'''
# 点列表页面
@app.route('/page/manage_point_list')
def page_manage_point_list():
    pointDao = PointDao()
    return template('manage_point_list', data=pointDao.getPoints())

# 点添加页面
@app.route('/page/manage_point_add')
def page_manage_point_add():
    robotDao = RobotDao()
    robots = robotDao.getRobots()
    availableRobots = []
    for robot in robots:
        if(robot.mode==Robot.MODE_DEBUG):
            for ip, machine_id in SocketServer.ip_machine_map.items():
                if(machine_id==robot.machine_id):
                    for client_address, client_socket in SocketServer.clients.items():
                        if(client_address[0]==ip):
                            for position in SocketServer.robotPositionList:
                                if (position.robot.machine_id == robot.machine_id):
                                    availableRobots.append(robot)

    return template('manage_point_add',availableRobotsData = availableRobots)

# 点位回传功能
@app.route('/api/get_robot_position')
def api_point_edit():
    id = int(request.query.getunicode('id'))
    robotDao = RobotDao()
    point = None
    for position in SocketServer.robotPositionList:
        if(position.robot.id==id):
            point = position.point

    response.content_type = 'application/json'
    data = {
        'x':point.x,
        'y':point.y
    }
    # 使用 json.dumps() 来返回 JSON 格式的数据
    return json.dumps(data)


# 点添加api
@app.route('/api/point_add')
def api_point_add():
    x = float(request.query.getunicode('x'))
    y = float(request.query.getunicode('y'))
    description = request.query.getunicode('description')
    pointDao = PointDao()
    pointDao.addPoint(Point(None, x, y, description))
    return template('messageBox', message='添加点成功!', redirectURL='../page/manage_point_list')

# 点修改页面
@app.route('/page/manage_point_edit')
def page_manage_point_edit():
    id = int(request.query.getunicode('id'))
    pointDao = PointDao()

    robotDao = RobotDao()
    robots = robotDao.getRobots()
    availableRobots = []
    for robot in robots:
        if(robot.mode==Robot.MODE_DEBUG):
            for ip, machine_id in SocketServer.ip_machine_map.items():
                if(machine_id==robot.machine_id):
                    for client_address, client_socket in SocketServer.clients.items():
                        if(client_address[0]==ip):
                            for position in SocketServer.robotPositionList:
                                if (position.robot.machine_id == robot.machine_id):
                                    availableRobots.append(robot)

    return template('manage_point_edit', data=pointDao.getPoint(id),availableRobotsData = availableRobots)

# 点修改api
@app.route('/api/point_edit')
def api_point_edit():
    id = int(request.query.getunicode('id'))
    x = float(request.query.getunicode('x'))
    y = float(request.query.getunicode('y'))
    description = request.query.getunicode('description')
    pointDao = PointDao()
    pointDao.setPoint(Point(id, x, y, description))
    return template('messageBox', message='修改点信息成功!', redirectURL='../page/manage_point_list')

# 点删除api
@app.route('/api/point_remove')
def api_point_remove():
    id = int(request.query.getunicode('id'))
    pointDao = PointDao()
    pointDao.removePoint(id)
    return template('messageBox', message='删除点成功!', redirectURL='../page/manage_point_list')


@app.route('/page/test')
def page_test():
    return template('error-404')

'''
机器人管理
'''
# 机器人列表页面
@app.route('/page/manage_robot_list')
def page_manage_robot_list():
    robotDao = RobotDao()
    availableRobots = []
    robots = robotDao.getRobots()
    for robot in robots:
        for ip, machine_id in SocketServer.ip_machine_map.items():
            if (machine_id == robot.machine_id):
                for client_address, client_socket in SocketServer.clients.items():
                    if (client_address[0] == ip):
                        availableRobots.append(robot)
    return template('manage_robot_list', data=robotDao.getRobots(),availableRobotsData = availableRobots)

# 机器人添加页面
@app.route('/page/manage_robot_add')
def page_manage_robot_add():
    return template('manage_robot_add')

# 机器人添加api
@app.route('/api/robot_add')
def api_robot_add():
    machine_id = request.query.getunicode('machine_id')
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    mode = int(request.query.getunicode('mode'))
    robotDao = RobotDao()
    robotDao.addRobot(Robot(None, machine_id, name, description, mode))
    return template('messageBox', message='添加机器人成功!', redirectURL='../page/manage_robot_list')

# 机器人修改页面
@app.route('/page/manage_robot_edit')
def page_manage_robot_edit():
    id = int(request.query.getunicode('id'))
    robotDao = RobotDao()
    return template('manage_robot_edit', data=robotDao.getRobot(id))

# 机器人修改api
@app.route('/api/robot_edit')
def api_robot_edit():
    id = int(request.query.getunicode('id'))
    machine_id = request.query.getunicode('machine_id')
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    mode = int(request.query.getunicode('mode'))
    robotDao = RobotDao()
    robotDao.setRobot(Robot(id, machine_id, name, description, mode))
    return template('messageBox', message='修改机器人信息成功!', redirectURL='../page/manage_robot_list')

# 机器人删除api
@app.route('/api/robot_remove')
def api_robot_remove():
    id = int(request.query.getunicode('id'))
    robotDao = RobotDao()
    robotDao.removeRobot(id)
    return template('messageBox', message='删除机器人成功!', redirectURL='../page/manage_robot_list')

'''
Sonaradar-CPRDevice(车牌识别设备) 管理 
'''
# CPR设备列表页面
@app.route('/page/manage_cprd_list')
def page_manage_device_list():
    deviceDao = CPRDeviceDao()
    availableCPRDevice = []
    CPRDevices = deviceDao.getCPRDevices()
    for CPRDevice in CPRDevices:
        for ip, machine_id in SocketServer.ip_machine_map.items():
            if(CPRDevice.machine_id==machine_id):
                for client_address, client_socket in SocketServer.clients.items():
                    if (client_address[0] == ip):
                        TCPRDevice = CPRDevice
                        TCPRDevice.description = client_address[0]
                        availableCPRDevice.append(TCPRDevice)

    return template('manage_cprd_list', data=deviceDao.getCPRDevices(),availableCPRDeviceData=availableCPRDevice)

# CPR设备添加页面
@app.route('/page/manage_cprd_add')
def page_manage_device_add():
    return template('manage_cprd_add')

# CPR设备添加api
@app.route('/api/cprd_add')
def api_device_add():
    machine_id = request.query.getunicode('machine_id')
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    deviceDao = CPRDeviceDao()
    deviceDao.addCPRDevice(CPRDevice(None, machine_id, name, description))
    return template('messageBox', message='添加设备成功!', redirectURL='../page/manage_cprd_list')

# CPR设备修改页面
@app.route('/page/manage_cprd_edit')
def page_manage_device_edit():
    id = int(request.query.getunicode('id'))
    deviceDao = CPRDeviceDao()
    return template('manage_cprd_edit', data=deviceDao.getCPRDevice(id))

# CPR设备修改api
@app.route('/api/cprd_edit')
def api_device_edit():
    id = int(request.query.getunicode('id'))
    machine_id = request.query.getunicode('machine_id')
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    deviceDao = CPRDeviceDao()
    deviceDao.setCPRDevice(CPRDevice(id, machine_id, name, description))
    return template('messageBox', message='修改设备信息成功!', redirectURL='../page/manage_cprd_list')

# CPR设备删除api
@app.route('/api/cprd_remove')
def api_device_remove():
    id = int(request.query.getunicode('id'))
    deviceDao = CPRDeviceDao()
    deviceDao.removeCPRDevice(id)
    return template('messageBox', message='删除设备成功!', redirectURL='../page/manage_cprd_list')

#CPRD图片上传接口
# 上传图片接口
@app.route('/api/cprd_image_upload', method='POST')
def do_upload():
    # 获取上传的文件
    upload = request.files.get('image')

    # 获取机器 ID
    machineID = request.forms.get('machine_id')

    if upload:
        # 定义文件的保存路径，使用机器 ID 来命名文件
        save_path = 'cprdImage/{}.jpg'.format(machineID)

        # 如果文件已经存在，删除旧文件
        if os.path.exists(save_path):
            os.remove(save_path)
            print(f"[Sonaradar-PNR] Existing file {save_path} removed.")

        # 保存文件到指定路径
        upload.save(save_path)

        return f"File {machineID}.jpg uploaded and saved successfully!"
    else:
        return "No file uploaded."

'''
CPRI 信息管理
'''
# CPR信息列表页面
@app.route('/page/manage_cpri_list')
def page_manage_cpri_list():
    cpriDao = CPRInfoDao()
    cprdDao = CPRDeviceDao()
    return template('manage_cpri_list', data=cpriDao.getCPRInfos(),cprdData=cprdDao.getCPRDevices())

# CPR信息添加页面
@app.route('/page/manage_cpri_add')
def page_manage_cpri_add():
    # 获取可用CPRD设备
    deviceDao = CPRDeviceDao()
    availableCPRDevice = []
    CPRDevices = deviceDao.getCPRDevices()
    for CPRDevice in CPRDevices:
        for ip, machine_id in SocketServer.ip_machine_map.items():
            if CPRDevice.machine_id == machine_id:
                for client_address, client_socket in SocketServer.clients.items():
                    if client_address[0] == ip:
                        TCPRDevice = CPRDevice
                        TCPRDevice.description = client_address[0]
                        availableCPRDevice.append(TCPRDevice)

    return template('manage_cpri_add', availableCPRDeviceData=availableCPRDevice)

# CPR信息添加api
@app.route('/api/cpri_add')
def api_cpri_add():
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    cprd_id = int(request.query.getunicode('cprd_id'))
    x1 = float(request.query.getunicode('x1'))
    y1 = float(request.query.getunicode('y1'))
    x2 = float(request.query.getunicode('x2'))
    y2 = float(request.query.getunicode('y2'))
    # occupying_flag, car_plate_no, image 不从请求中获取，因为它们不能修改
    cpriDao = CPRInfoDao()
    # 默认占用标志为False，车牌号和图片为空
    cpriDao.addCPRInfo(CPRInfo(None, name, description, cprd_id, x1, y1, x2, y2, False, "", b''))
    return template('messageBox', message='添加CPR信息成功!', redirectURL='../page/manage_cpri_list')

# CPR信息修改页面
@app.route('/page/manage_cpri_edit')
def page_manage_cpri_edit():
    id = int(request.query.getunicode('id'))
    cpriDao = CPRInfoDao()
    cpri = cpriDao.getCPRInfo(id)

    # 获取可用CPRD设备
    deviceDao = CPRDeviceDao()
    availableCPRDevice = []
    CPRDevices = deviceDao.getCPRDevices()
    for CPRDevice in CPRDevices:
        for ip, machine_id in SocketServer.ip_machine_map.items():
            if CPRDevice.machine_id == machine_id:
                for client_address, client_socket in SocketServer.clients.items():
                    if client_address[0] == ip:
                        TCPRDevice = CPRDevice
                        TCPRDevice.description = client_address[0]
                        availableCPRDevice.append(TCPRDevice)

    # 在编辑页面只展示不可修改的字段
    return template('manage_cpri_edit', data=cpri,availableCPRDeviceData=availableCPRDevice)

# CPR信息修改api
@app.route('/api/cpri_edit')
def api_cpri_edit():
    id = int(request.query.getunicode('id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    cprd_id = int(request.query.getunicode('cprd_id'))
    x1 = float(request.query.getunicode('x1'))
    y1 = float(request.query.getunicode('y1'))
    x2 = float(request.query.getunicode('x2'))
    y2 = float(request.query.getunicode('y2'))
    # occupying_flag, car_plate_no, image 不更新
    cpriDao = CPRInfoDao()
    cpriDao.setCPRInfo(CPRInfo(id, name, description, cprd_id, x1, y1, x2, y2, False, "", b''))  # 这些字段不修改
    return template('messageBox', message='修改CPR信息成功!', redirectURL='../page/manage_cpri_list')

# CPR信息删除api
@app.route('/api/cpri_remove')
def api_cpri_remove():
    id = int(request.query.getunicode('id'))
    cpriDao = CPRInfoDao()
    cpriDao.removeCPRInfo(id)
    return template('messageBox', message='删除CPR信息成功!', redirectURL='../page/manage_cpri_list')


# CPR信息获取摄像头图片
@app.route('/api/cpri_get_cprd_image')
def api_cpri_get_cprd_image():
    id = int(request.query.getunicode('id'))
    cprDeviceDao = CPRDeviceDao()
    imagePath = 'cprdImage/{}.jpg'.format(cprDeviceDao.getCPRDevice(id).machine_id)
    image = ImageUtil.read_image(imagePath)

    if not os.path.exists(imagePath):
        print(f"[Error] File {imagePath} does not exist.")
        return None

    try:
        # 读取图片
        image = Image.open(imagePath)
        print(f"[Info] Image {imagePath} successfully loaded.")

        # 将图片保存到内存中的缓冲区
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # 可以根据需要调整格式
        # 获取图片的二进制数据并转换为 base64 编码
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print("[Info] Image successfully converted to Base64.")

        return {"image_base64": img_base64}
    except Exception as e:
        print(f"[Error] Error processing image {imagePath}: {e}")
        return {"image_base64": None}


@app.route('/api/cpri_upload', method='POST')
def api_cpri_upload():
    try:
        # 从表单中获取其他字段
        id = int(request.forms.get('id'))
        occupying_flag = int(request.forms.get('occupying_flag'))
        carplate_no = request.forms.get('carplate_no')

        # 获取上传的图片文件
        image = request.files.get('image')
        # 读取上传的图片文件（无需保存为文件）
        img = Image.open(image.file)  # 直接从文件流读取图片
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')  # 将图片保存到内存中的BytesIO对象
        img_blob = img_byte_arr.getvalue()  # 获取二进制数据

        if occupying_flag == 1:
            occupying_flag = True
        else:
            occupying_flag = False

        cpri = CPRInfo(id,"","","","","","","",occupying_flag,carplate_no,img_blob)
        cpriDao = CPRInfoDao()
        cpriDao.setCPRAdditionalInfo(cpri)

        print(f"[Sonaradar-PNR]Upload CPR information successfully.")

        return f"文件上传成功！信息：ID={id}, 占用状态={occupying_flag}, 车牌号={carplate_no}"

    except Exception as e:
        print(f"[Sonaradar-PNR]Upload CPR information error, reason: {str(e)}")
        return f"上传失败，错误: {str(e)}"


# CPR信息修改页面
@app.route('/page/manage_cpri_view')
def page_manage_cpri_edit():
    id = int(request.query.getunicode('id'))
    cpriDao = CPRInfoDao()
    cpri = cpriDao.getCPRInfo(id)
    # 在编辑页面只展示不可修改的字段
    return template('manage_cpri_view', data=cpri,image_base64=base64.b64encode(cpri.image).decode('utf-8'))

'''
ParkingPlace
'''
# 停车位列表页面
@app.route('/page/manage_parking_place_list')
def page_manage_parking_place_list():
    parkingPlaceDao = ParkingPlaceDao()
    return template('manage_parking_place_list', data=parkingPlaceDao.getParkingPlaces())

# 停车位添加页面
@app.route('/page/manage_parking_place_add')
def page_manage_parking_place_add():
    cpriDao = CPRInfoDao()
    pointDao = PointDao()

    return template('manage_parking_place_add',cpris=cpriDao.getCPRInfos(),points=pointDao.getPoints())

# 停车位添加api
@app.route('/api/parking_place_add')
def api_parking_place_add():
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    cpri_id = int(request.query.getunicode('cpri_id'))
    point_id = int(request.query.getunicode('point_id'))
    parkingPlaceDao = ParkingPlaceDao()
    parkingPlaceDao.addParkingPlace(ParkingPlace(None, name, description, cpri_id, '', '', 0, 0, 0, 0, 0, '', None, point_id, 0, 0, ''))
    return template('messageBox', message='添加停车位成功!', redirectURL='../page/manage_parking_place_list')

# 停车位修改页面
@app.route('/page/manage_parking_place_edit')
def page_manage_parking_place_edit():
    id = int(request.query.getunicode('id'))
    parkingPlaceDao = ParkingPlaceDao()
    cpriDao = CPRInfoDao()
    pointDao = PointDao()
    return template('manage_parking_place_edit', data=parkingPlaceDao.getParkingPlace(id),cpris=cpriDao.getCPRInfos(),points=pointDao.getPoints())

# 停车位修改api
@app.route('/api/parking_place_edit')
def api_parking_place_edit():
    id = int(request.query.getunicode('id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    cpri_id = int(request.query.getunicode('cpri_id'))
    point_id = int(request.query.getunicode('point_id'))
    parkingPlaceDao = ParkingPlaceDao()
    parkingPlaceDao.setParkingPlace(ParkingPlace(id, name, description, cpri_id, '', '', 0, 0, 0, 0, 0, '', None, point_id, 0, 0, ''))
    return template('messageBox', message='修改停车位信息成功!', redirectURL='../page/manage_parking_place_list')

# 停车位删除api
@app.route('/api/parking_place_remove')
def api_parking_place_remove():
    id = int(request.query.getunicode('id'))
    parkingPlaceDao = ParkingPlaceDao()
    parkingPlaceDao.removeParkingPlace(id)
    return template('messageBox', message='删除停车位成功!', redirectURL='../page/manage_parking_place_list')

'''
robot_standby_position
'''
# 机器人备用位置列表页面
@app.route('/page/manage_robot_standby_position_list')
def page_manage_robot_standby_position_list():
    robotStandbyPositionDao = RobotStandbyPositionDao()
    # 获取所有机器人备用位置数据
    positions = robotStandbyPositionDao.getRobotStandbyPositions()  # 可以根据需要调整查询条件
    return template('manage_robot_standby_position_list', data=positions)


# 机器人备用位置添加页面
@app.route('/page/manage_robot_standby_position_add')
def page_manage_robot_standby_position_add():
    robotDao = RobotDao()
    pointDao = PointDao()
    return template('manage_robot_standby_position_add',robots=robotDao.getRobots(),points=pointDao.getPoints())


# 机器人备用位置添加 API
@app.route('/api/robot_standby_position_add')
def api_robot_standby_position_add():
    robot_id = int(request.query.getunicode('robot_id'))
    point_id = int(request.query.getunicode('point_id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')

    # 创建一个 RobotStandbyPosition 对象
    rsp = RobotStandbyPosition(None, robot_id, point_id, name, description, None, None, None, None, None, None, None)
    robotStandbyPositionDao = RobotStandbyPositionDao()
    robotStandbyPositionDao.addRobotStandbyPosition(rsp)

    # 返回成功提示页面
    return template('messageBox', message='添加备用位置成功!', redirectURL='../page/manage_robot_standby_position_list')


# 机器人备用位置修改页面
@app.route('/page/manage_robot_standby_position_edit')
def page_manage_robot_standby_position_edit():
    id = int(request.query.getunicode('id'))
    robotStandbyPositionDao = RobotStandbyPositionDao()
    position = robotStandbyPositionDao.getRobotStandbyPosition(id)
    robotDao = RobotDao()
    pointDao = PointDao()
    return template('manage_robot_standby_position_edit', data=position,robots=robotDao.getRobots(),points=pointDao.getPoints())


# 机器人备用位置修改 API
@app.route('/api/robot_standby_position_edit')
def api_robot_standby_position_edit():
    id = int(request.query.getunicode('id'))
    robot_id = int(request.query.getunicode('robot_id'))
    point_id = int(request.query.getunicode('point_id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')

    # 创建一个 RobotStandbyPosition 对象
    rsp = RobotStandbyPosition(id, robot_id, point_id, name, description, None, None, None, None, None, None, None)
    robotStandbyPositionDao = RobotStandbyPositionDao()
    robotStandbyPositionDao.setRobotStandbyPosition(rsp)

    # 返回成功提示页面
    return template('messageBox', message='修改备用位置成功!', redirectURL='../page/manage_robot_standby_position_list')


# 机器人备用位置删除 API
@app.route('/api/robot_standby_position_remove')
def api_robot_standby_position_remove():
    id = int(request.query.getunicode('id'))
    robotStandbyPositionDao = RobotStandbyPositionDao()
    robotStandbyPositionDao.removeRobotStandbyPosition(id)
    return template('messageBox', message='删除备用位置成功!', redirectURL='../page/manage_robot_standby_position_list')

"""
Car owner wait zone
"""
# 等待区列表页面
@app.route('/page/manage_car_owner_wait_zone_list')
def page_manage_car_owner_wait_zone_list():
    carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
    return template('manage_car_owner_wait_zone_list', data=carOwnerWaitZoneDao.getCarOwnerWaitZones())

# 等待区添加页面
@app.route('/page/manage_car_owner_wait_zone_add')
def page_manage_car_owner_wait_zone_add():
    pointDao = PointDao()
    return template('manage_car_owner_wait_zone_add',points=pointDao.getPoints())

# 等待区添加api
@app.route('/api/car_owner_wait_zone_add')
def api_car_owner_wait_zone_add():
    point_id = int(request.query.getunicode('point_id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
    carOwnerWaitZoneDao.addCarOwnerWaitZone(CarOwnerWaitZone(None, point_id, name, description))
    return template('messageBox', message='添加等待区成功!', redirectURL='../page/manage_car_owner_wait_zone_list')

# 等待区修改页面
@app.route('/page/manage_car_owner_wait_zone_edit')
def page_manage_car_owner_wait_zone_edit():
    id = int(request.query.getunicode('id'))
    pointDao = PointDao()
    carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
    return template('manage_car_owner_wait_zone_edit', data=carOwnerWaitZoneDao.getCarOwnerWaitZone(id),points=pointDao.getPoints())

# 等待区修改api
@app.route('/api/car_owner_wait_zone_edit')
def api_car_owner_wait_zone_edit():
    id = int(request.query.getunicode('id'))
    point_id = int(request.query.getunicode('point_id'))
    name = request.query.getunicode('name')
    description = request.query.getunicode('description')
    carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
    carOwnerWaitZoneDao.setCarOwnerWaitZone(CarOwnerWaitZone(id, point_id, name, description))
    return template('messageBox', message='修改等待区信息成功!', redirectURL='../page/manage_car_owner_wait_zone_list')

# 等待区删除api
@app.route('/api/car_owner_wait_zone_remove')
def api_car_owner_wait_zone_remove():
    id = int(request.query.getunicode('id'))
    carOwnerWaitZoneDao = CarOwnerWaitZoneDao()
    carOwnerWaitZoneDao.removeCarOwnerWaitZone(id)
    return template('messageBox', message='删除等待区成功!', redirectURL='../page/manage_car_owner_wait_zone_list')





"""
front LLM Chat
"""


# 处理前端上传的音频文件
@app.post('/api/upload_audio')
def upload_audio():
    try:
        machine_ID = request.json.get('machine_id')
        point_ID = request.json.get('point_id')
        # 获取上传的文件（前端的 FormData 中应该有一个 'audio' 字段）
        upload = request.files.get('audio')

        # 确保文件存在
        if not upload:
            response.status = 400
            return {"error": "No audio file uploaded."}

        # 获取上传的文件名和扩展名
        filename = upload.filename
        file_extension = filename.split('.')[-1]

        # 限制文件类型为 wav 格式
        if file_extension != 'wav':
            response.status = 400
            return {"error": "Invalid file type. Only 'wav' files are allowed."}

        # 保存文件到指定目录
        file_path = os.path.join('voiceRecord', filename)
        try:
            os.remove(file_path)
        except Exception as e:
            pass
        wav_path = os.path.join('voiceRecord', 'audio_transfered.wav')
        try:
            os.remove(wav_path)
        except Exception as e:
            pass
        upload.save(file_path)

        # 使用ffmpeg将音频文件转换为wav格式
        try:
            # 将文件转换为pcm编码的wav格式
            subprocess.run(['ffmpeg', '-i', file_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', wav_path],
                           check=True)
        except subprocess.CalledProcessError as e:
            pass

        # 调用语音识别处理 需要进行申请
        # https://cloud.baidu.com/doc/SPEECH/s/Tl9mh38eu
        APP_ID = ''
        API_KEY = ''
        SECRET_KEY = ''

        # 创建 AipSpeech 客户端
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        # 读取音频文件
        audio_data = get_file_content(wav_path)

        # 识别语音，dev_pid 参数为1537表示普通话识别
        result = client.asr(audio_data, 'pcm', 16000, {'dev_pid': 1537})

        # 返回识别结果
        if result['err_no'] == 0:
            recognition_result = result['result'][0]  # 返回第一个识别结果
        else:
            recognition_result = f"Error: {result['err_msg']}"

        if (machine_ID != ''):
            model_response = LLMUtil.dialog(recognition_result + "(本设备机器码为:{},如果不使用FunctionCall函数回复消息请忽略本括号内容,本括号内文字仅作为FunctionCall调用标识，不作为回答依据)".format(machine_ID))
        else:
            model_response = LLMUtil.dialog(recognition_result + "(本设备点位ID为:{},如果不使用FunctionCall函数回复消息请忽略本括号内容,本括号内文字仅作为FunctionCall调用标识，不作为回答依据)".format(point_ID))
        # 返回识别结果给前端
        return {"modelResponse": model_response}

    except Exception as e:
        # 如果发生错误，返回错误信息
        response.status = 500
        print(f"An error occurred: {traceback.format_exc()}")
        return {"error": f"An error occurred: {str(e)}"}

# 读取文件内容的函数
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 处理文字输入消息
@app.post('/api/chat_text')
def chat_text():
    try:
        machine_ID = request.json.get('machine_id')
        point_ID = request.json.get('point_id')
        # 获取用户输入的文字
        user_message = request.json.get('message')

        if not user_message:
            response.status = 400
            return {"error": "No message provided."}

        # TODO: 将用户输入的文本发送到大语言模型进行处理
        # 这里你可以调用大语言模型API并获取响应结果
        if (machine_ID != ''):
            model_response = LLMUtil.dialog(user_message + "(本设备机器码为:{},如果不使用FunctionCall函数回复消息请忽略本括号内容,本括号内文字仅作为FunctionCall调用标识，不作为回答依据)".format(machine_ID))
        else:
            model_response = LLMUtil.dialog(user_message + "(本设备点位ID为:{},如果不使用FunctionCall函数回复消息请忽略本括号内容,本括号内文字仅作为FunctionCall调用标识，不作为回答依据)".format(point_ID))

        print("[Sonaradar-PNR-LLM] LLM Response:{}".format(model_response))
        # 返回模型的回答
        return {"modelResponse": model_response}

    except Exception as e:
        # 如果发生错误，返回错误信息
        response.status = 500
        return {"error": f"An error occurred: {str(e)}"}

@app.route('/page/front_llm_chat')
def page_manage_parking_place_list():
    try:
        machine_ID = request.query.getunicode('machine_id')
        if(machine_ID!=None):

            robotDao = RobotDao()
            robots = robotDao.getRobots()
            for robot in robots:
                for ip, machine_id in SocketServer.ip_machine_map.items():
                    if (machine_id == robot.machine_id):
                        for client_address, client_socket in SocketServer.clients.items():
                            if (client_address[0] == ip):
                                for position in SocketServer.robotPositionList:
                                    if (position.robot.machine_id == robot.machine_id and robot.machine_id==machine_ID):
                                        SocketServer.function_scanWait(client_socket)

            return template('front_llm_chat',machine_id=machine_ID,point_id=0)
    except Exception as e:
        pass
    try:
        point_ID = int(request.query.getunicode('point_id'))
        if(point_ID!=0):
            return template('front_llm_chat', machine_id='', point_id=point_ID)
    except Exception as e:
        pass
    return template('front_llm_chat', machine_id='', point_id=0)

@app.route('/api/tts')
def api_tts():
    text = request.query.getunicode('text')

    # 使用时间戳生成文件名，确保不包含小数部分
    timestamp = int(time.time())
    soundPath = 'soundCache/{}.mp3'.format(timestamp)

    # 调用 TTS 生成声音文件
    TTSUtils.autoTTS(text, soundPath)

    # 返回文件的路径，确保路径是正确的
    return static_file('{}.mp3'.format(timestamp), root='./soundCache')


"""
STATUS PANEL
"""

# CPR信息修改页面
@app.route('/page/status_panel_cpri')
def page_status_panel_cpri():
    id = int(request.query.getunicode('id'))
    cpriDao = CPRInfoDao()
    cpri = cpriDao.getCPRInfo(id)
    # 在编辑页面只展示不可修改的字段
    return template('status_panel_cpri', data=cpri,image_base64=base64.b64encode(cpri.image).decode('utf-8'))

# CPR信息修改页面
@app.route('/page/status_panel_robot')
def page_status_panel_robot():
    id = int(request.query.getunicode('id'))
    robotDao = RobotDao()
    robots = robotDao.getRobots()
    robotData = robotDao.getRobot(id)
    flag1 = False
    for ip, machine_id in SocketServer.ip_machine_map.items():
        if (machine_id == robotData.machine_id):
            for client_address, client_socket in SocketServer.clients.items():
                if (client_address[0] == ip):
                    flag1 = True

    point = None
    for position in SocketServer.robotPositionList:
        if(position.robot.id==id):
            point = position.point

    try:
        flag3 = SocketServer.robot_core_status_map[robotData.machine_id]
    except Exception:
        flag3 = {
                    'is_searching_car': False,
                    'is_searching_driver':False,
                    'is_searching_scan_wait':False
                }

    return template('status_panel_robot', data=robotData, flag3=flag3,flag1=flag1,point=point)

# 测试方法
if __name__ == '__main__':
    #程序初始化
    SocketServer.start_server_thread()

    #启动bottle服务端
    #run(app, host=SocketServer.get_local_ip(), port=8080)
    run(app, host='192.168.149.18', port=8080)