import multiprocessing
import binascii #we import the library to use globally in the script lorawan_async

#We import the scripts mains in every functions
def run_orquestador():
    import orquestador
    orquestador.elapse_scripts(0)

def run_lorawan_async():
    #We open script lorawan_async.py and we run 
    exec(open('lorawan_async.py').read())

if __name__ == '__main__':
     #We crete two separete process to the run every script
    m1 = multiprocessing.Process(target=run_orquestador)
    m2 = multiprocessing.Process(target=run_lorawan_async)
    #We init every process
    m1.start()
    m2.start()
    #We wait to end process
    m1.join()
    m2.join()