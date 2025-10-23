#!/usr/bin/env python
# coding:utf-8
import configparser
import os
import hashlib
import qrcode
from StringIO import StringIO  # Python 2.7 中使用 StringIO
from PIL import Image, ImageDraw  # 确保导入 ImageDraw
import base64

"""
DBUtil
"""
class DBUtil:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "pnr_root"
        self.password = "abc123456"
        self.database = "sonaradar_pnr_v3"
        self.connection = None


    def connect(self):
        self.connection = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.database
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_queryWithPara(self, query, params=None):
        cursor = self.connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def execute_update(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows

    def execute_queryWithPara(self, query, params=None):
        cursor = self.connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

class ConfigUtil:
    def __init__(self, config_file='settings.ini'):
        # 初始化时，指定配置文件路径
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # 如果配置文件不存在，初始化空文件
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                f.write("[DEFAULT]\n")  # 初始化默认区块
            print("[Sonaradar-PNR-ConfigManager] Created new configuration file: {}".format(self.config_file))

    # 读取配置项
    def read(self, section, key):
        """读取指定 section 和 key 的值"""
        self.config.read(self.config_file)
        
        try:
            value = self.config.get(section, key)
            print("[Sonaradar-PNR-ConfigManager] Read value for '{}' from section '{}': {}".format(key, section, value))
            return value
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print("[Sonaradar-PNR-ConfigManager] Error reading '{}' from section '{}': {}".format(key, section, e))
            return None

    # 写入配置项
    def write(self, section, key, value):
        """写入指定 section 和 key 的值"""
        self.config.read(self.config_file)

        # 如果没有该 section，先添加
        if not self.config.has_section(section):
            self.config.add_section(section)

        # 设置 key 的值
        self.config.set(section, key, value)

        # 保存回配置文件
        with open(self.config_file, 'w') as f:
            self.config.write(f)

        print("[Sonaradar-PNR-ConfigManager] Written '{}' = '{}' to section '{}'. Configuration saved.".format(key, value, section))

    # 删除指定配置项
    def delete(self, section, key):
        """删除指定 section 中的 key"""
        self.config.read(self.config_file)

        if self.config.has_option(section, key):
            self.config.remove_option(section, key)
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            print("[Sonaradar-PNR-ConfigManager] Deleted '{}' from section '{}'. Configuration updated.".format(key, section))
        else:
            print("[Sonaradar-PNR-ConfigManager] '{}' not found in section '{}'.".format(key, section))

    # 获取所有 section
    def get_sections(self):
        """返回所有的 section"""
        self.config.read(self.config_file)
        sections = self.config.sections()
        print("[Sonaradar-PNR-ConfigManager] Sections available in the configuration: {}".format(sections))
        return sections

    # 获取指定 section 下的所有键值对
    def get_all_items(self, section):
        """返回指定 section 下的所有键值对"""
        self.config.read(self.config_file)
        if self.config.has_section(section):
            items = self.config.items(section)
            print("[Sonaradar-PNR-ConfigManager] All items in section '{}': {}".format(section, items))
            return items
        else:
            print("[Sonaradar-PNR-ConfigManager] Section '{}' not found.".format(section))
            return None
'''
# 示例使用
if __name__ == "__main__":
    # 创建 ConfigUtil 对象
    config_util = ConfigUtil()

    # 写入配置
    config_util.write("UserSettings", "username", "john_doe")
    config_util.write("UserSettings", "email", "john.doe@example.com")

    # 读取配置
    username = config_util.read("UserSettings", "username")

    # 获取所有 sections 和键值对
    sections = config_util.get_sections()
    for section in sections:
        items = config_util.get_all_items(section)

    # 删除配置项
    config_util.delete("UserSettings", "email")
'''



class MachineCodeUtil:
    @staticmethod
    def get_linux_mac_address(interface='eth0'):
        """获取 Linux 系统上指定网卡的 MAC 地址"""
        try:
            # 尝试读取指定网卡的 MAC 地址
            with open("/sys/class/net/{}/address".format(interface), 'r') as f:
                mac_address = f.read().strip()
                if mac_address:
                    print("[Sonaradar-PNR-IDCertification] Retrieved MAC address: {}".format(mac_address))
                    return mac_address
        except Exception as e:
            print("[Sonaradar-PNR-IDCertification] Error retrieving MAC address for interface {}: {}".format(interface, e))
        return None

    @staticmethod
    def get_machine_code(interface='eth0'):
        """根据网卡的 MAC 地址生成唯一机器码，长度为 15 位"""
        mac_address = MachineCodeUtil.get_linux_mac_address(interface)

        if not mac_address:
            raise Exception("[Sonaradar-PNR-IDCertification] Unable to retrieve MAC address.")

        # 使用哈希算法对 MAC 地址进行哈希
        full_hash = hashlib.sha256(mac_address).hexdigest()

        # 截取前 15 位
        machine_code = full_hash[:15]
        print("[Sonaradar-PNR-IDCertification] Generated machine code: {}".format(machine_code))
        return machine_code.upper()

'''
# 示例：获取机器码
if __name__ == "__main__":
    try:
        machine_code = MachineCodeUtil.get_machine_code()
        print("[Sonaradar-PNR-IDCertification] Unique machine code: {}".format(machine_code))
    except Exception as e:
        print("[Sonaradar-PNR-IDCertification] Error: {}".format(e))
'''

class QRCodeUtil:
    
    @staticmethod
    def generate_qr_code_image(data):
        """
        给定字符串，生成二维码并返回图像。

        :param data: 二维码中包含的数据（如网址、文本等）
        :return: 生成的二维码图像（PIL.Image 对象）
        """
        # 创建QRCode对象
        qr = qrcode.QRCode(
            version=1,  # 控制二维码的大小，1是最小的
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误修正级别
            box_size=10,  # 每个小方格的像素大小
            border=4,  # 边框大小
        )
        
        # 添加数据到二维码中
        qr.add_data(data)
        qr.make(fit=True)

        # 生成二维码的矩阵
        qr_matrix = qr.get_matrix()

        # 创建一个空白图像，背景为白色
        img = Image.new('RGB', (len(qr_matrix) * 10, len(qr_matrix) * 10), color=(255, 255, 255))

        # 创建绘图对象
        draw = ImageDraw.Draw(img)

        # 通过矩阵绘制二维码
        for y in range(len(qr_matrix)):
            for x in range(len(qr_matrix[y])):
                if qr_matrix[y][x]:  # 如果该位置是二维码的一部分
                    draw.rectangle([x * 10, y * 10, (x + 1) * 10, (y + 1) * 10], fill=(0, 0, 0))

        return img

    @staticmethod
    def image_to_base64(image):
        """
        将二维码图像转换为 base64 格式。

        :param image: 要转换的二维码图像（PIL.Image 对象）
        :return: 图像的 base64 编码字符串
        """
        # 将图像保存到一个字节流
        buffered = StringIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue())  # 不需要 decode('utf-8') 在 Python 2 中
        return img_base64
