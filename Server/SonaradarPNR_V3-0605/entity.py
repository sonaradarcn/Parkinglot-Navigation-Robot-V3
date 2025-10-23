import json
class User:

    ROLE_ADMIN = 1
    ROLE_SUPERADMIN = 2

    STATUS_ENABLE = 1
    STATUS_DISABLE = 0

    def __init__(self, id: int, username: str, password: str, role: int, enable: int):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.enable = enable


class SocketMessage:
    COMMANDCODE_SHAKEHAND = 'shakehand'
    COMMANDCODE_GETROBOTPOSITION = 'get_robot_position'
    COMMANDCODE_CPRDUPDATEIMAGE = 'cprd_update_image'
    COMMANDCODE_CARPLATEDETECTION = 'carplate_detection'
    COMMANDCODE_SEARCHCAR = 'search_car'
    COMMANDCODE_UPDATESTANDBYPOSITION = 'update_standby_position'
    COMMANDCODE_UPDATEROBOTCORESTATUS = 'update_robot_core_status'
    COMMANDCODE_SCANWAIT = 'scan_wait'
    COMMANDCODE_SEARCHOWMER = 'search_owner'

    def __init__(self, machineID: str, commandCode: str, parameters: str):
        self.machineID = machineID
        self.commandCode = commandCode
        self.parameters = parameters

    def to_json(self) -> str:
        """将 SocketMessage 对象转换为 JSON 字符串"""
        return json.dumps({
            'machineID': self.machineID,
            'commandCode': self.commandCode,
            'parameters': self.parameters
        })

    @staticmethod
    def from_json(json_str: str):
        """从 JSON 字符串创建 SocketMessage 对象"""
        data = json.loads(json_str)
        return SocketMessage(
            machineID=data['machineID'],
            commandCode=data['commandCode'],
            parameters=data['parameters']
        )

class Point:
    def __init__(self, id: int, x: float, y: float, description: str):
        self.id = id
        self.x = x
        self.y = y
        self.description = description

class Robot:

    MODE_ONSERVICE = 1;
    MODE_OFFSERVICE = 0;
    MODE_DEBUG = 2;

    def __init__(self, id: int, machine_id: str, name: str, description: str, mode: int):
        self.id = id
        self.machine_id = machine_id
        self.name = name
        self.description = description
        self.mode = mode


class RobotPosition:

    def __init__(self, robot:Robot, point:Point):
        self.robot = robot
        self.point = point

class CPRDevice:

    def __init__(self, id: int, machine_id: str, name: str, description: str):
        self.id = id
        self.machine_id = machine_id
        self.name = name
        self.description = description

class CPRInfo:
    def __init__(self, id: int, name: str, description: str, cprd_id: int, x1: float, y1: float, x2: float, y2: float, occupying_flag: bool, car_plate_no: str, image: bytes):
        self.id = id
        self.name = name
        self.description = description
        self.cprd_id = cprd_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.occupying_flag = occupying_flag
        self.car_plate_no = car_plate_no
        self.image = image


class ParkingPlace:
    def __init__(self, id: int, name: str, description: str, cpri_id: int, cpri_name: str, cpri_description: str,
                 x1: float, y1: float, x2: float, y2: float, occupying_flag: int, car_plate_no: str, image: bytes,
                 point_id: int, point_x: float, point_y: float, point_description: str):
        self.id = id
        self.name = name
        self.description = description

        # Cpri信息
        self.cpri_id = cpri_id
        self.cpri_name = cpri_name
        self.cpri_description = cpri_description
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.occupying_flag = occupying_flag
        self.car_plate_no = car_plate_no
        self.image = image

        # Point信息
        self.point_id = point_id
        self.point_x = point_x
        self.point_y = point_y
        self.point_description = point_description

class RobotStandbyPosition:
    def __init__(self, id: int, robot_id: int, point_id: int ,
                 name: str, description: str, robot_machine_id: str, robot_name: str,
                 robot_description: str, robot_mode: int, point_x: float, point_y: float, point_description: str):
        # RobotStandbyPosition的字段
        self.id = id
        self.robot_id = robot_id
        self.point_id = point_id
        self.name = name
        self.description = description

        # Robot信息

        self.robot_machine_id = robot_machine_id
        self.robot_name = robot_name
        self.robot_description = robot_description
        self.robot_mode = robot_mode

        # Point信息

        self.point_x = point_x
        self.point_y = point_y
        self.point_description = point_description

class CarOwnerWaitZone:
    def __init__(self, id: int, point_id: int, name: str, description: str, point_id_in_point: int, x: float, y: float):
        self.id = id
        self.point_id = point_id
        self.name = name
        self.description = description
        self.point_id_in_point = point_id_in_point  # Point表中的id
        self.x = x  # Point表中的x
        self.y = y  # Point表中的y

class devShow:
    devList = [
        {
            'image':'../static/images/head.jpg',
            'name':'',
            'nick':'Sonaradar',
            'description':''
        },
        {
            'image': '../static/images/head2.jpg',
            'name': '',
            'nick': '',
            'description': ''
        }
    ]
    count = 0









