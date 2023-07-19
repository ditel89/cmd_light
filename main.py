# This is a sample Python script.
import serial
import sys

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
    if cmd == status:
        if len(result) == 0:
            result = 'error, try again'
        else:
            parsing = result.split(',')
            result = "V : " + parsing[1] + ', A : ' + parsing[2] + ', CDS : ' + parsing[3] + ', ON/OFF : ' + parsing[
                4] + \
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

    ser = open_serial('/dev/ttyUSB0')

    status = '$LICMD,1,1*4F\r\n'
    turnOff = '$LICMD,3,1*4D\r\n'
    turnOn = '$LICMD,2,1*4C\r\n'
    lightReset = '$LICMD,4,1*4A\r\n'
    floatingLight = '$LICMD,5,1*4B\r\n'

    string = status
    # write_port(ser, string.encode())
    # print(string)
    while True:
        print('insert cmd :')
        op = input()
        if op == '1':
            string = status
            print('Show Status')
        elif op == '2':
            string = turnOn
            print('Turn On')
        elif op == '3':
            string = turnOff
            print('Turn Off')
        elif op == '4':
            string = lightReset
            print('Reset')
        elif op == '5':
            string = floatingLight
            print('Floating Light')
        elif op == 'q':
            print('break')
            break

        ser.write(string.encode())
        # print(op.encode())

        result = read(ser)
        print('result : ', result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
