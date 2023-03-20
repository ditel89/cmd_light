# This is a sample Python script.
import serial


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def open_serial(port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
    ss = serial.Serial()
    ss.port = port
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
