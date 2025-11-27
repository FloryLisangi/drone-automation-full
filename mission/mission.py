# mission.py - DroneKit mission script
import argparse, time, math, os, sys, signal
from dronekit import connect, VehicleMode, LocationGlobalRelative
def signal_handler(sig, frame):
    print('Interrupted, exiting...')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default=os.getenv('DRONEKIT_CONN','127.0.0.1:14550'))
parser.add_argument('--alt', type=float, default=15.0)
args = parser.parse_args()

def connect_vehicle(conn):
    print('Connecting to vehicle on', conn)
    v = connect(conn, wait_ready=True, timeout=60)
    return v

def arm_and_takeoff(v, target_alt):
    print('Setting mode GUIDED and arming')
    v.mode = VehicleMode('GUIDED')
    v.armed = True
    timeout = time.time() + 30
    while not v.armed and time.time() < timeout:
        print(' waiting for arm...')
        time.sleep(1)
    if not v.armed:
        raise RuntimeError('Failed to arm')
    print('Takeoff to', target_alt)
    v.simple_takeoff(target_alt)
    while True:
        alt = v.location.global_relative_frame.alt
        print(f' Altitude: {alt:.1f} m', end='\r')
        if alt >= target_alt*0.95:
            print('\nReached target altitude')
            break
        time.sleep(1)

def goto_wait(v, lat, lon, alt, tol=2.5):
    target = LocationGlobalRelative(lat, lon, alt)
    v.simple_goto(target)
    while True:
        cur = v.location.global_relative_frame
        d = haversine(cur.lat, cur.lon, lat, lon)
        if d <= tol:
            break
        time.sleep(0.8)

def haversine(lat1, lon1, lat2, lon2):
    R=6371000.0
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2-lat1); dl = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

def main():
    v = connect_vehicle(args.connect)
    try:
        arm_and_takeoff(v, args.alt)
        lat0 = v.location.global_relative_frame.lat
        lon0 = v.location.global_relative_frame.lon
        waypoints = [
            (lat0 + 0.00012, lon0, args.alt),
            (lat0 + 0.00012, lon0 + 0.00012, args.alt),
            (lat0, lon0 + 0.00012, args.alt),
        ]
        for (la, lo, al) in waypoints:
            print('Going to', la, lo)
            goto_wait(v, la, lo, al)
            time.sleep(1)
        print('Mission complete: RTL')
        v.mode = VehicleMode('RTL')
        while v.armed:
            time.sleep(1)
    finally:
        v.close()

if __name__ == '__main__':
    main()
