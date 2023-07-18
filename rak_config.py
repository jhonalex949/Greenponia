import serial
import serial.tools.list_ports as sr


#Get an list of available ports
ports = list(sr.comports())
for port, desc, hwi in ports:
    print('{}:{}[{}]'.format(port, desc, hwi))

uart = serial.Serial(port, 9600, timeout=1)

def SendAT(command):
    #Send the AT command encode so they can be read by rak module lora
    uart.write(command.encode() + b'\r\n')
    #Read and decode the data until 1024 bytes
    response = uart.read(1024).decode()
    return response

