import argparse
import datetime
import sys
import time
import signal
import atexit

from pythonosc import dispatcher
from pythonosc import osc_server

from pythonosc import udp_client

TITLE = 'clock_rabbit_osc_sender'
VERSION = 2

DEFAULT_SEND_IP = "127.0.0.1"
DEFAULT_SEND_PORT = 9000

DEFAULT_RECEIVE_IP = "127.0.0.1"
DEFAULT_RECEIVE_PORT = 9001

def sig_handler(signum, frame) -> None:
    detect_exit()
    sys.exit(1)

def main():

    print(TITLE + ' ' + 'v' + str(VERSION))

    parser = argparse.ArgumentParser()
    parser.add_argument("--send-ip", default=DEFAULT_SEND_IP, help="The IP address of the OSC server to send to")
    parser.add_argument("--send-port", type=int, default=DEFAULT_SEND_PORT, help="The port number of the OSC server to send to")
    # parser.add_argument("--receive-ip", default=DEFAULT_RECEIVE_IP, help="The IP address to listen on for OSC messages")
    # parser.add_argument("--receive-port", type=int, default=DEFAULT_RECEIVE_PORT, help="The port number to listen on for OSC messages")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.send_ip, args.send_port)

    def loop():
        while True:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute

            hour0 = hour // 10
            hour1 = hour % 10
            minute0 = minute // 10
            minute1 = minute % 10

            client.send_message("/avatar/parameters/OSC_hour0", hour0)
            client.send_message("/avatar/parameters/OSC_hour1", hour1)
            client.send_message("/avatar/parameters/OSC_minute0", minute0)
            client.send_message("/avatar/parameters/OSC_minute1", minute1)

            print("\r" + str(hour0) + str(hour1) + ':' + str(minute0) + str(minute1), end="")
            time.sleep(1)

    def detect_exit():
        client.send_message("/avatar/parameters/OSC_hour0", 10)
        client.send_message("/avatar/parameters/OSC_hour1", 10)
        client.send_message("/avatar/parameters/OSC_minute0", 10)
        client.send_message("/avatar/parameters/OSC_minute1", 10)

    atexit.register(detect_exit)
    signal.signal(signal.SIGTERM, sig_handler)

    try:
        loop()

    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        detect_exit()

        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":

    sys.exit(main())
