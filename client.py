import socket
import cv2
import numpy as np
import time
import json
import pygetwindow as gw
from pynput import keyboard

def on_press(key):
    if is_opencv_window_focused():
        print('Send key down:', key)


ip = '127.0.0.1'
port_screen = 5001
port_events = 5000

# 1. Set up the TCP socket for future events
sock_events = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock_events.connect((ip, port_events))
    print("Connected to event server (not sending anything yet).")
except Exception as e:
    print("Event server not available:", e)

# 2. Set up the UDP socket for screen streaming
sock_screen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_screen.settimeout(2)

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        msg = {"event": "mouse", "kind": "left", "x": x, "y": y}
        sock_events.sendall(json.dumps(msg).encode('utf-8'))
    elif event == cv2.EVENT_RBUTTONDOWN:
        msg = {"event": "mouse", "kind": "right", "x": x, "y": y}
        sock_events.sendall(json.dumps(msg).encode('utf-8'))
    elif event == cv2.EVENT_MBUTTONDBLCLK:
        msg = {"event": "mouse", "kind": "middle", "x": x, "y": y}
        sock_events.sendall(json.dumps(msg).encode('utf-8'))
        
def is_opencv_window_focused():
    win = gw.getActiveWindow()
    return win and win.title == 'Live Screen'
        
def keyboard_event_press(key):
    
    if not is_opencv_window_focused():
        return
    
    if key == ord('q'):
        print("Quit command received.")
        cv2.destroyAllWindows()
        listener.stop()
        exit()
    else:
        msg = {"event": "keyboard", "key": chr(key), "action": "press"}
        sock_events.sendall(json.dumps(msg).encode('utf-8'))

def keyboard_event_release(key):
    if not is_opencv_window_focused():
        return
    
    if key == ord('q'):
        print("Quit command received.")
        cv2.destroyAllWindows()
        exit()
    else:
        msg = {"event": "keyboard", "key": chr(key), "action": "release"}
        sock_events.sendall(json.dumps(msg).encode('utf-8'))

        

cv2.namedWindow("Live Screen")
cv2.setMouseCallback("Live Screen", mouse_event )
listener = keyboard.Listener(on_press=keyboard_event_press, on_release=keyboard_event_release)
listener.start()



def get_frame():
    # Request a new screenshot
    sock_screen.sendto(b'ping', (ip, port_screen))
    # Get the length of the image
    img_len_bytes, _ = sock_screen.recvfrom(1024)
    img_len = int(img_len_bytes.decode('utf-8'))
    # Receive the image data in chunks
    chunks = []
    received = 0
    while received < img_len:
        try:
            chunk, _ = sock_screen.recvfrom(4096)
            chunks.append(chunk)
            received += len(chunk)
        except socket.timeout:
            print("Timeout receiving data.")
            break
    img_bytes = b''.join(chunks)
    return img_bytes


while True:
    try:
        img_bytes = get_frame()
        # Convert PNG bytes to OpenCV image (numpy array)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow("Live Screen", frame)
        else:
            print("Error decoding frame.")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print("Error:", e)
        time.sleep(0.5)  # Wait before retrying

cv2.destroyAllWindows()
