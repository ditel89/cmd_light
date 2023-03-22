# This is a sample Python script.
import serial
import sys

import mqtt

status = '$LICMD,1,1*4F\r\n'
turn_on = '$LICMD,2,1*4C\r\n'
turn_off = '$LICMD,3,1*4D\r\n'
light_reset = '$LICMD,4,1*4A\r\n'
floating_light = '$LICMD,5,1*4B\r\n'


def open_serial(device, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
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


def write_port(ss, data):
    ss.write(data)


def read(ss, timeout=1):
    ss.timeout = timeout
    rx = ss.readline().decode()
    return rx


def connect_serial_device(cmd):
    ser = open_serial('/dev/ttyUSB0')

    ser.write(cmd.encode())

    result = read(ser)
    parsing = result.split(',')
    if cmd == status:
        result = "V : " + parsing[1] + ', A : ' + parsing[2] + ', CDS : ' + parsing[3] + ', ON/OFF : ' + parsing[4] + \
                  ', Character : ' + parsing[5] + ', Latitude : ' + parsing[8] + ', Longitude : ' + parsing[9][:4]
    # print(result2)
    # print('result : ', result)
    return result


def published_message(msg, topic_pub):
    publisher = mqtt.Publisher()
    publisher.start(host_url, port)
    publisher.publish(topic_pub, msg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('test cmd light')
    if len(sys.argv) < 2:
        host_url = "localhost"
        port = 1883
        topic = "cmd/Light"
        print("start for default option")
        print("usage : python main.py <host_url> <mqtt_port> <topic>")
        print("        host_url = localhost, mqtt_port = 1883, topic = cmd/Light")
    else:
        host_url = sys.argv[1]
        port = sys.argv[2]
        topic = sys.argv[3]


    def on_message(client, userdata, msg):

        rx_message = str(msg.payload.decode("utf-8"))
        print(rx_message)

        if rx_message == 'q':
            print('stop subscriber')
            subscriber.stop()
        elif rx_message == '1':
            published_message(connect_serial_device(status), topic)
        elif rx_message == '2':
            connect_serial_device(turn_on)
            published_message('Turn On the Light', topic)
        elif rx_message == '3':
            connect_serial_device(turn_off)
            published_message('Turn Off the Light', topic)
        elif rx_message == '4':
            connect_serial_device(light_reset)
            published_message('Reset the Light', topic)
        elif rx_message == '5':
            connect_serial_device(floating_light)
            published_message('Floating Light Mode', topic)


    subscriber = mqtt.Subscriber(on_message)
    subscriber.start(host_url, port, topic)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
