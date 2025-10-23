#!/usr/bin/env python
# encoding: utf-8

import socket
import threading

class SocketClient:
    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 启动客户端并连接服务器
    def start(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("[Sonaradar-PNR-SocketServer] Connected to server at {}:{}".format(self.server_ip, self.server_port))

            # 启动接收服务器消息的线程
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            # 允许用户输入并发送消息
            while True:
                message = input("Enter message to send to server (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                self.send_message(message)
        
        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error connecting to server: {}".format(e))
    
    # 发送消息给服务器
    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
            print("[Sonaradar-PNR-SocketServer] Sent message to server: {}".format(message))
        except Exception as e:
            print("[Sonaradar-PNR-SocketServer] Error sending message to server: {}".format(e))
    
    # 接收来自服务器的消息
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print("[Sonaradar-PNR-SocketServer] Received from server: {}".format(message))
                else:
                    print("[Sonaradar-PNR-SocketServer] Connection to server closed.")
                    break
            except Exception as e:
                print("[Sonaradar-PNR-SocketServer] Error receiving message: {}".format(e))
                break


# 如果需要直接运行客户端
if __name__ == "__main__":
    client = SocketClient(server_ip='192.168.3.110', server_port=12000)
    client.start()
