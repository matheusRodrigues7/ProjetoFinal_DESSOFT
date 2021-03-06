from os import path

WIDTH = 1024
HEIGHT = 768
FPS = 60

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Define tamanhos
ROCKET_WIDTH = 202
ROCKET_HEIGHT = 66
SANDMANN_WIDTH = 55
SANDMANN_HEIGHT = 55

# Para a tela se mover
SCROLL_SPEED = 5

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100,100,100)
# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
FINAL = 2
QUIT = 3