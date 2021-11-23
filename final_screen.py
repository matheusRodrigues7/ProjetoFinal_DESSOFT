import pygame
import sys
import random
from os import path
from assets import BACKGROUND, load_assets, SCORE_FONT_FINAL, SCORE_FONT_LEADERBOARDS, GROUND
from config import IMG_DIR, BLACK, FPS, GAME, FNT_DIR, WHITE, YELLOW, GRAY
from game_screen import game_screen

# Lista de 3 maiores scores
scores = []

def final_screen(screen,score):
    if len(scores) < 3:
        scores.append(score)

    if score > scores[0]:
        scores.insert(1,scores[0])
        scores.remove(scores[-1])
        scores.remove(scores[0])
        scores.insert(0,score)
    elif len(scores) > 1 and score > scores[1]:
        scores.insert(2,scores[1])
        scores.remove(scores[-1])
        scores.remove(scores[1])
        scores.insert(1,score)
    elif len(scores) > 2 and score > scores[2]:
        scores.remove(scores[2])
        scores.insert(2,score)

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    assets = load_assets()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'morte.png')).convert_alpha()
    background_rect = background.get_rect()

    pygame.init() 
    res = (1024,768) 
    screen = pygame.display.set_mode(res)
    #width = screen.get_width() 
    #height = screen.get_height() 
    smallfont = pygame.font.Font(path.join(FNT_DIR, 'NewAthleticM54.ttf'), 80)
    sair = smallfont.render('QUIT', True, BLACK)
    play_again = smallfont.render('PLAY AGAIN', True , BLACK)
    
    running = True
    pygame.mixer.music.play(loops=-1)
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if 524 <= mouse[0] <= 524+365 and 320 <= mouse[1] <= 320+155:
                    pygame.quit()
                if 524 <= mouse[0] <= 524+365 and 495 <= mouse[1] <= 495+155:
                    state = GAME
                    running = False
        mouse = pygame.mouse.get_pos()
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        
        screen.blit(assets[GROUND], background_rect)
        
        if score >= 500:
            screen.blit(assets[BACKGROUND], background_rect)

        screen.blit(background, background_rect)

        if 524 <= mouse[0] <= 524+365 and 320 <= mouse[1] <= 320+155: 
            pygame.draw.rect(screen,WHITE,[524,320,365,155]) 
          
        else: 
            pygame.draw.rect(screen,GRAY,[524,320,365,155])
        
        if 524 <= mouse[0] <= 524+365 and 495 <= mouse[1] <= 495+155: 
            pygame.draw.rect(screen,WHITE,[524,528,450,158]) 
          
        else: 
            pygame.draw.rect(screen,GRAY,[524,528,450,158])
        
        screen.blit(sair, (640.5,350.5))
        screen.blit(play_again , (570.5,560.5))
        text_surface = assets[SCORE_FONT_FINAL].render(f'{str(int(score))}M ', True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (250,  150)
        screen.blit(text_surface, text_rect)

        n = 125
        for score1 in scores:
            text_surface = assets[SCORE_FONT_LEADERBOARDS].render(f'{str(int(score1))}M ', True, YELLOW)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (800,  n)
            screen.blit(text_surface, text_rect)
            n += 50

        pygame.display.update() 
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
    return state

    # text_surface = load_assets()[SCORE_FONT].render("{:08d}".format(int(game_screen.score)), True, (255, 255, 0))