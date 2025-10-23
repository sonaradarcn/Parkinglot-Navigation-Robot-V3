#!/usr/bin/env python
# encoding: utf-8

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseStamped
from actionlib_msgs.msg import GoalStatus, GoalStatusArray
import math

class RobotNavigation:
    # 类变量，所有对象共享
    cmd_vel_pub = rospy.Publisher('/jetauto_1/cmd_vel', Twist, queue_size=10)
    #odom_sub = rospy.Subscriber('/jetauto_1/odom', Odometry, lambda msg: RobotNavigation.odom_callback(msg))
    goal_pub = rospy.Publisher('/jetauto_1/move_base_simple/goal', PoseStamped, queue_size=10)
    status_sub = rospy.Subscriber('/jetauto_1/move_base/status', GoalStatusArray, lambda msg: RobotNavigation.move_base_status_callback(msg))
    
    last_velocity = None
    odom_sub_1 = None
    
    
    # 类级变量来保存状态
    current_pose = None
    goal_pose = None
    
    @staticmethod
    def init():
        """初始化 ROS 订阅"""
        if RobotNavigation.odom_sub_1 is None:
            RobotNavigation.odom_sub_1 = rospy.Subscriber(
                '/jetauto_1/odom', 
                Odometry, 
                RobotNavigation.odom_callback_1
            )

    @staticmethod
    def odom_callback(msg):
        # 获取机器人的当前位置
        RobotNavigation.current_pose = msg.pose.pose

    @staticmethod
    def get_current_position():
        # 输出当前坐标
        if RobotNavigation.current_pose:
            rospy.loginfo("[Sonaradar-PNR-NavigationModule] Current position: x={}, y={}, z={}".format(
                RobotNavigation.current_pose.position.x, RobotNavigation.current_pose.position.y, RobotNavigation.current_pose.position.z))
            return RobotNavigation.current_pose.position.x, RobotNavigation.current_pose.position.y, RobotNavigation.current_pose.position.z
        else:
            rospy.loginfo("[Sonaradar-PNR-NavigationModule] Current position is not available.")
            return None, None, None

    @staticmethod
    def move_to_goal(goal_x, goal_y, goal_z=0.0):
        RobotNavigation.wait_for_move_base()  # 等待 move_base 准备好

        goal = PoseStamped()
        goal.header.frame_id = 'jetauto_1/map'  # 使用 jetauto_1/map 作为坐标系
        goal.header.stamp = rospy.Time.now()  # 获取最新的时间戳
        goal.pose.position.x = goal_x
        goal.pose.position.y = goal_y
        goal.pose.position.z = goal_z
        goal.pose.orientation.w = 1.0  # 保持朝向为默认方向

        rospy.loginfo("[Sonaradar-PNR-NavigationModule] Publishing goal: x={}, y={}, z={}".format(goal_x, goal_y, goal_z))
        RobotNavigation.goal_pub.publish(goal)

        RobotNavigation.goal_pose = goal.pose  # 保存目标位置

        rospy.loginfo("[Sonaradar-PNR-NavigationModule] Goal Published: {}".format(goal))
        rospy.sleep(2)  # 确保目标已发布

    @staticmethod
    def stop_navigation():
        # 停止导航
        RobotNavigation.cmd_vel_pub.publish(Twist())
        rospy.loginfo("[Sonaradar-PNR-NavigationModule] Navigation stopped.")
        
    @staticmethod
    def wait_for_move_base():
        rospy.loginfo("[Sonaradar-PNR-NavigationModule] Waiting for move_base to be ready...")
        while not rospy.is_shutdown():
            try:
                # 检查move_base是否能接受目标
                if RobotNavigation.goal_pub.get_num_connections() > 0:
                    rospy.loginfo("[Sonaradar-PNR-NavigationModule] move_base is ready!")
                    break
            except rospy.ROSException as e:
                rospy.logwarn("[Sonaradar-PNR-NavigationModule] Error checking move_base connection: {}".format(e))
            rospy.sleep(1)

    @staticmethod
    def move_base_status_callback(msg):
        
        # rospy.loginfo("[Sonaradar-PNR-NavigationModule] move_base status: {}".format(msg.status_list))
        # 可以进一步分析 move_base 的状态变化，查看是否有 GoalStatus 更新
        pass

    @staticmethod
    def get_distance_to_goal():
        """
        计算当前位置与目标位置之间的欧几里得距离
        """
        if RobotNavigation.current_pose and RobotNavigation.goal_pose:
            current_x = RobotNavigation.current_pose.position.x
            current_y = RobotNavigation.current_pose.position.y
            goal_x = RobotNavigation.goal_pose.position.x
            goal_y = RobotNavigation.goal_pose.position.y

            # 欧几里得距离
            distance = math.sqrt((goal_x - current_x)**2 + (goal_y - current_y)**2)
            rospy.loginfo("[Sonaradar-PNR-NavigationModule] Distance to goal: {:.2f} meters".format(distance))
            return distance
        else:
            rospy.logwarn("[Sonaradar-PNR-NavigationModule] Cannot calculate distance: current pose or goal pose is missing.")
            return None

    # @staticmethod
    # def check_navigation_status():
    #     """
    #     检测导航状态
    #     - 返回值：
    #         - 0：目标已到达
    #         - 1：导航中
    #         - 2：导航失败
    #     """
    #     if RobotNavigation.current_pose and RobotNavigation.goal_pose:
    #         distance = RobotNavigation.get_distance_to_goal()
    #         if distance is None:
    #             return 2  # 如果没有目标，返回失败

    #         # 判断是否到达目标，假设距离小于2米视为已到达
    #         if distance < 9999:
    #             rospy.loginfo("[Sonaradar-PNR-NavigationModule] Robot has reached the goal!")
    #             return 0  # 到达目标
    #         else:
    #             rospy.loginfo("[Sonaradar-PNR-NavigationModule] Robot is moving towards the goal...")
    #             return 1  # 继续导航
    #     else:
    #         rospy.logwarn("[Sonaradar-PNR-NavigationModule] Navigation status cannot be determined: current pose or goal pose is missing.")
    #         return 2  # 如果没有位置信息，返回失败
    
    @staticmethod
    def odom_callback_1(msg):
        """更新速度信息"""
        RobotNavigation.last_velocity = msg.twist.twist
        RobotNavigation.current_pose = msg.pose.pose

    @staticmethod
    def check_navigation_status():
        """
        检测导航状态（基于速度）
        - 返回值：
            - 0：机器人已停止（可能到达目标）
            - 1：正在移动
            - 2：未知状态
        """
        if RobotNavigation.last_velocity is None:
            rospy.logwarn("[Sonaradar-PNR-NavigationModule] No odometry data received yet!")
            return 2

        linear_speed = abs(RobotNavigation.last_velocity.linear.x)
        angular_speed = abs(RobotNavigation.last_velocity.angular.z)

        if linear_speed < 0.01 and angular_speed < 0.01:
            rospy.loginfo("[Sonaradar-PNR-NavigationModule] Robot has stopped (possibly reached goal).")
            return 0
        else:
            rospy.loginfo("[Sonaradar-PNR-NavigationModule] Robot is moving...")
            return 1

# if __name__ == "__main__":
#     rospy.init_node('robot_navigation_node')

#     # 输出当前坐标
#     print("Current Position: {}".format(RobotNavigation.get_current_position()))

#     # 假设目标位置为(2.0, 3.0, 0.0)
#     RobotNavigation.move_to_goal(2.0, 3.0)

#     # 等待导航完成
#     rospy.sleep(5)

#     # 输出当前坐标
#     print("Current Position: {}".format(RobotNavigation.get_current_position()))

#     # 检查导航状态
#     nav_status = RobotNavigation.check_navigation_status()
#     if nav_status == 0:
#         print("The robot has reached the goal.")
#     elif nav_status == 1:
#         print("The robot is still moving towards the goal.")
#     else:
#         print("Navigation failed.")

#     # 停止导航
#     RobotNavigation.stop_navigation()
