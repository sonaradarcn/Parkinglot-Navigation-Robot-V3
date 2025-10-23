#!/usr/bin/env python
# encoding: utf-8

import base64
import json
import os
from bottle import Bottle, request, redirect, run, template, static_file , response
import io
from utils import *
from socketClient import *
from core import *


app = Bottle()#bottle init

# 静态文件路由
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    static_folder = os.path.join(os.path.dirname(__file__), 'views', 'static')
    return static_file(filepath, root=static_folder)

# index
@app.route('/')
def index():
    return redirect('/page/step_qrscan')

# step_qrscan
@app.route('/page/step_qrscan')
def page_step_qrscan():
    configUtil = ConfigUtil()
    print("{}/page/front_llm_chat?machine_id={}".format(configUtil.read("server","server-url"),SocketClientCommand.machine_code))
    qrCodeImage = QRCodeUtil.generate_qr_code_image("{}/page/front_llm_chat?machine_id={}".format(configUtil.read("server","server-url"),SocketClientCommand.machine_code))
    qrCodeImageBase64 = QRCodeUtil.image_to_base64(qrCodeImage)
    return template('step_qrscan',qr_code=qrCodeImageBase64,machine_id=SocketClientCommand.machine_code)

# step_wait_for_operation
@app.route('/page/step_wait_for_operation')
def page_step_wait_for_operation():
    return template('step_wait_for_operation',machine_id=SocketClientCommand.machine_code)

# step_search_car
@app.route('/page/step_search_car')
def page_step_search_car():
    return template('step_search_car',machine_id=SocketClientCommand.machine_code,parking_place_no=Core.parking_place_no,car_plate_no=Core.car_plate_no)

# step_search_car
@app.route('/page/step_search_owner')
def page_step_search_owner():
    return template('step_search_owner',machine_id=SocketClientCommand.machine_code)

# step_message_show
@app.route('/page/step_message_show')
def page_step_search_owner():
    return template('step_message_show',machine_id=SocketClientCommand.machine_code)

# step_off_service
@app.route('/page/step_off_service')
def page_step_off_service():
    return template('step_off_service',machine_id=SocketClientCommand.machine_code)

# step_debug
@app.route('/page/step_debug')
def page_step_debug():
    return template('step_debug',machine_id=SocketClientCommand.machine_code)

# WEBUI自动跳转控制函数
@app.route('/api/turn_next_page', method='GET')
def check_condition_endpoint():
    step_name = request.query.get('step_name')  # 获取查询参数 step_name
    if not step_name:
        return {'error': 'step_name 参数缺失'}
    
    if Core.robot_mode == 0:
        if(step_name=='step_off_service'):
            return {}
        return {'redirectUrl': '../page/step_off_service'}
    
    if Core.robot_mode == 2:
        if(step_name=='step_debug'):
            return {}
        return {'redirectUrl': '../page/step_debug'}
    
    if Core.is_searching_car==False and Core.is_searching_driver==False and Core.is_searching_scan_wait==False:
        if(step_name=='step_qrscan'):
            return {}
        return {'redirectUrl': '../page/step_qrscan'}
    elif Core.is_searching_car==True and Core.is_searching_driver==False:
        if(step_name=='step_search_car'):
            return {}
        return {'redirectUrl': '../page/step_search_car'}
    elif Core.is_searching_car==False and Core.is_searching_driver==True:
        if(step_name=='step_search_owner'):
            return {}
        return {'redirectUrl': '../page/step_search_owner'}
    elif Core.is_searching_car==False and Core.is_searching_driver==False and Core.is_searching_scan_wait==True:
        if(step_name=='step_wait_for_operation'):
            return {}
        return {'redirectUrl': '../page/step_wait_for_operation'}
    else:
        return {}




    

# 测试方法
if __name__ == '__main__':
    rospy.init_node('sonaradar_pnr_robot')
    configUtil = ConfigUtil()
    # 启动客户端并连接服务器
    SocketClientCommand.start_socket(configUtil.read("server","server-ip"), 12000)
    
    #核心启动
    Core.init()
    
    
    #启动bottle服务端
    run(app, host='192.168.149.1', port=12002)
    # run(app, host=SocketClientCommand.get_local_ip(), port=12002)