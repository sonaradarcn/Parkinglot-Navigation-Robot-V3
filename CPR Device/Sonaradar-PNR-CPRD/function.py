import cv2
# pip install ultralytics[export] -i https://pypi.tuna.tsinghua.edu.cn/simple
from ultralytics import YOLO
# pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple
from paddleocr import PaddleOCR, draw_ocr

import base64
from utils import *
import io
import requests

class CarPlateDetection:
    @staticmethod
    def autorun(cpri_coordinates):
        configUtil = ConfigUtil()
        if(configUtil.read('function', 'recognization_enable')==0):
            return
        image = CarPlateDetection.capture_image_from_camera(int(configUtil.read('camera', 'index')))
        coordinates = CarPlateDetection.detect_car_plate(image=image)
        if coordinates:
            for (result_x1, result_y1, result_x2, result_y2) in coordinates:
                for cpri_coordinate in cpri_coordinates:
                    if(result_x1>=cpri_coordinate['x1'] and result_y1>=cpri_coordinate['y1']):
                        if(result_x2<=cpri_coordinate['x2'] and result_y2<=cpri_coordinate['y2']):
                            imageDetect = CarPlateDetection.crop_image(image,result_x1,result_y1,result_x2,result_y2)
                            strResult = CarPlateDetection.recognize_car_plate_number(imageDetect)
                            imageRect = image
                            occupyFlag = 0
                            if(strResult.replace(" ","")!=''):
                                print("[Sonaradar-PNR-CPRService] Car plate detected! String:{}".format(strResult))
                                imageRect = CarPlateDetection.draw_rectangle_on_image(image,[(result_x1,result_y1,result_x2,result_y2)])
                                occupyFlag = 1
                            """
                            上传数据，包括图片和其他表单数据
                            """
                            url = 'http://{}:8080/api/cpri_upload'.format(configUtil.read('server', 'ip'))  # 替换为你自己的 API 地址
        
                            # 加载图片
                            if imageRect is None:
                                print("Failed to load image.")
                                return
        
                            # 将图像转换为字节流格式（JPEG格式）
                            _, img_encoded = cv2.imencode('.jpg', imageRect)
                            img_bytes = img_encoded.tobytes()  # 转换为字节数组
        
                            # 创建表单数据
                            data = {
                                'id': cpri_coordinate['id'],  # CPR ID
                                'occupying_flag': occupyFlag,  # 占用状态，1表示占用，0表示空闲
                                'carplate_no': strResult,  # 车牌号
                            }
        
                            # 将图片作为文件上传
                            files = {'image': ('image.jpg', io.BytesIO(img_bytes), 'image/jpeg')}
        
                            # 发送 POST 请求
                            requests.post(url, data=data, files=files)
                            
        
    
    @staticmethod
    def detect_car_plate(image, model_path="best.pt"):
        """
        从图片中识别车牌，返回车牌区域的坐标（x1, y1, x2, y2）
        如果识别出多个车牌，则返回一个包含多个坐标元组的列表
        """
        # 加载YOLOv11模型
        model = YOLO('Sonaradar_CP_Model_YOLOv11.pt')
        
        # 使用YOLO模型进行车牌检测
        results = model(image)
        
        # 获取检测框的坐标
        car_plate_coordinates = []
        for result in results[0].boxes:
            # x1, y1, x2, y2 坐标
            x1, y1, x2, y2 = result.xyxy[0]
            car_plate_coordinates.append((int(x1), int(y1), int(x2), int(y2)))

        return car_plate_coordinates

    @staticmethod
    def load_image(image_path):
        """
        从本地文件读取图片并返回图片数据
        """
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load the image from {image_path}")
            return None
        return image
    
    @staticmethod
    def crop_image(image, x1, y1, x2, y2):
        """
        根据给定的坐标 (x1, y1, x2, y2) 对图片进行裁剪，返回裁剪后的图片
        """
        # 确保坐标是有效的
        if x1 < 0 or y1 < 0 or x2 > image.shape[1] or y2 > image.shape[0]:
            print("Error: Invalid crop coordinates.")
            return None
        
        # 对图片进行裁剪，切片形式 [y1:y2, x1:x2]
        cropped_image = image[y1:y2, x1:x2]
        return cropped_image

    @staticmethod
    def recognize_car_plate_number(image):
        """
        使用PaddleOCR从图片中识别车牌号
        """
        # 初始化PaddleOCR模型
        ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 使用PaddleOCR的中文识别

        # 使用PaddleOCR识别文本
        result = ocr.ocr(image, cls=True)

        # 处理识别结果并提取车牌号
        car_plate_numbers = []
        for line in result[0]:
            text = line[1][0]
            car_plate_numbers.append(text)

        # 将车牌号列表转换为一个字符串，使用空格或其他分隔符
        car_plate_str = ''.join(car_plate_numbers)  # 使用空格分隔
        # 或者使用逗号等其他分隔符
        # car_plate_str = ', '.join(car_plate_numbers)

        return car_plate_str

    @staticmethod
    def save_image(image, output_path):
        """
        保存图片到指定路径
        """
        cv2.imwrite(output_path, image)
        print(f"Image saved as {output_path}")

    @staticmethod
    def draw_rectangle_on_image(image, coordinates):
        """
        在图片上绘制橘色矩形框，传入图片和车牌区域坐标（x1, y1, x2, y2），返回修改后的图片
        """
        for (x1, y1, x2, y2) in coordinates:
            # 绘制橘色矩形框
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 165, 255), 10)  # BGR: 橘色 (0, 165, 255)
        return image

    @staticmethod
    def get_available_cameras():
        """
        获取计算机上所有可用的摄像头索引
        """
        available_cameras = []
        for index in range(10):  # 假设最多有10个摄像头
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                available_cameras.append(index)
                cap.release()
        return available_cameras
    
    @staticmethod
    def get_camera_info():
        """
        获取计算机上所有可用摄像头的索引、名称、描述等信息
        """
        camera_info = []
        for index in range(20):  # 假设最多有10个摄像头
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                camera_details = {
                    'index': index,
                    'width': cap.get(cv2.CAP_PROP_FRAME_WIDTH),  # 获取摄像头的宽度
                    'height': cap.get(cv2.CAP_PROP_FRAME_HEIGHT),  # 获取摄像头的高度
                    'fps': cap.get(cv2.CAP_PROP_FPS),  # 获取帧率
                    'fourcc': cap.get(cv2.CAP_PROP_FOURCC)  # 获取编码格式
                }
                # 获取更多信息（如描述和设备名称）是有限的，可以添加其他自定义属性
                camera_info.append(camera_details)
                cap.release()
        return camera_info

    @staticmethod
    def capture_image_from_camera(camera_index=0):
        return CarPlateDetection.load_image('test/z6.jpg')
        """
        从指定的摄像头拍照，并返回图像
        默认使用索引 0 作为摄像头
        """
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"Error: Could not open camera with index {camera_index}")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return frame
        else:
            print(f"Error: Failed to capture image from camera {camera_index}")
            return None
        
    @staticmethod
    def image_to_base64(image):
        """
        将图像转换为 Base64 格式
        :param image: 输入的图像（OpenCV 格式）
        :return: 返回 Base64 编码后的字符串
        """
        if image is None:
            return None
        
        # 将图像编码为 JPEG 格式
        _, buffer = cv2.imencode('.jpg', image)
        
        # 将图像转为 Base64 编码
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return image_base64


# 使用示例：
if __name__ == "__main__":
    # # 获取可用摄像头索引
    cameras = CarPlateDetection.get_available_cameras()
    print(f"Available cameras: {cameras}")

    # 从默认摄像头拍照
    if cameras:
        print(cameras[0])
        image = CarPlateDetection.capture_image_from_camera(cameras[0])
        if image is not None:
            # 保存图片
            CarPlateDetection.save_image(image, "captured_image.jpg")
    #image = CarPlateDetection.load_image('test/z6.jpg')
    coordinates = CarPlateDetection.detect_car_plate(image=image)
    image = CarPlateDetection.draw_rectangle_on_image(image=image,coordinates=coordinates)
    CarPlateDetection.save_image(image,'test/z7.jpg')
