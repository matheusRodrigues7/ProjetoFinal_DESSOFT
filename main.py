'''# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, QUIT
from init_screen import init_screen
from game_screen import game_screen

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Joyride')

state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados'''

# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame, sys, random, os

pygame.init()

# ----- Gera tela principal
WIDTH = 1024
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Joyride')

# ----- Inicia assets
PLAYER_WIDTH = 71
PLAYER_HEIGHT = 83
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('assets/img/background.jpg').convert()
ground = pygame.image.load('assets/img/background_ground.png').convert_alpha()
background_move = pygame.image.load('assets/img/background_move.png').convert_alpha()
player_img = pygame.image.load('assets/img/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
raio1 = pygame.image.load('assets/img/zap1.png').convert_alpha()
raio2 = pygame.image.load('assets/img/zap2.png').convert_alpha()
raio3 = pygame.image.load('assets/img/zap3.png').convert_alpha()
raio4 = pygame.image.load('assets/img/zap4.png').convert_alpha()
raio5 = pygame.image.load('assets/img/zap5.png').convert_alpha()
ground_scroll = 0
scroll_speed = 5

# ----- Inicia estruturas de dados
# Definindo os novos tipos
class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT / 2
        self.rect.left = WIDTH - 400
        self.speedy = 0

    def update(self):
        # Atualização da posição da nave
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class Raio(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(50, 715)
        self.speedx = -5

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 50 or self.rect.bottom > 715 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = random.randint(50, 715)
            


game = True
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de meteoros
all_sprites = pygame.sprite.Group()
# Criando o jogador
player = Player(player_img)
all_sprites.add(player)
# Criando os meteoros
raios = [raio1,raio2,raio3,raio4]
for _ in range(3):
    raio = Raio(random.choice(raios))
    all_sprites.add(raio)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_UP:
                player.speedy -= 15
            # if event.key == pygame.K_DOWN:
                # player.speedy += 8
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_UP:
                player.speedy += 15
            # if event.key == pygame.K_DOWN:
                # player.speedy -= 8

    # ----- Atualiza estado do jogo
    # Atualizando a posição dos meteoros
    all_sprites.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))
    window.blit(ground, (ground_scroll, 0))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 1024:
        ground_scroll = 0
    
    # Desenhando meteoros
    all_sprites.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados