# object_tracking.py - OpenCV KCF tracker that sends velocity setpoints via DroneKit
import argparse, cv2, time, math, os
from dronekit import connect
parser = argparse.ArgumentParser()
parser.add_argument('--camera', type=int, default=0)
parser.add_argument('--connect', default=os.getenv('DRONEKIT_CONN', None))
args = parser.parse_args()

vehicle = None
if args.connect:
    try:
        vehicle = connect(args.connect, wait_ready=False)
    except Exception as e:
        print('Vehicle connect failed:', e)
        vehicle = None

cap = cv2.VideoCapture(args.camera)
if not cap.isOpened():
    raise SystemExit('Camera not available')

ret, frame = cap.read()
if not ret:
    raise SystemExit('Failed to read first frame')

bbox = cv2.selectROI('Select target', frame, False)
tracker = cv2.TrackerKCF_create()
tracker.init(frame, bbox)

W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
Kx = 0.6
Ky = 0.6

def send_velocity_body(vx, vy, vz, duration=1.0):
    # Sends velocity in body frame (m/s) for duration seconds
    if vehicle is None:
        return
    from pymavlink import mavutil
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0,0,0,
        vx, vy, vz,
        0,0,0, 0,0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ok, box = tracker.update(frame)
        if ok:
            x,y,w,h = map(int, box)
            cx, cy = x + w//2, y + h//2
            err_x = (cx - W/2)/(W/2)
            err_y = (cy - H/2)/(H/2)
            vx = -err_y * Ky
            vy = -err_x * Kx
            send_velocity_body(vx, vy, 0)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(frame, (cx,cy), 4, (0,255,0), -1)
            cv2.putText(frame, f'vx={vx:.2f} vy={vy:.2f}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),2)
        else:
            cv2.putText(frame, 'TRACK LOST', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255),2)
        cv2.imshow('track', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    if vehicle:
        vehicle.close()
