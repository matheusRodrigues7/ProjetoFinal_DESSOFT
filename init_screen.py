import pygame
import random
from os import path
from assets import load_assets , SCORE_FONT_LEADERBOARDS
from config import IMG_DIR, BLACK, FPS, GAME, QUIT, WHITE


def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
    background_rect = background.get_rect()

    running = True
    assets = load_assets()
    pygame.mixer.music.play(loops=-1)
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                state = GAME
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        # Instruções
        inst1 = assets[SCORE_FONT_LEADERBOARDS].render('press up to fly', True, WHITE)
        inst1_rect = inst1.get_rect()
        inst1_rect.midtop = (500,  590)
        screen.blit(inst1, inst1_rect)

        inst2 = assets[SCORE_FONT_LEADERBOARDS].render('press space to shoot', True, WHITE)
        inst2_rect = inst1.get_rect()
        inst2_rect.midtop = (450,  640)
        screen.blit(inst2, inst2_rect)
        
        pygame.display.flip()
    
    return state