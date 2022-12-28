from tello import Tello
import sys
from datetime import datetime
from netifaces import interfaces, AF_INET, ifaddresses
import time

def find_local_addr():
    network_segment="192.168.10.x"
    retry_count = 0
    while True:
        process_network_segment = ""
        for i in range(0,len(network_segment)):
            if (i != len(network_segment)-1 and i != len(network_segment)-2):
                process_network_segment += network_segment[i]
        for ifaceName in interfaces():
            try:
                if process_network_segment in ifaddresses(ifaceName)[AF_INET][0]['addr']:
                    if (retry_count != 0):
                        print("")
                    print("Found local address [{0}]".format(ifaddresses(ifaceName)[AF_INET][0]['addr']))
                    return ifaddresses(ifaceName)[AF_INET][0]['addr']
            except:
                retry_count += 1
                print(".", end = "")
                time.sleep(0.01)

start_time = str(datetime.now())

f = open("./command.txt", "r")
commands = f.readlines()

drone = Tello(find_local_addr(),8889)
for command in commands:
    if command != '' and command != '\n':
        command = command.rstrip()

        if command.find('delay') != -1:
            sec = float(command.partition('delay')[2])
            print('delay {0}'.format(sec))
            time.sleep(sec)
            pass
        else:
            drone.send_command(command)