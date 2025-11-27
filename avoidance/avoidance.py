# avoidance.py - YOLOv8 + RealSense avoidance scaffold
import time, math, argparse
from ultralytics import YOLO
try:
    import pyrealsense2 as rs
except Exception:
    rs = None
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default=None)
parser.add_argument('--model', default='yolov8n.pt')
args = parser.parse_args()

model = YOLO(args.model)

# If RealSense present, start pipeline
pipeline = None
if rs:
    pipeline = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(cfg)

SAFE_DIST = 2.5  # meters

def get_depth_at(depth_frame, x, y):
    if depth_frame is None: return None
    depth = depth_frame.get_distance(x, y)
    return depth

try:
    while True:
        # acquire frame
        if pipeline:
            frames = pipeline.wait_for_frames(timeout_ms=5000)
            color = frames.get_color_frame()
            depth = frames.get_depth_frame()
            if not color or not depth:
                time.sleep(0.01); continue
            import numpy as np
            img = np.asanyarray(color.get_data())
        else:
            # fallback: use sample image or camera capture (not implemented)
            time.sleep(0.5); continue

        results = model(img, imgsz=640)
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy() if hasattr(r,'boxes') else []
            for box in boxes:
                x1,y1,x2,y2 = map(int,box[:4])
                cx = (x1+x2)//2; cy = (y1+y2)//2
                depth_m = get_depth_at(depth, cx, cy) if pipeline else None
                if depth_m is not None and depth_m < SAFE_DIST:
                    # compute avoidance vector (away from object)
                    img_h, img_w = img.shape[:2]
                    nx = (cx - img_w/2)/(img_w/2)
                    ny = (cy - img_h/2)/(img_h/2)
                    # simple avoidance velocities (body frame): move backward and to side
                    vx = -0.5  # backward
                    vy = -nx * 0.6
                    vz = 0.0
                    # Here: send velocity to drone (not implemented in scaffold)
                    print(f'AVOID: depth={depth_m:.2f} vx={vx} vy={vy}')
        time.sleep(0.02)
except KeyboardInterrupt:
    pass
finally:
    if pipeline:
        pipeline.stop()
