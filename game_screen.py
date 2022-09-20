import pygame
from config import FPS, SCROLL_SPEED, FINAL
from assets import load_assets, DESTROY_SOUND, BACKGROUND2, BACKGROUND, SCORE_FONT, GAME_OVER
from sprites import Player, Rocket, Explosion
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
        score += 0.25
        t += 0.0001
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Se apertar a tecla UP, voa
                    if event.key == pygame.K_UP:
                        player.movement() #Houve uma coesão marcada neste local para delegar a função de movimento.
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player.speedy += 20
        
        # ---- Atualiza estado do jogo 
        # Atualizando a posição dos sprites
        all_sprites.update()
        if state == PLAYING:
            # Verifica se houve colisão entre tiro e foguete
            hits = pygame.sprite.groupcollide(all_rockets, all_bullets, True, True, pygame.sprite.collide_mask)
            for rocket in hits: # As chaves são os elementos do primeiro grupo (rockets) que colidiram com alguma bala
                # O foguete e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                r = Rocket(assets,t)
                all_sprites.add(r)
                all_rockets.add(r)
                explosao = Explosion(rocket.rect.center, assets)
                all_sprites.add(explosao)
                
            # ---- Verifica se houve colisão entre player e foguete
            # Finalizar jogo se colidir player com Rockets
            hits = pygame.sprite.spritecollide(player, all_rockets, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                assets[GAME_OVER].play()
                sleep(1) # Precisa esperar senão fecha
                state = EXPLODING
        elif state == EXPLODING:
            state = FINAL
            break

        # ---- Gera saídas
        # ---- Faz o background se mover
        window.blit(assets[BACKGROUND], (ground_scroll, 0))
        # Troca de tela 
        if score >= 1000:
            window.blit(assets[BACKGROUND2], (ground_scroll, 0))
        
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
