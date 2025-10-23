#!/usr/bin/env python
# coding:utf-8
import rospy
from robotFunction import *

if __name__ == '__main__':
    # 创建节点
    print("start init")
    rospy.init_node("sonaradar_pnr_robot")
    try:
        # 实例化机器人导航器
        navigator = RobotNavigator()

        # 设置目标位置
        target_x = 12.0
        target_y = 13.0
        target_z = 0.0  # z轴的方向
        target_w = 1.0  # w轴的方向

        rospy.loginfo("current position:{}".format(navigator.get_current_position()))

        # 移动到目标位置
        navigator.move_to_goal(target_x, target_y, target_z, target_w)

        # 假设你希望停下来
        rospy.sleep(5)  # 假设5秒后停止
        navigator.stop_navigation(None)

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation interrupted.")
    print("Finished")