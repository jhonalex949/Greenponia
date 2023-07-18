import serial
import time 
import binascii
import json
import Jetson.GPIO as GPIO
import rak_config as rak
import re          #library to use regular expressions
import crecimiento_now as crec_now #We import the variable of growth of script 'crecimiento_now'
from var_shared import run_time, t_lwan #We import the variable of 'run time'


#Setup gpio to reset LoRaWAN module
GPIO.setmode(GPIO.BOARD)
#Pin 40 -- channel 1 of relay
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
#Pin 38 -- channel 2 of relay (for trigger pump)
GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH) #trigger pum for default

#We reset the LoRaWAN module for it to connect network LoRaWAN
GPIO.output(40, GPIO.LOW)
time.sleep(3)
GPIO.output(40, GPIO.HIGH)

#Parameters to config rak module lora
NWM = "1"
DEVEUI = "ac1f09fffe054a6b"
APPEUI = "AC1F09FFF8683172"
APPKEY = "ac1f09fffe054a6bac1f09fff8683172"
NJM = "1"
JOIN = "0:1:10:8"
ADR = "1" 
CLASS = "C"
DCS = "1"
RETY = "3"
BAND = "5"


AT = "AT+NWM=" + NWM + b'\r\n' +\
     "AT+DEVEUI=" + DEVEUI + b'\r\n' +\
     "AT+APPEUI=" + APPEUI + b'\r\n' +\
     "AT+APPKEY=" + APPKEY + b'\r\n' +\
     "AT+NJM=" + NJM + b'\r\n' +\
     "AT+JOIN=" + JOIN + b'\r\n' +\
     "AT+ADR=" + ADR + b'\r\n' +\
     "AT+CLASS=" + CLASS + b'\r\n' +\
     "AT+DCS=" + DCS + b'\r\n' +\
     "AT+RETY=" + RETY +  b'\r\n' +\
     "AT+BAND=" + BAND + b'\r\n' 
     
print(AT)
#We send the AT commands the rak module lora
conf = rak.SendAT(AT)
print(conf)  

#We import the variable of growth
crec = int(crec_now.crecimiento())
print("Growth percentegen: ", crec)
  
#setup port serial    
rs485 = serial.Serial('/dev/ttyTHS1', 4800, timeout=1)
#encode the port to utf-8
rs485.encoding = "utf-8"

#Config register of soil sensor (geted by datasheet)
reg = [0x01, 0x03, 0x00, 0x00, 0x00, 0x04, 0x44, 0x09]

#We convert the bytes of hex
def Bytes2Hex(a):
  return binascii.hexlify(a)

#Function to convert decimal to hex
def Dec2Hex(dec):
  return hex(dec)[2:]

#We create a function to get the payload of the downlink messages and then convert to ascii
def Hex2Ascii(b):
  #We convert the message 'b' to bytes array and then 
  #we decode the bytes to ascii using the function decode
  data_hex = b.replace('\r\n\r\nOK', '')
  byte_array = bytearray.fromhex(data_hex)
  ascii_string = byte_array.decode()
  return str(ascii_string) 

#We calculate the number of runs during the period 'run_time'
t = run_time/t_lwan #for example: if run_time = 60 seg, t_lwan = 10; t = 6 runs for each 10 seconds


#We run script during the time assigned in the variable 't'
for i in range(0, t):    
   ############Sensor soil in working#################
    rs485.write(reg)
    time.sleep(1)
    #Get all data without spaces at the beginnig and at the end of string
    data = rs485.readall().strip()
    hexa = Bytes2Hex(data)
    #We get the position of every variable and we convert to int
    a = int(hexa[6:10], 16)
    b = int(hexa[10:14], 16)
    c = int(hexa[14:18], 16)
    d = int(hexa[18:22], 16)
    #We convert the variables float format
    hum = float(a)/10
    temp = float(b)/10
    cond = float(c)/10
    ph = float(d)/10
    print("read: ", hexa)
    print("hum: ", hum)
    print("temp: ", temp)
    print("cond: ", cond)
    print("ph: ", ph)
    #We convert an json object string and them to Hex
    
    dec_hex = Dec2Hex(crec)
    payload = hexa + dec_hex
    print(dec_hex)
    print(hexa)
    print(payload)
    obj = json.dumps({"dt":payload})
    raw = Bytes2Hex(obj)
    print(raw)
    #We send the data for channel 1 of link lorawan
    data = "AT+SEND=1:" + raw + '\r\n'
    print(data)
    rak.uart.write(data)
    time.sleep(t_lwan)
    read = rak.uart.readall().strip() #the function strip() delete whitespace
    resp = read.replace('\r\n', '')
    #We reset the lora module if not connect to the red
    if (resp == "AT_NO_NETWORK_JOINED" or resp == "AT_NO_NETWORK_JOINED\r\n\r\nAT_NO_NETWORK_JOINED"): 
      GPIO.output(40, GPIO.LOW)
      time.sleep(3)
      GPIO.output(40, GPIO.HIGH)
    else:
     try:
      #find the index of last occurrence 
      index = resp.rindex(':') + 1
      #We get the dowlink message
      msg = resp[index:]
      #We test if the msg is an hex using regular expressions
      if re.match(r'[0-9a-fA-F]+', msg):
          #We get the hex to ascii
          downlink = Hex2Ascii(msg)
          #We get the value of json object
          obj_val = json.loads(downlink)  #{'start': '1', 'act': '0'}
          bomb = int(obj_val['act'])    #act = 0

         #Starting pump drive
          if (bomb == 1):
            #We turn on pump
            print('bomb ON')
            GPIO.output(38, GPIO.HIGH)

          elif (bomb == 0):
            #We turn off pump
            print('bomb OFF')
            GPIO.output(38, GPIO.LOW)  

      else:
          print("msg", msg)               
     except:
       print("Not found")

    print("paylad: ", resp)

#We turn off pump when timeout 't'
GPIO.output(38, GPIO.LOW)  