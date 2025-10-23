import subprocess
import wave
import pymysql as MySQLdb
from entity import *
import edge_tts
import asyncio
import asyncio
import pyttsx3
from io import BytesIO
import os
from pydub import AudioSegment

import base64
from PIL import Image

import json
import random
from dashscope import Generation


"""
DBUtil 数据库辅助类
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

    def execute_update_1(self, query, params=None):
        cursor = self.connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
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


class TTSUtils:
    @staticmethod
    def text_to_speech(text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # 使用默认语音
        # 创建一个临时文件保存语音
        temp_wav = "resources/temp_audio.wav"
        temp_mp3 = "resources/temp_audio.mp3"

        engine.save_to_file(text, temp_wav)
        engine.runAndWait()

        # 转换WAV到MP3
        audio = AudioSegment.from_wav(temp_wav)
        audio.export(temp_mp3, format="mp3")

        # 从MP3文件读取bytes
        with open(temp_mp3, 'rb') as f:
            audio_bytes = f.read()

        # 删除临时文件
        os.remove(temp_wav)
        os.remove(temp_mp3)

        return audio_bytes

    @staticmethod
    def tts(text: str) -> bytes:
        try:
            voice = 'zh-CN-XiaoyiNeural'
            output_file = "resources/output_tts.mp3"

            communicate = edge_tts.Communicate(text, voice)

            # Create a new event loop and run the coroutine
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(communicate.save(output_file))
            loop.close()

            # Read the file's content
            with open(output_file, 'rb') as f:
                data = f.read()

            return data
        except Exception as e:
            #没网了用本地
            print('[Sonaradar-PNR-Plus]error while generate sound,reason:{}'.format(e))
            return TTSUtils.text_to_speech(text)

    @staticmethod
    def merge_audios(audio_bytes1: bytes, audio_bytes2: bytes) -> bytes:
        buf1 = BytesIO(audio_bytes1)
        buf2 = BytesIO(audio_bytes2)

        audio1 = AudioSegment.from_file(buf1, format='mp3')  # specify format if needed
        audio2 = AudioSegment.from_file(buf2, format='mp3')  # specify format if needed

        merged_audio = audio1 + audio2

        buf = BytesIO()
        merged_audio.export(buf, format='mp3')  # Assuming the audio format is MP3, adjust if necessary
        return buf.getvalue()

    @staticmethod
    def read_mp3_as_bytes(file_path: str) -> bytes:
        with open(file_path, 'rb') as f:
            return f.read()

    @staticmethod
    def autoTTS(txt: str, filepath: str) -> bytes:
        ttsFile = TTSUtils.tts(txt)
        tipSound = TTSUtils.read_mp3_as_bytes('resources/tip_sound.mp3')
        merged_audio = TTSUtils.merge_audios(tipSound, ttsFile)

        # Save the merged audio to a file if output_file is provided
        output_file = filepath
        with open(output_file, 'wb') as f:
            f.write(merged_audio)

        return merged_audio


class ImageUtil:

    @staticmethod
    def read_image(file_path):
        """读取图片文件并返回 PIL Image 对象"""
        try:
            with Image.open(file_path) as img:
                print("[Sonaradar-PNR-ImageUtil] 图片成功读取: {}".format(file_path))
                return img
        except Exception as e:
            print("[Sonaradar-PNR-ImageUtil] 读取图片时发生错误: {}".format(e))
            return None

    @staticmethod
    def save_image(image, save_path):
        """将 PIL Image 对象保存到本地"""
        try:
            image.save(save_path)
            print("[Sonaradar-PNR-ImageUtil] 图片成功保存到: {}".format(save_path))
        except Exception as e:
            print("[Sonaradar-PNR-ImageUtil] 保存图片时发生错误: {}".format(e))

    @staticmethod
    def image_to_base64(image):
        """将 PIL Image 对象转换为 base64 编码"""
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")  # 可以根据需要调整格式
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            print("[Sonaradar-PNR-ImageUtil] 图片成功转换为 base64 编码")
            return img_base64
        except Exception as e:
            print("[Sonaradar-PNR-ImageUtil] 图片转 base64 时发生错误: {}".format(e))
            return None

    @staticmethod
    def base64_to_image(base64_str):
        """将 base64 编码的字符串转换为 PIL Image 对象"""
        try:
            img_data = base64.b64decode(base64_str)
            image = Image.open(BytesIO(img_data))
            print("[Sonaradar-PNR-ImageUtil] 成功将 base64 转换为图片")
            return image
        except Exception as e:
            print("[Sonaradar-PNR-ImageUtil] base64 转图片时发生错误: {}".format(e.with_traceback()))
            return None





