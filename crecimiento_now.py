#coding=utf-8
import cv2
import numpy as np
import json
import datetime
import time

def crecimiento():
    cap = cv2.VideoCapture(0)
    print("Capturando imágenes de la cámara 1")

    tiempo_analisis = 10  # Duración del análisis en segundos

    green_on_image_percent = 0

   
    greenBajo1 = np.array([35, 50, 50], np.uint8)
    greenAlto1 = np.array([85, 255, 255], np.uint8)

    tiempo_inicial = time.time()  # tiempo actual en segundos

    while (time.time() - tiempo_inicial) < tiempo_analisis:
        ret, frame = cap.read()
        if ret == True:
            
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
           
            maskGreen1 = cv2.inRange(frameHSV, greenBajo1, greenAlto1)
           
            maskGreenvis = cv2.bitwise_and(frame, frame, mask=maskGreen1)
            green_only = cv2.merge((np.zeros_like(maskGreen1), maskGreen1, np.zeros_like(maskGreen1)))
            cv2.imshow('Frame de video', frame)
            cv2.imshow('Area verde en escala de grises', maskGreen1)
            cv2.imshow('Visualizacion area verde', maskGreenvis)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break  # salir con 's'
    #print("Frame capturado")


    number_of_white_pix = np.sum(maskGreen1 == 255)
    number_of_black_pix = np.sum(maskGreen1 == 0)

    #print('Number of white pixels:', number_of_white_pix)
    #print('Number of black pixels:', number_of_black_pix)

    cap.release()
    cv2.destroyAllWindows()

 
    total_image_pixels = number_of_white_pix + number_of_black_pix
    #print('Total image pixels:', total_image_pixels)

    green_on_image_percent = ((number_of_white_pix * 100) / total_image_pixels)
    #print('Green_on_image_percent:', green_on_image_percent)

    soil_on_image_percent = 100 - green_on_image_percent
    #print('Soil_on_image_percent:', soil_on_image_percent)

    return green_on_image_percent


   
 
    """ timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Crear el diccionario con la clave "green_on_image_percent" y su valor
    data = {"green_on_image_percent": green_on_image_percent}

    # Convertir el diccionario en una cadena JSON
    json_data = json.dumps(data)

    # Crear el nombre de archivo con la marca de tiempo
    filename = f"archivo_{timestamp}.json"

    # Escribir la cadena JSON en un archivo con el nombre único
    with open(filename, "w") as archivo:
        archivo.write(json_data)


    crecimiento_lechugas = 'Lechugas', 'Suelo'
    # Declaramos el tamaño de cada 'rebanada' y en sumatoria todos deben dar al 100%
    sizes = [green_on_image_percent, soil_on_image_percent]
    # En este punto señalamos que posicion debe 'resaltarse' y el valor, si se coloca 0, se omite
    explode = (0.1, 0)
    mycolors = ["green", "sienna"]

    fig1, ax1 = plt.subplots()
    # Creamos el grafico, añadiendo los valores
    ax1.pie(sizes, explode=explode, labels=crecimiento_lechugas, colors=mycolors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # señalamos la forma, en este caso 'equal' es para dar forma circular
    ax1.axis('equal')
    plt.title("Crecimiento de las lechugas")
    plt.legend()
    plt.savefig('Grafico_crecimiento_lechugas.png')
    plt.show()"""
    
if __name__ == '__main__':
    crecimiento()
