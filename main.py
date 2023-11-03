# This is a sample Python script.
import json
import time

import serial
import sys
import threading
import mqtt

status = '$LICMD,1,1*4F\r\n'
turn_on = '$LICMD,2,1*4C\r\n'
turn_off = '$LICMD,3,1*4D\r\n'
light_reset = '$LICMD,4,1*4A\r\n'
floating_light = '$LICMD,5,1*4B\r\n'


def open_serial(device, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
    ss = serial.Serial()
    ss.port = device
    ss.baudrate = baudrate
    ss.bytesize = bytesize
    ss.parity = parity
    ss.stopbits = stopbits
    ss.timeout = timeout
    ss.xonxoff = xonxoff
    ss.rtscts = rtscts
    ss.dsrdtr = dsrdtr
    ss.open()
    return ss


def read(ss, timeout=1):
    ss.timeout = timeout
    rx = ss.readline().decode()
    return rx


def connect_serial_device(cmd):
    # ser = open_serial('/dev/ttyUSB0')
    ser.write(cmd.encode())
    result = read(ser)
    if len(result) <= 0:
        result = 'error, try again'
    else:
        if cmd == status:
            parsing = result.split(',')
            if dataForm == 'json':
                result = json.dumps(
                    {
                        "v": parsing[1],
                        "A": parsing[2],
                        "CSD": parsing[3],
                        "ON/OFF": parsing[4],
                        "Character": parsing[5],
                        "Latitude": parsing[8],
                        "Longitude": parsing[9][:4]
                    }, indent=4
                )
            else:
                result = ("V : " + parsing[1] + ', A : ' + parsing[2] + ', CDS : ' + parsing[3] +
                          ', ON/OFF : ' + parsing[4] + ', Character : ' + parsing[5] +
                          ', Latitude : ' + parsing[8] + ', Longitude : ' + parsing[9][:4])
    # print(result2)
    # print('result : ', result)
    return result


def published_message(msg, topic_pub):
    publisher = mqtt.Publisher()
    publisher.start(host_url, port)
    publisher.publish(topic_pub, msg)


def pub_status_schedule(topic, cnt):
    while True:
        msg = connect_serial_device(status)
        published_message(msg, topic)
        time.sleep(cnt)


def subscribe_message():
    subscriber = mqtt.Subscriber(on_message)
    subscriber.start(host_url, port, topic_cmd)


def on_message(client, userdata, msg):
    rx_message = str(msg.payload.decode("utf-8"))
    print(rx_message, flush=True)

    if rx_message == 'q':
        print('--------exit--------')
        published_message('exit', topic_cmd)
        sys.exit()
    elif rx_message == '1':
        published_message(connect_serial_device(status), topic_cmd)
    elif rx_message == '2':
        connect_serial_device(turn_on)
        published_message('Turn On the Light', topic_cmd)
    elif rx_message == '3':
        connect_serial_device(turn_off)
        published_message('Turn Off the Light', topic_cmd)
    elif rx_message == '4':
        connect_serial_device(light_reset)
        published_message('Reset the Light', topic_cmd)
    elif rx_message == '5':
        connect_serial_device(floating_light)
        published_message('Floating Light Mode', topic_cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('test cmd light')
    if len(sys.argv) <= 1:
        # host_url = "localhost"
        # port = 1883
        # topic = "cmd/Light"
        # host_url = 'ketibnt.iptime.org'
        host_url = "10.128.0.10"
        port = 1883
        topic_cmd = 'light/cmd'
        topic_status = 'light/status'
        interval = 5
        device = '/dev/ttyTHS0'

        print("start for default option")
        print("usage : python main.py <host_url> <mqtt_port> <topic>")
        #print("        host_url = localhost, mqtt_port = 1883, topic = light/status, interval = 3")
        print("host_url = " + host_url + ", mqtt_port = " + port +
              ", topic_cmd = " + topic_cmd + ", topic_status = " + topic_status +
              ", interval = " + interval + "sec" + " device = " + device, flush=True)
    else:
        host_url = sys.argv[1]
        port = int(sys.argv[2])
        topic_cmd = sys.argv[3]
        topic_status = sys.argv[4]
        interval = int(sys.argv[5])
        device = sys.argv[6]
        print("host_url = " + sys.argv[1] + ", mqtt_port = " + sys.argv[2] +
              ", topic_cmd = " + sys.argv[3] + ", topic_status = " + sys.argv[4] +
              ", interval = " + sys.argv[5] + "sec" + " device = " + sys.argv[6], flush=True)

    ser = open_serial(device)

    dataForm = 'json'
    # ser = open_serial('/dev/ttyTHS0')

    thread_1 = threading.Thread(target=subscribe_message)
    thread_1.start()

    thread_2 = threading.Thread(target=pub_status_schedule, args=(topic_status, interval))
    thread_2.daemon = True
    thread_2.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
