import pygame
from config import FPS, SCROLL_SPEED, FINAL
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, GROUND, SCORE_FONT
from sprites import Player, Rocket, Bullet, Explosion
from time import sleep

def game_screen(window):
    clock = pygame.time.Clock()
    assets = load_assets()
    # Variável para o ajuste de velocidade (FPS)
    # ---- Criando um grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_rockets = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_rockets'] = all_rockets
    groups['all_bullets'] = all_bullets
# ---- Criando o jogador
    player = Player(groups,assets)
    all_sprites.add(player)
    # ---- Criando os Rockets
    #Rockets = [Rocket1, Rocket2]
    for _ in range(5):
        #Rocket = Rocket(random.choice(Rockets))
        rocket = Rocket(assets)
        all_sprites.add(rocket)
        all_rockets.add(rocket)
    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING
    score = 0
    ground_scroll = 0
    t = 0
    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)
        score += 1
        t += 0.000001
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_UP:
                        player.speedy -= 20
                        player.fogo()
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_UP:
                        player.speedy += 20
        # Finalizar jogo se colidir player com Rockets - !!!IMPLEMENTAR!!!
        #if len(hits) == True:
            #dead = True
        # ---- Atualiza estado do jogo 
        # Atualizando a posição dos sprites
        all_sprites.update()
        if state == PLAYING:
            # Verifica se houve colisão entre tiro e foguete
            hits = pygame.sprite.groupcollide(all_rockets, all_bullets, True, True, pygame.sprite.collide_mask)
            for rocket in hits: # As chaves são os elementos do primeiro grupo (rockets) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                r = Rocket(assets,t)
                all_sprites.add(r)
                all_rockets.add(r)
                explosao = Explosion(rocket.rect.center, assets)
                all_sprites.add(explosao)
                '''score += 100'''
                
            # ---- Verifica se houve colisão entre player e foguete
            hits = pygame.sprite.spritecollide(player, all_rockets, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                dead = True
                assets[BOOM_SOUND].play()
                sleep(1) # Precisa esperar senão fecha
                state = EXPLODING
        elif state == EXPLODING:
            state = FINAL
            break
        # ---- Setting Default Variable
        dead = False
        # ---- Gera saídas
        # ---- Faz o background se mover
        window.blit(assets[GROUND], (ground_scroll, 0))
        if score >= 500:
            window.blit(assets[BACKGROUND], (ground_scroll, 0))
        if dead == False:
            # ---- Cria novos Rockets
            #time_now = pygame.time.get_ticks()
            #if time_now - last_Rocket > Rocket_frequency:
                    #Rocket = Rocket(random.choice(Rockets))
                    #all_sprites.add(Rocket)
            # ---- Faz o background se mover
            ground_scroll -= SCROLL_SPEED
            if abs(ground_scroll) > 1024:
                ground_scroll = 0
        # ---- Desenhando os sprites
        all_sprites.draw(window)
        # desenhando o placar
        text_surface = assets[SCORE_FONT].render("{:04d}M".format(int(score)), True, (255, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (80,  10)
        window.blit(text_surface, text_rect)
        # ---- Mostra o novo frame para o jogador
        pygame.display.update()
    return state, score
