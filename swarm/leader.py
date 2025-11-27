# leader.py - broadcast position via UDP
import socket, json, time, argparse
from dronekit import connect
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()
v = connect(args.connect, wait_ready=True)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
BROAD = ('<broadcast>', 5005)
try:
    while True:
        lat = v.location.global_relative_frame.lat
        lon = v.location.global_relative_frame.lon
        alt = v.location.global_relative_frame.alt
        msg = json.dumps({'lat':lat,'lon':lon,'alt':alt,'ts':time.time()})
        sock.sendto(msg.encode('utf8'), BROAD)
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    v.close()
    sock.close()
