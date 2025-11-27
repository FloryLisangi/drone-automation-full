# follower.py - listen to leader and follow with fixed offset
import socket, json, time, math, argparse
from dronekit import connect, LocationGlobalRelative
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14551')
args = parser.parse_args()
v = connect(args.connect, wait_ready=True)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',5005))
OFF_EAST = 5.0
OFF_NORTH = 0.0
def add_offset(lat, lon, north_m, east_m):
    dlat = north_m / 111111.0
    dlon = east_m / (111111.0 * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon

try:
    while True:
        data, _ = sock.recvfrom(4096)
        info = json.loads(data.decode('utf8'))
        lat, lon, alt = info['lat'], info['lon'], info['alt']
        tgt_lat, tgt_lon = add_offset(lat, lon, OFF_NORTH, OFF_EAST)
        v.simple_goto(LocationGlobalRelative(tgt_lat, tgt_lon, alt))
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    v.close()
    sock.close()
