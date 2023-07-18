import pygame
import time
from var_shared import run_time

pygame.init()
pygame.mixer.init()

archivo_audio = r"interestellar.mp3"
pygame.mixer.music.load(archivo_audio)
pygame.mixer.music.play()

time.sleep(run_time)
pygame.mixer.music.stop()

