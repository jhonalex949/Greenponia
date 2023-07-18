import time 
import json
import binascii
import Jetson.GPIO as GPIO
import rak_config as rak
import re          #library to use regular expressions
from var_shared import t_lwan
import orquestador


#Setup gpio to reset LoRaWAN module
GPIO.setmode(GPIO.BOARD)
#Pin 40 -- channel 1 of relay
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
#Pin 38 -- channel 2 of relay (for trigger pump)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)

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

#Function to covert Bytes to Hexadecimal
def Bytes2Hex(a):
  return binascii.hexlify(a)

#We create a function to get the payload of the downlink messages and then convert to ascii
def Hex2Ascii(b):
  #We convert the message 'b' to bytes array and then 
  #we decode the bytes to ascii using the function decode
  data_hex = b.replace('\r\n\r\nOK', '')
  byte_array = bytearray.fromhex(data_hex)
  ascii_string = byte_array.decode()
  return str(ascii_string) 

#We crate a variable of system woking
ok = 0

if __name__ == '__main__':
   while(True):
    ok = ok + 1
    if (ok >= 100):
      ok = 0 

    #We crate the payoad of working
    obj = json.dumps({'system': ok})
   
    #We send the uplink message
    hex_payload = Bytes2Hex(obj) #We convert Bytes to Hex
    data = "AT+SEND=2:" + hex_payload + '\r\n'
    rak.uart.write(data)    
    resp = rak.uart.readall().strip() #the function strip() delete whitespace
    #We reset the lora module if not connect to the network
    if (resp == "AT_NO_NETWORK_JOINED"): 
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
          downlink = Hex2Ascii(msg)
          #We get the value of json object
          json_val = json.loads(downlink)   #{'start': '1', 'act': '0'}
          start = int(json_val['start'])    # 1
          bomb = int(json_val['act'])
          print("start: ", start)
          print("bomb: ", bomb)
        
         #variable for activation the script lorawan.py asynchronously
          if (start == 1):
            #We run all the system
            orquestador.elapse_scripts(1)
            continue

          #Starting pump drive
          if (bomb == 1):
            #We turn off bomb
            print("bomb ON")
            GPIO.output(38, GPIO.HIGH)

          elif (bomb == 0):
            #We turn on bomb
            print("bomb OFF")
            GPIO.output(38, GPIO.LOW) 
  
      else:          
          start = 0
          print("msg", msg)               
     except:
       print("Not found")

    print("payload: ", resp)
    time.sleep(t_lwan) #time of wait to send payload for channel LoRaWAN
