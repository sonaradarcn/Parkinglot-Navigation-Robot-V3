#!/usr/bin/env python
# coding:utf-8
import configparser
import os
import hashlib

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
            with open(f"/sys/class/net/{interface}/address", 'r') as f:
                mac_address = f.read().strip()
                if mac_address:
                    print(f"[Sonaradar-PNR-IDCertification] Retrieved MAC address: {mac_address} for interface {interface}")
                    return mac_address
        except Exception as e:
            print(f"[Sonaradar-PNR-IDCertification] Error retrieving MAC address for interface {interface}: {e}")
        return None

    @staticmethod
    def get_all_network_interfaces():
        """遍历所有网卡接口，返回所有可用接口名称"""
        interfaces = []
        try:
            # 遍历 /sys/class/net/ 目录，获取所有接口名
            for interface in os.listdir("/sys/class/net/"):
                # 排除掉 lo（本地回环接口）
                if interface != 'lo':
                    interfaces.append(interface)
        except Exception as e:
            print(f"[Sonaradar-PNR-IDCertification] Error retrieving network interfaces: {e}")
        return interfaces

    @staticmethod
    def get_machine_code():
        """根据所有可用网卡的 MAC 地址生成唯一机器码，长度为 15 位"""
        # 获取所有可用的网卡接口
        interfaces = MachineCodeUtil.get_all_network_interfaces()
        
        # 遍历每个网卡接口，尝试获取 MAC 地址
        for interface in interfaces:
            mac_address = MachineCodeUtil.get_linux_mac_address(interface)
            if mac_address:
                # 使用哈希算法对 MAC 地址进行哈希
                full_hash = hashlib.sha256(mac_address.encode()).hexdigest()

                # 截取前 15 位
                machine_code = full_hash[:15]
                print(f"[Sonaradar-PNR-IDCertification] Generated machine code: {machine_code}")
                return machine_code.upper()

        # 如果无法获取任何网卡的 MAC 地址，抛出异常
        raise Exception("[Sonaradar-PNR-IDCertification] Unable to retrieve MAC address from any network interface.")