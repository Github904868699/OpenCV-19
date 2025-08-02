import json
import socket

HOST = '127.0.0.1'
PORT = 9760

def request_photo(cam_id=0):
    with socket.create_connection((HOST, PORT)) as sock:
        cmd = json.dumps({"reqType": "photo", "camID": cam_id}) + "\n"
        sock.sendall(cmd.encode('utf-8'))
        buf = b''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                msg = json.loads(line.decode('utf-8'))
                if 'dsData' in msg:
                    for cam in msg['dsData']:
                        for det in cam.get('data', []):
                            print(f"cam {cam['camID']}: {det['label']} ({det['x']}, {det['y']})")
                else:
                    print(msg)

if __name__ == '__main__':
    request_photo()
