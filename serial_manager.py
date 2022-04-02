import serial 


class SerialManager(serial.Serial):
    def __init__(self, port='/dev/ttyUSB1', baudrate=1843200, timeout=0.5):
        try:
            super().__init__(port=port, baudrate=baudrate, timeout=timeout)
        except:
            raise Exception('Could not open serial port.')
    
    def send_command(self, command, size=500):
        command = bytes(command + '\r\n', 'utf-8')
        res = ''
        try:
            bytes_written = super().write(command)
            print(f'Bytes written: {bytes_written}.')
            
            tmp = super().read(size).decode('ascii')
            res += tmp
            
            while len(tmp) == size:
                tmp = super().read(size).decode('ascii')
                res += tmp
        except:
            raise Exception('Error sending command.')
        
        if res[:5] == '\n\r>\n\r':
            res = res[5:]
        if res[-5:] == '\r\n\n\r>':
            res = res[:-5]
        return res

if __name__ == '__main__':
    serial = SerialManager()
    print(serial.send_command('RD AFE 0 REG 1'))
    serial.close()
