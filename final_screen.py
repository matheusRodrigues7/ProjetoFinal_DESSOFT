import pygame
import random
from os import path
from assets import BACKGROUND, load_assets, SCORE_FONT_FINAL
from config import IMG_DIR, BLACK, FPS, GAME, QUIT
from game_screen import game_screen


def final_screen(screen,score):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'morte.png')).convert()
    background_rect = background.get_rect()

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        assets = load_assets()
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
        #screen.fill(BLACK)
        screen.blit(assets[BACKGROUND], background_rect)

        screen.blit(background, background_rect)

        text_surface = assets[SCORE_FONT_FINAL].render(f'{str(score)}M ', True, (255, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (250,  150)
        screen.blit(text_surface, text_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
    return state

    # text_surface = load_assets()[SCORE_FONT].render("{:08d}".format(int(game_screen.score)), True, (255, 255, 0))