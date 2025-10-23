from entity import *
from utils import DBUtil


class UserDao:
    def __init__(self):
        self.db = DBUtil()

    def createUserFromRow(self, row):
        return User(int(row[0]), row[1], row[2], int(row[3]), int(row[4]))

    def getUser(self, id: int):
        self.db.connect()
        query = "SELECT * FROM user WHERE id = {}".format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createUserFromRow(row)

    def getUserByUsername(self, username: str):
        self.db.connect()
        query = "SELECT * FROM user WHERE username = '{}'".format(username)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createUserFromRow(row)

    def getUsers(self):
        self.db.connect()
        query = "SELECT * FROM user"
        result = self.db.execute_query(query)
        self.db.disconnect()

        users = []
        for row in result:
            users.append(self.createUserFromRow(row))
        return users

    def addUser(self, user: User):
        self.db.connect()
        query = "INSERT INTO user (username, password, role, enable) VALUES ('{}', '{}', {}, {})".format(
            user.username, user.password, user.role, user.enable)
        self.db.execute_update(query)
        self.db.disconnect()

    def setUser(self, user: User):
        self.db.connect()
        query = "UPDATE user SET username = '{}', password = '{}', role = {}, enable = {} WHERE id = {}".format(
            user.username, user.password, user.role, user.enable, user.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removeUser(self, id: int):
        self.db.connect()
        query = "DELETE FROM user WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class PointDao:
    def __init__(self):
        self.db = DBUtil()

    def createPointFromRow(self, row):
        return Point(int(row[0]), float(row[1]), float(row[2]), row[3])

    def getPoint(self, id: int):
        self.db.connect()
        query = "SELECT * FROM point WHERE id = {}".format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createPointFromRow(row)

    def getPoints(self):
        self.db.connect()
        query = "SELECT * FROM point"
        result = self.db.execute_query(query)
        self.db.disconnect()

        points = []
        for row in result:
            points.append(self.createPointFromRow(row))
        return points

    def addPoint(self, point: Point):
        self.db.connect()
        query = "INSERT INTO point (x, y, description) VALUES ({}, {}, '{}')".format(
            point.x, point.y, point.description)
        self.db.execute_update(query)
        self.db.disconnect()

    def setPoint(self, point: Point):
        self.db.connect()
        query = "UPDATE point SET x = {}, y = {}, description = '{}' WHERE id = {}".format(
            point.x, point.y, point.description, point.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removePoint(self, id: int):
        self.db.connect()
        query = "DELETE FROM point WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class RobotDao:
    def __init__(self):
        self.db = DBUtil()

    def createRobotFromRow(self, row):
        return Robot(int(row[0]), row[1], row[2], row[3], int(row[4]))

    def getRobot(self, id: int):
        self.db.connect()
        query = "SELECT * FROM robot WHERE id = {}".format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createRobotFromRow(row)

    def getRobotByMachineId(self, machine_id: str):
        self.db.connect()
        query = "SELECT * FROM robot WHERE machine_id = '{}'".format(machine_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createRobotFromRow(row)

    def getRobots(self):
        self.db.connect()
        query = "SELECT * FROM robot"
        result = self.db.execute_query(query)
        self.db.disconnect()

        robots = []
        for row in result:
            robots.append(self.createRobotFromRow(row))
        return robots

    def addRobot(self, robot: Robot):
        self.db.connect()
        query = "INSERT INTO robot (machine_id, name, description, mode) VALUES ('{}', '{}', '{}', {})".format(
            robot.machine_id, robot.name, robot.description, robot.mode)
        self.db.execute_update(query)
        self.db.disconnect()

    def setRobot(self, robot: Robot):
        self.db.connect()
        query = "UPDATE robot SET machine_id = '{}', name = '{}', description = '{}', mode = {} WHERE id = {}".format(
            robot.machine_id, robot.name, robot.description, robot.mode, robot.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removeRobot(self, id: int):
        self.db.connect()
        query = "DELETE FROM robot WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class CPRDeviceDao:
    def __init__(self):
        self.db = DBUtil()

    def createCPRDeviceFromRow(self, row):
        return CPRDevice(int(row[0]), row[1], row[2], row[3])

    def getCPRDevice(self, id: int):
        self.db.connect()
        query = "SELECT * FROM cpr_device WHERE id = {}".format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createCPRDeviceFromRow(row)

    def getCPRDeviceByMachineId(self, machine_id: str):
        self.db.connect()
        query = "SELECT * FROM cpr_device WHERE machine_id = '{}'".format(machine_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createCPRDeviceFromRow(row)

    def getCPRDevices(self):
        self.db.connect()
        query = "SELECT * FROM cpr_device"
        result = self.db.execute_query(query)
        self.db.disconnect()

        devices = []
        for row in result:
            devices.append(self.createCPRDeviceFromRow(row))
        return devices

    def addCPRDevice(self, cpr_device: CPRDevice):
        self.db.connect()
        query = "INSERT INTO cpr_device (machine_id, name, description) VALUES ('{}', '{}', '{}')".format(
            cpr_device.machine_id, cpr_device.name, cpr_device.description)
        self.db.execute_update(query)
        self.db.disconnect()

    def setCPRDevice(self, cpr_device: CPRDevice):
        self.db.connect()
        query = "UPDATE cpr_device SET machine_id = '{}', name = '{}', description = '{}' WHERE id = {}".format(
            cpr_device.machine_id, cpr_device.name, cpr_device.description, cpr_device.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removeCPRDevice(self, id: int):
        self.db.connect()
        query = "DELETE FROM cpr_device WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class CPRInfoDao:
    def __init__(self):
        self.db = DBUtil()

    def createCPRInfoFromRow(self, row):
        return CPRInfo(
            int(row[0]),  # id
            row[1],        # name
            row[2],        # description
            int(row[3]) if row[3] is not None else None,  # cprd_id
            float(row[4]) if row[4] is not None else None, # x1
            float(row[5]) if row[5] is not None else None, # y1
            float(row[6]) if row[6] is not None else None, # x2
            float(row[7]) if row[7] is not None else None, # y2
            bool(row[8]) if row[8] is not None else None,  # occupying_flag
            row[9],        # car_plate_no
            row[10]        # image (this is assumed to be a BLOB, we store it as bytes)
        )

    def getCPRInfo(self, id: int):
        self.db.connect()
        query = "SELECT * FROM cprd_recognising_zone WHERE id = {}".format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createCPRInfoFromRow(row)

    def getCPRInfoByCPRDId(self, cprd_id: int):
        self.db.connect()
        query = "SELECT * FROM cprd_recognising_zone WHERE cprd_id = {}".format(cprd_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return []  # 返回一个空列表，表示没有找到对应的结果

        # 将查询结果转换为 CPRInfo 对象列表
        cpri_list = []
        for row in result:
            cpri = self.createCPRInfoFromRow(row)
            cpri_list.append(cpri)

        return cpri_list  # 返回一个 CPRInfo 对象的列表

    def getCPRInfos(self):
        self.db.connect()
        query = "SELECT * FROM cprd_recognising_zone"
        result = self.db.execute_query(query)
        self.db.disconnect()

        cpr_infos = []
        for row in result:
            cpr_infos.append(self.createCPRInfoFromRow(row))
        return cpr_infos

    def addCPRInfo(self, cpr_info: CPRInfo):
        self.db.connect()
        query = "INSERT INTO cprd_recognising_zone (name, description, cprd_id, x1, y1, x2, y2, occupying_flag, car_plate_no, image) VALUES ('{}', '{}', {}, {}, {}, {}, {}, {}, '{}', '{}')".format(
            cpr_info.name, cpr_info.description, cpr_info.cprd_id, cpr_info.x1, cpr_info.y1, cpr_info.x2, cpr_info.y2,
            cpr_info.occupying_flag, cpr_info.car_plate_no, cpr_info.image.hex()  # Assuming image is in bytes and using hex to store it as string
        )
        self.db.execute_update(query)
        self.db.disconnect()

    def setCPRInfo(self, cpr_info: CPRInfo):
        """
        更新 CPR 基本信息，不包括占用状态、车牌号和图片
        """
        self.db.connect()
        query = """UPDATE cprd_recognising_zone SET 
                    name = '{}', description = '{}', cprd_id = {}, x1 = {}, y1 = {}, x2 = {}, y2 = {} 
                    WHERE id = {}""".format(
            cpr_info.name, cpr_info.description, cpr_info.cprd_id, cpr_info.x1, cpr_info.y1, cpr_info.x2, cpr_info.y2, cpr_info.id
        )
        self.db.execute_update(query)
        self.db.disconnect()

    def setCPRAdditionalInfo(self, cpr_info: CPRInfo):
        """
        只更新 CPR 的占用状态、车牌号和图片
        """
        self.db.connect()
        query = """UPDATE cprd_recognising_zone SET 
                    occupying_flag = %s, car_plate_no = %s, image = %s 
                    WHERE id = %s"""
        params = (cpr_info.occupying_flag, cpr_info.car_plate_no, cpr_info.image, cpr_info.id)
        self.db.execute_update_1(query, params)  # 这里传递参数元组
        self.db.disconnect()

    def removeCPRInfo(self, id: int):
        self.db.connect()
        query = "DELETE FROM cprd_recognising_zone WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()


class ParkingPlaceDao:
    def __init__(self):
        self.db = DBUtil()

    def createParkingPlaceFromRow(self, row):
        # 根据查询结果构造ParkingPlace对象
        return ParkingPlace(
            int(row[0]),  # id
            row[1],  # name
            row[2],  # description

            # Cpri信息
            int(row[3]),  # cpri_id
            row[4],  # cpri_name
            row[5],  # cpri_description
            float(row[6]),  # x1
            float(row[7]),  # y1
            float(row[8]),  # x2
            float(row[9]),  # y2
            int(row[10]),  # occupying_flag
            row[11],  # car_plate_no
            row[12],  # image

            # Point信息
            int(row[13]),  # point_id
            float(row[14]),  # point_x
            float(row[15]),  # point_y
            row[16]  # point_description
        )

    def getParkingPlace(self, id: int):
        self.db.connect()
        query = """
        SELECT pp.id, pp.name, pp.description, 
               cpr.id AS cpri_id, cpr.name AS cpri_name, cpr.description AS cpri_description, 
               cpr.x1, cpr.y1, cpr.x2, cpr.y2, cpr.occupying_flag, cpr.car_plate_no, cpr.image,
               pt.id AS point_id, pt.x AS point_x, pt.y AS point_y, pt.description AS point_description
        FROM parking_place pp
        LEFT JOIN cprd_recognising_zone cpr ON pp.cpri_id = cpr.id
        LEFT JOIN point pt ON pp.point_id = pt.id
        WHERE pp.id = {}
        """.format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createParkingPlaceFromRow(row)

    def getParkingPlaceByName(self, name: str):
        self.db.connect()
        query = """
        SELECT pp.id, pp.name, pp.description, 
               cpr.id AS cpri_id, cpr.name AS cpri_name, cpr.description AS cpri_description, 
               cpr.x1, cpr.y1, cpr.x2, cpr.y2, cpr.occupying_flag, cpr.car_plate_no, cpr.image,
               pt.id AS point_id, pt.x AS point_x, pt.y AS point_y, pt.description AS point_description
        FROM parking_place pp
        LEFT JOIN cprd_recognising_zone cpr ON pp.cpri_id = cpr.id
        LEFT JOIN point pt ON pp.point_id = pt.id
        WHERE pp.name = '{}'
        """.format(name)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createParkingPlaceFromRow(row)

    def getParkingPlaces(self):
        self.db.connect()
        query = """
        SELECT pp.id, pp.name, pp.description, 
               cpr.id AS cpri_id, cpr.name AS cpri_name, cpr.description AS cpri_description, 
               cpr.x1, cpr.y1, cpr.x2, cpr.y2, cpr.occupying_flag, cpr.car_plate_no, cpr.image,
               pt.id AS point_id, pt.x AS point_x, pt.y AS point_y, pt.description AS point_description
        FROM parking_place pp
        LEFT JOIN cprd_recognising_zone cpr ON pp.cpri_id = cpr.id
        LEFT JOIN point pt ON pp.point_id = pt.id
        """
        result = self.db.execute_query(query)
        self.db.disconnect()

        parking_places = []
        for row in result:
            parking_places.append(self.createParkingPlaceFromRow(row))
        return parking_places

    def addParkingPlace(self, parking_place: ParkingPlace):
        self.db.connect()
        query = """INSERT INTO parking_place 
                   (name, description, cpri_id, point_id) 
                   VALUES ('{}', '{}', {}, {})""".format(
            parking_place.name, parking_place.description, parking_place.cpri_id, parking_place.point_id
        )
        self.db.execute_update(query)
        self.db.disconnect()

    def setParkingPlace(self, parking_place: ParkingPlace):
        self.db.connect()
        query = """UPDATE parking_place SET 
                   name = '{}', description = '{}', cpri_id = {}, point_id = {} 
                   WHERE id = {}""".format(
            parking_place.name, parking_place.description, parking_place.cpri_id, parking_place.point_id,
            parking_place.id
        )
        self.db.execute_update(query)
        self.db.disconnect()

    def removeParkingPlace(self, id: int):
        self.db.connect()
        query = "DELETE FROM parking_place WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class RobotStandbyPositionDao:
    def __init__(self):
        self.db = DBUtil()

    def createRobotStandbyPositionFromRow(self, row):
        # 创建RobotStandbyPosition对象，包含机器人和点位信息
        return RobotStandbyPosition(
            int(row[0]),  # robot_standby_position.id
            int(row[1]),  # robot_standby_position.robot_id
            int(row[2]),  # robot_standby_position.point_id
            row[3],       # robot_standby_position.name
            row[4],       # robot_standby_position.description
            row[5],       # robot.machine_id
            row[6],       # robot.name
            row[7],       # robot.description
            row[8],       # robot.mode
            row[9],       # point.x
            row[10],      # point.y
            row[11]       # point.description
        )

    def getRobotStandbyPosition(self, id: int):
        self.db.connect()
        query = """
            SELECT rsp.id, rsp.robot_id, rsp.point_id, rsp.name, rsp.description,
                   r.machine_id, r.name AS robot_name, r.description AS robot_description, r.mode,
                   p.x, p.y, p.description AS point_description
            FROM robot_standby_position rsp
            LEFT JOIN robot r ON rsp.robot_id = r.id
            LEFT JOIN point p ON rsp.point_id = p.id
            WHERE rsp.id = {}
        """.format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createRobotStandbyPositionFromRow(row)

    def getRobotStandbyPositions(self):
        self.db.connect()
        query = """
            SELECT rsp.id, rsp.robot_id, rsp.point_id, rsp.name, rsp.description,
                   r.machine_id, r.name AS robot_name, r.description AS robot_description, r.mode,
                   p.x, p.y, p.description AS point_description
            FROM robot_standby_position rsp
            LEFT JOIN robot r ON rsp.robot_id = r.id
            LEFT JOIN point p ON rsp.point_id = p.id
        """
        result = self.db.execute_query(query)
        self.db.disconnect()

        positions = []
        for row in result:
            positions.append(self.createRobotStandbyPositionFromRow(row))
        return positions

    def getRobotStandbyPositionsByRobotId(self, robot_id: int):
        self.db.connect()
        query = """
            SELECT rsp.id, rsp.robot_id, rsp.point_id, rsp.name, rsp.description,
                   r.machine_id, r.name AS robot_name, r.description AS robot_description, r.mode,
                   p.x, p.y, p.description AS point_description
            FROM robot_standby_position rsp
            LEFT JOIN robot r ON rsp.robot_id = r.id
            LEFT JOIN point p ON rsp.point_id = p.id
            WHERE rsp.robot_id = {}
        """.format(robot_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        positions = []
        for row in result:
            positions.append(self.createRobotStandbyPositionFromRow(row))
        return positions

    def getRobotStandbyPositionsByPointId(self, point_id: int):
        self.db.connect()
        query = """
            SELECT rsp.id, rsp.robot_id, rsp.point_id, rsp.name, rsp.description,
                   r.machine_id, r.name AS robot_name, r.description AS robot_description, r.mode,
                   p.x, p.y, p.description AS point_description
            FROM robot_standby_position rsp
            LEFT JOIN robot r ON rsp.robot_id = r.id
            LEFT JOIN point p ON rsp.point_id = p.id
            WHERE rsp.point_id = {}
        """.format(point_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        positions = []
        for row in result:
            positions.append(self.createRobotStandbyPositionFromRow(row))
        return positions

    def addRobotStandbyPosition(self, rsp: RobotStandbyPosition):
        self.db.connect()
        query = """
            INSERT INTO robot_standby_position (robot_id, point_id, name, description)
            VALUES ({}, {}, '{}', '{}')
        """.format(rsp.robot_id, rsp.point_id, rsp.name, rsp.description)
        self.db.execute_update(query)
        self.db.disconnect()

    def setRobotStandbyPosition(self, rsp: RobotStandbyPosition):
        self.db.connect()
        query = """
            UPDATE robot_standby_position
            SET robot_id = {}, point_id = {}, name = '{}', description = '{}'
            WHERE id = {}
        """.format(rsp.robot_id, rsp.point_id, rsp.name, rsp.description, rsp.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removeRobotStandbyPosition(self, id: int):
        self.db.connect()
        query = "DELETE FROM robot_standby_position WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

class CarOwnerWaitZoneDao:
    def __init__(self):
        self.db = DBUtil()

    def createCarOwnerWaitZoneFromRow(self, row):
        # 创建CarOwnerWaitZone对象并包含Point信息
        return CarOwnerWaitZone(
            int(row[0]),  # car_owner_wait_zone.id
            int(row[1]),  # car_owner_wait_zone.point_id
            row[2],       # car_owner_wait_zone.name
            row[3],       # car_owner_wait_zone.description
            int(row[4]),  # point.id
            row[5],       # point.x
            row[6]        # point.y
        )

    def getCarOwnerWaitZone(self, id: int):
        self.db.connect()
        query = """
            SELECT c.id, c.point_id, c.name, c.description, p.id, p.x, p.y
            FROM car_owner_wait_zone c
            LEFT JOIN point p ON c.point_id = p.id
            WHERE c.id = {}
        """.format(id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createCarOwnerWaitZoneFromRow(row)

    def getCarOwnerWaitZoneByPointId(self, point_id: int):
        self.db.connect()
        query = """
            SELECT c.id, c.point_id, c.name, c.description, p.id, p.x, p.y
            FROM car_owner_wait_zone c
            LEFT JOIN point p ON c.point_id = p.id
            WHERE c.point_id = {}
        """.format(point_id)
        result = self.db.execute_query(query)
        self.db.disconnect()

        if len(result) == 0:
            return None
        row = result[0]
        return self.createCarOwnerWaitZoneFromRow(row)

    def getCarOwnerWaitZones(self):
        self.db.connect()
        query = """
            SELECT c.id, c.point_id, c.name, c.description, p.id, p.x, p.y
            FROM car_owner_wait_zone c
            LEFT JOIN point p ON c.point_id = p.id
        """
        result = self.db.execute_query(query)
        self.db.disconnect()

        car_owner_wait_zones = []
        for row in result:
            car_owner_wait_zones.append(self.createCarOwnerWaitZoneFromRow(row))
        return car_owner_wait_zones

    def addCarOwnerWaitZone(self, car_owner_wait_zone: CarOwnerWaitZone):
        self.db.connect()
        query = """
            INSERT INTO car_owner_wait_zone (point_id, name, description) 
            VALUES ({}, '{}', '{}')
        """.format(car_owner_wait_zone.point_id, car_owner_wait_zone.name, car_owner_wait_zone.description)
        self.db.execute_update(query)
        self.db.disconnect()

    def setCarOwnerWaitZone(self, car_owner_wait_zone: CarOwnerWaitZone):
        self.db.connect()
        query = """
            UPDATE car_owner_wait_zone 
            SET point_id = {}, name = '{}', description = '{}' 
            WHERE id = {}
        """.format(car_owner_wait_zone.point_id, car_owner_wait_zone.name, car_owner_wait_zone.description, car_owner_wait_zone.id)
        self.db.execute_update(query)
        self.db.disconnect()

    def removeCarOwnerWaitZone(self, id: int):
        self.db.connect()
        query = "DELETE FROM car_owner_wait_zone WHERE id = {}".format(id)
        self.db.execute_update(query)
        self.db.disconnect()

