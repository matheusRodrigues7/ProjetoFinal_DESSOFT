import pygame
import os
from config import ROCKET_WIDTH, ROCKET_HEIGHT, IMG_DIR, SND_DIR, FNT_DIR

BACKGROUND = 'background'
GROUND = 'ground'
PLAYER_IMG = 'player_img'
FLY_IMG = 'fly_img'
JUMP_IMG = 'jump_img'
ROCKET_IMG = 'rocket_img'
BULLET_IMG = 'bullet_img'
EXPLOSION_ANIM = 'explosion_anim'
SCORE_FONT = 'score_font'
SCORE_FONT_FINAL = 'score_font_final'
BOOM_SOUND = 'boom_sound'
DESTROY_SOUND = 'destroy_sound'
PEW_SOUND = 'pew_sound'

def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, 'background.jpg')).convert()
    assets[GROUND] = pygame.image.load(os.path.join(IMG_DIR, 'background_ground.png')).convert_alpha()
    assets[PLAYER_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'walk1.png')).convert_alpha()
    assets[FLY_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'flying1.png')).convert_alpha()
    assets[JUMP_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'beggining.png')).convert_alpha()
    assets[ROCKET_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'foguete.png')).convert_alpha()
    assets[ROCKET_IMG] = pygame.transform.scale(assets['rocket_img'], (ROCKET_WIDTH, ROCKET_HEIGHT))
    assets[BULLET_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'star.png')).convert_alpha()
    assets[BULLET_IMG] = pygame.transform.scale(assets['bullet_img'], (47, 47))
    explosion_anim = []
    for i in range(9):
        filename = os.path.join(IMG_DIR, f'exp{i}.png')
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (90, 90))
        explosion_anim.append(img)
    assets[EXPLOSION_ANIM] = explosion_anim
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(FNT_DIR, 'NewAthleticM54.ttf'), 40)
    assets[SCORE_FONT_FINAL] = pygame.font.Font(os.path.join(FNT_DIR, 'NewAthleticM54.ttf'), 100)

    # Carrega os sons do jogo
    pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.wav')
    pygame.mixer.music.set_volume(0.4)
    assets[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl3.wav'))
    assets[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl6.wav'))
    assets[PEW_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'pew.wav'))
    
    return assets