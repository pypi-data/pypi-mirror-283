import cv2
import socket
import pickle
import struct
import threading
import pyautogui
import numpy as np
import pyautogui as pg
from pynput.keyboard import Listener
from rcps.utils.utils import print_colored
from rcps.utils._key_maps import convert_key_to_str, convert_key
                                
class StreamingServer:
    def __init__(self, host, port, slots=8, quit_key='q'):
        self.__host = host
        self.__port = port
        self.__slots = slots
        self.__used_slots = 0
        self.__running = False
        self.__quit_key = quit_key
        self.__block = threading.Lock()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init_socket()

    def __init_socket(self):
        self.__server_socket.bind((self.__host, self.__port))

    def start_server(self):
        if self.__running:
            print("Server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()

    def __server_listening(self):
        self.__server_socket.listen()
        while self.__running:
            self.__block.acquire()
            connection, address = self.__server_socket.accept()
            if self.__used_slots >= self.__slots:
                print("Connection refused! No free slots!")
                connection.close()
                self.__block.release()
                continue
            else:
                print_colored("Connection accepted!")
                self.__used_slots += 1
            self.__block.release()
            thread = threading.Thread(target=self.__client_connection, args=(connection, address,))
            thread.start()

    def stop_server(self):
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
        else:
            print("Server not running!")

    def __client_connection(self, connection, address):
        def show(key):
            self.key_str = convert_key_to_str(key)
            connection.sendall(self.key_str.encode('utf-8'))

        def listen_keys():
            with Listener(on_press=show) as listener:
                listener.join()

        key_thread = threading.Thread(target=listen_keys)
        key_thread.start()

        payload_size = struct.calcsize('>L')
        data = b""

        while self.__running:
            break_loop = False
            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    self.__used_slots -= 1
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(address), frame)
            if cv2.waitKey(1) == ord(self.__quit_key):
                connection.close()
                self.__used_slots -= 1
                break

        key_thread.join()
            
          
class StreamingClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self._configure()
        self.__running = False
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        return None

    def _cleanup(self):
        cv2.destroyAllWindows()

    def __client_streaming(self):
        self.__client_socket.connect((self.__host, self.__port))
        
        while self.__running:
            
            def get_and_run_key():
                key = self.__client_socket.recv(1024).decode('utf-8')
                key = convert_key(key)
                
                if key is not None:
                    pg.press(key)
                    
            key_thread = threading.Thread(target=get_and_run_key)
            key_thread.start()
                
            frame = self._get_frame()
            _, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self.__client_socket.send(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False

        key_thread.join()
        self._cleanup()

    def start_stream(self):
        if self.__running:
            print("Client is already streaming!")
        else:
            print_colored("Client is streaming!")
            self.__running = True
            client_thread = threading.Thread(target=self.__client_streaming)
            client_thread.start()

    def stop_stream(self):
        if self.__running:
            self.__running = False
        else:
            print("Client not streaming!")
            
class ScreenShareClient(StreamingClient):
    def __init__(self, host, port, x_res=1024, y_res=576):
        self.__x_res = x_res
        self.__y_res = y_res
        super(ScreenShareClient, self).__init__(host, port)

    def _get_frame(self):
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.__x_res, self.__y_res), interpolation=cv2.INTER_AREA)
        return frame          



if __name__ == "__main__":
    def start_server():
        server = StreamingServer("127.0.0.1", 8888, slots=4, quit_key='q')
        server.start_server()
    
    def start_screen_share_client():
        screen_share_client = ScreenShareClient("127.0.0.1", 8888, x_res=1024, y_res=576)
        screen_share_client.start_stream()

    start_server()
    start_screen_share_client()