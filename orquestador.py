#we import librarys
import schedule
import time
import multiprocessing
import binascii

def run_script1():
   #We imports and runs the script lorawan
   exec(open('lorawan.py').read())


def run_script2():
   #We imports and runs the script estimulo_now
   exec(open('estimulo_now.py').read())


def run_scripts():
   #We crete two separete process to the run every script
   p1 = multiprocessing.Process(target=run_script1)
   p2 = multiprocessing.Process(target=run_script2)

   #We init every process
   p1.start()
   p2.start()

   #We wait to end process
   p1.join()
   p2.join()
   
   stop = 1
   print('Stop scripts: ', stop)
 
 #We defined the function to run scripts
def elapse_scripts(x):
   if (x == 0):
      #We run the scripts each 24 h
      schedule.every(15).minutes.do(run_scripts)

      #loop for repit the run each 'x' schedule time
      while True:
        schedule.run_pending()
        time.sleep(1)

   elif (x == 1):
      #The function run a just one time     
      run_scripts()   
 


     
     
   



