import time
import systemd.daemon
from bluetoothctl import Bluetoothctl
from subprocess import Popen

def get_ds4_device(device_tuples):
    found_device = [device for device in device_tuples
            if "Wireless Controller" in device['name']]
    if found_device:
        return found_device[0]
    return {}

def is_ds4_connected(connected_device=[]):
    bt = Bluetoothctl()
    if not connected_device:
        connected_device = get_ds4_device(bt.get_paired_devices())
        print("Paired devices: ", connected_device)
        if not connected_device:
            return ()
    device_info = bt.get_device_info(connected_device['mac_address'])
    print(device_info)
    if any("Connected: yes" in info_block for info_block in device_info):
        return connected_device
    return ()



if __name__ == '__main__':

    print('Startup complete')

    connected_device = is_ds4_connected()
    while True:
        if connected_device:
            print("Device already connected. Sleep.")
            time.sleep(30)
            connected_device = is_ds4_connected(connected_device)
        else:
            bt = Bluetoothctl()
            #Scan
            print("Scanning")
            scan = Popen(["exec" " /usr/bin/bluetoothctl" " scan" " on"], shell=True)
            time.sleep(6)
            scan.kill()

            #Connect to paired device
            av_devices = bt.get_available_devices()
            print("Available devices", av_devices)
            to_connect = get_ds4_device(av_devices)
            if to_connect:
                connected = bt.connect(to_connect['mac_address'])
                print(connected)
                if connected:
                    print("Successfully connected to " + to_connect['mac_address'])
                    bt.trust(to_connect['mac_address'])
                    connected_device = to_connect
                else:
                    print("Did not connect. Wait and try again")
                    time.sleep(10)


