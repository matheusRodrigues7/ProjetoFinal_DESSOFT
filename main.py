# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, FINAL, QUIT
from init_screen import init_screen
from game_screen import game_screen
from final_screen import final_screen

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Joyride')

score = 0
state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state,score = game_screen(window)
    elif state == FINAL:
        state = final_screen(window,score)
    else:
        state = QUIT

# ==== Finalização ====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
'''
# ==== Inicialização ====
# ---- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, QUIT
from init_screen import init_screen
from game_screen import game_screen
from time import sleep

pygame.init()
pygame.mixer.init()

# ---- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Joyride')
    
game_screen(window)
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados'''