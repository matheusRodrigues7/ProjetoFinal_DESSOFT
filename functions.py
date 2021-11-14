# ==== Inicialização ====
# ---- Importa e inicia pacotes
import pygame, sys, random, os, time
pygame.init()
pygame.mixer.init()
# ---- Gera tela principal
WIDTH = 1024
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Joyride')
# ---- Inicia assets
def load_assets():
    assets = {}
    assets['background'] = pygame.image.load('assets/img/background.jpg').convert()
    assets['ground'] = pygame.image.load('assets/img/background_ground.png').convert_alpha()
    assets['player_img'] = pygame.image.load('assets/img/walk1.png').convert_alpha()
    assets['img_fly'] = pygame.image.load('assets/img/flying1.png').convert_alpha()
    assets['img_jump'] = pygame.image.load('assets/img/beggining.png').convert_alpha()
    assets['rocket_img'] = pygame.image.load('assets/img/foguete.png').convert_alpha()
    assets['rocket_img'] = pygame.transform.scale(assets['rocket_img'], (47*3, 24*3))
    assets['bullet_img'] = pygame.image.load('assets/img/star.png').convert_alpha()
    assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (47, 47))
    explosion_anim = []
    for i in range(9):
        img = pygame.image.load(f'assets/img/exp{i}.png').convert()
        img = pygame.transform.scale(img, (90, 90))
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font('assets/font/NewAthleticM54.ttf', 28)
    # Carrega os sons do jogo
    pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
    pygame.mixer.music.set_volume(0.4)
    assets['boom_sound'] = pygame.mixer.Sound('assets/snd/expl3.wav')
    assets['destroy_sound'] = pygame.mixer.Sound('assets/snd/expl6.wav')
    assets['pew_sound'] = pygame.mixer.Sound('assets/snd/pew.wav')
    assets['ground_scroll'] = 0
    assets['scroll_speed'] = 5
    return assets
