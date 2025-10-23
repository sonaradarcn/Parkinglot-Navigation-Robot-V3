#!/usr/bin/env python
# encoding: utf-8

import rospy
import math
import threading
from threading import Event
from robotFunction import *

class Core:
    # 静态变量：待机位置
    standby_position_x = None
    standby_position_y = None
    # 导航对象
    navigation = None
    # 用于控制检查线程暂停和恢复
    check_standby_event = Event()
    # 检查返回待机位置的线程
    check_standby_thread = None
    # 标记是否正在执行任务
    is_searching_driver = False
    is_searching_car = False
    is_searching_scan_wait = False  # 新增标记位：search_scan_wait的执行状态
    
    car_plate_no = None
    parking_place_no = None
    robot_mode = 1

    @staticmethod
    def init():
        """
        初始化函数，设置待机位置和导航对象
        """
        Core.standby_position_x = 0
        Core.standby_position_y = 0
        Core.navigation = RobotNavigation()
        Core.navigation.init()
        Core.check_standby_event.set()  # 默认线程运行
        Core.check_standby_thread = threading.Thread(target=Core.check_return_to_standby)
        Core.check_standby_thread.start()  # 启动检查线程
        

    @staticmethod
    def cancel_navigation():
        """
        取消当前导航任务并等待机器人停止
        """
        rospy.logwarn("[Core] Canceling current navigation task.")
        Core.navigation.stop_navigation()  # 停止当前的导航任务
        rospy.sleep(2)  # 给机器人一些时间来停止导航任务

    @staticmethod
    def search_car(car_x, car_y):
        """
        寻找停车位：提供停车位的 x, y 坐标，导航至目标
        """
        # 如果有其他任务正在执行，则直接返回
        if Core.is_searching_driver:
            rospy.logwarn("[Core] search_car cannot be executed because another task is running.")
            return False
        
        # 设置标记为正在寻找停车位
        Core.is_searching_driver = False
        Core.is_searching_scan_wait = False
        Core.is_searching_car = True

        # 取消当前导航任务
        Core.cancel_navigation()

        rospy.logwarn("[Core] Searching for parking at: x={}, y={}".format(car_x, car_y))

        # 暂停返回待机位置的线程
        Core.check_standby_event.clear()

        # 执行寻车操作
        Core.navigation.move_to_goal(car_x, car_y)
        
        while(RobotNavigation.check_navigation_status()==1):
            rospy.sleep(0.5)
            
        # 假设导航完成后，等待15秒
        rospy.sleep(15)

        # 恢复检查线程
        Core.check_standby_event.set()

        # 设置标记为任务完成
        Core.is_searching_driver = False
        Core.is_searching_scan_wait = False
        Core.is_searching_car = False

        return True

    @staticmethod
    def search_driver(driver_x, driver_y):
        """
        寻找车主：提供车主的 x, y 坐标，导航至车主位置
        """
        # 如果有其他任务正在执行，则直接返回
        if Core.is_searching_car:
            rospy.logwarn("[Core] search_driver cannot be executed because another task is running.")
            return False
        
        # 设置标记为正在寻找车主
        Core.is_searching_driver = True
        Core.is_searching_scan_wait = False
        Core.is_searching_car = False

        # 取消当前导航任务
        Core.cancel_navigation()

        rospy.logwarn("[Core] Searching for driver at: x={}, y={}".format(driver_x, driver_y))

        # 暂停返回待机位置的线程
        Core.check_standby_event.clear()

        # 执行寻找车主操作
        Core.navigation.move_to_goal(driver_x, driver_y)
        
        while(RobotNavigation.check_navigation_status()==1):
            rospy.sleep(0.5)

        # 找到车主后等待15秒
        rospy.sleep(15)

        # 恢复检查线程
        Core.check_standby_event.set()

        # 设置标记为任务完成      
        Core.is_searching_driver = False
        Core.is_searching_scan_wait = False
        Core.is_searching_car = False

        return True

    @staticmethod
    def search_scan_wait():
        """
        执行扫描等待操作：等待30秒，暂停检查待机位置
        """
        # 如果有其他任务正在执行，则直接返回
        if Core.is_searching_driver or Core.is_searching_car:
            rospy.logwarn("[Core] search_scan_wait cannot be executed because another task is running.")
            return False

        # 设置标记为正在执行扫描等待
        Core.is_searching_scan_wait = True
        rospy.logwarn("[Core] Starting scan wait operation in a separate thread...")

        # 取消当前导航任务
        Core.cancel_navigation()

        # 暂停返回待机位置的线程
        Core.check_standby_event.clear()

        # 创建线程来执行等待30秒的任务
        def wait_for_scan():
            rospy.sleep(30)  # 等待30秒
            # 恢复检查线程
            Core.check_standby_event.set()

            # 设置标记为任务完成
            Core.is_searching_scan_wait = False
            rospy.logwarn("[Core] Scan wait completed, returning to standby check.")

        # 启动线程执行
        threading.Thread(target=wait_for_scan).start()

        return True

    @staticmethod
    def check_return_to_standby():
        """
        检查机器人是否在待机位置 5 米范围内，如果不在则返回待机位置
        """
        while True:
            if(Core.robot_mode!=1):
                rospy.sleep(1)
                continue
            # 如果正在执行任务，则暂停
            if Core.is_searching_driver or Core.is_searching_car or Core.is_searching_scan_wait:
                rospy.loginfo("[Core] Task is running. Check standby location paused.")
                rospy.sleep(1)  # 暂停1秒，避免过于频繁的检查
                continue

            # 等待主线程通过 check_standby_event 来控制执行
            Core.check_standby_event.wait()

            current_x, current_y, _ = Core.navigation.get_current_position()
            if current_x is None or current_y is None:
                rospy.logwarn("[Core] Current position is unavailable.")
                continue

            distance_to_standby = math.sqrt((current_x - Core.standby_position_x)**2 + (current_y - Core.standby_position_y)**2)
            if distance_to_standby > 1.5:
                rospy.logwarn("[Core] Robot is more than 5 meters from standby position. Navigating back...")
                Core.navigation.move_to_goal(Core.standby_position_x, Core.standby_position_y)
                while(RobotNavigation.check_navigation_status()==1):
                    rospy.sleep(0.5)

            rospy.sleep(1)  # 每1秒检查一次
