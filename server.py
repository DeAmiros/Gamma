# udp_tcp_screen_server.py
import os
import socket
import threading
from PIL import ImageGrab
import io
import json
import pyautogui as pag
from pynput import keyboard as kb

ip = '0.0.0.0'
port_screen = 5001
port_events = 5000

# TCP socket for events (not used yet, just setup)
sock_events = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_events.bind((ip, port_events))
sock_events.listen(1)
print(f"Event socket listening on TCP port {port_events}")

sock_events_conn, addr = sock_events.accept()

def handle_events():
    while True:
        data = sock_events_conn.recv(1024)
        if not data:
            continue
        data =  json.loads(data.decode('utf-8'))
        if data['event'] == 'mouse':
            pag.click(x=data['x'], y=data['y'], button=data['kind'])
        elif data['event'] == 'keyboard':
            if data['key'] == 'q':
                print("Quit command received from client.")
                os._exit(0)
            else:
                if data['action'] == 'press':
                    kb.Controller().press(data['key'])
                elif data['action'] == 'release':
                    kb.Controller().release(data['key'])
            

sock_screen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_screen.bind((ip, port_screen))
print(f"Screen socket ready on UDP port {port_screen}")

def handle_screen():

    while True:
        data, addr = sock_screen.recvfrom(1024)
        print("Screen ping from", addr)
        img = ImageGrab.grab()
        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes = img_bytes_io.getvalue()

        img_len = len(img_bytes)
        sock_screen.sendto(str(img_len).encode('utf-8'), addr)
        for i in range(0, img_len, 4096):
            chunk = img_bytes[i:i+4096]
            sock_screen.sendto(chunk, addr)
        print("Screenshot sent to", addr)

# Start screen handler thread
threading.Thread(target=handle_screen, daemon=True).start()
threading.Thread(target=handle_events, daemon=True).start()

# You can add event handling here in the future!
print("Server running. Ready for screen share and future events.")
threading.Event().wait()  # Keep main thread alive
