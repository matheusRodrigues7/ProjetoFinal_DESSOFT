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

# ==== Finalização ====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados'''

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
font = pygame.font.SysFont(None, 48)
# ---- Background
'''background = pygame.image.load('assets/img/background.jpg').convert()
ground = pygame.image.load('assets/img/background_ground.png').convert_alpha()
background_move = pygame.image.load('assets/img/background_move.png').convert_alpha()
# ---- Player
player_img = pygame.image.load('assets/img/walk1.png').convert_alpha()
img_fly = pygame.image.load('assets/img/flying1.png').convert_alpha()
img_jump = pygame.image.load('assets/img/beggining.png').convert_alpha()
# ---- Obstacles
Rocket1 = pygame.image.load('assets/img/zap1.png').convert_alpha()
Rocket2 = pygame.image.load('assets/img/zap2.png').convert_alpha()
Rocket3 = pygame.image.load('assets/img/zap3.png').convert_alpha()
Rocket4 = pygame.image.load('assets/img/zap4.png').convert_alpha()
Rocket3 = pygame.image.load('assets/img/zap5.png').convert_alpha()'''

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

# ---- Setting Default Variable
ground_scroll = 0
scroll_speed = 5
dead = False
#Rocket_frequency = 4000 # --> Milesegundos 
#last_Rocket = pygame.time.get_ticks()

# ---- Inicia estruturas de dados
# ---- Definindo as classes
class Player(pygame.sprite.Sprite):
    def __init__(self,groups,assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['player_img']
        self.rect = self.image.get_rect()
        self.rect.centery = 625
        self.rect.left = 80
        self.speedy = 0
        self.images = []
        self.index = 0
        self.counter = 0
        self.fly = assets['img_fly']
        self.jump = assets['img_jump']
        self.groups = groups
        self.assets = assets
        #self.pew_sound = pew_sound
        
        for num in range(1,3):
            img2 = pygame.image.load(f'assets/img/walk{num}.png')
            self.images.append(img2)
        self.accel = 0


    def update(self):
        dead = False
        if dead == False: # ---> IMPLEMENTAR FUNÇÃO DE MORTE
            # ---- Atualização da posição do player
            # ---- Aceleração Gravidade
            self.accel += 0.5
            self.accel = min(self.accel, 10)
            
            # ---- Velocidade Jetpack
            self.rect.y += self.speedy

                    # ---- Troca o Estilo de Voo
            if self.accel <= 10:
                self.image = self.jump
            if self.speedy == -20:
                self.image = self.fly 

            # ---- Jogador anda dentro dessas cordenadas
            if self.rect.centery > 620 and self.rect.centery <= 650:
                self.counter+= 1
                walk_cooldown = 5
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index +=1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index]

        # ---- Limita o Teto   
        if self.rect.top<=110:
            self.rect.y=110

        # ---- Limita o chão 
        if self.rect.bottom < 660:
            self.rect.y += int(self.accel)
    
    def fogo(self):
        self.assets['pew_sound'].play()
    
    def shoot(self):
        # A nova bala vai ser criada logo acima e no centro horizontal da nave
        new_bullet = Bullet(self.assets, self.rect.right, self.rect.centery)
        self.groups['all_sprites'].add(new_bullet)
        self.groups['all_bullets'].add(new_bullet)
        self.assets['pew_sound'].play()

class Rocket(pygame.sprite.Sprite):
    def __init__(self,assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['rocket_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.top = random.randint(110, 670)
        self.rect.bottom = random.randint(0, 0)
        self.rect.x = random.randint(WIDTH/2, WIDTH)
        self.rect.y = random.randint(110, 715)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x -= scroll_speed*3
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        #if self.rect.right < 0:
           # self.kill()

        if self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randint(1024, 1536)
            self.rect.y = random.randint(110, 630)
            
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, left, centery):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bullet_img']
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = centery
        self.rect.left = left
        self.speedx = 10  # Velocidade fixa para a direita

    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx

        # Se o tiro passar do fim da tela, morre.
        if self.rect.left > WIDTH:
            self.kill()

# Classe que representa uma explosão de meteoro
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosion_anim']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Variável para o ajuste de velocidade (FPS)
clock = pygame.time.Clock()
FPS = 60
assets = load_assets()

# ---- Criando um grupo de sprites
all_sprites = pygame.sprite.Group()
all_rockets = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_rockets'] = all_rockets
groups['all_bullets'] = all_bullets

# ---- Criando o jogador
assets = load_assets
player = Player(groups,assets)
all_sprites.add(player)

# ---- Criando os Rockets
#Rockets = [Rocket1, Rocket2]
for _ in range(3):
    #Rocket = Rocket(random.choice(Rockets))
    rocket = Rocket(assets)
    all_sprites.add(rocket)
    all_rockets.add(rocket)

'''DONE = 0
PLAYING = 1
EXPLODING = 2
state = PLAYING'''

# ===== Loop principal =====
game = True
pygame.mixer.music.play(loops=-1)
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


    # Verifica se houve colisão entre tiro e foguete
    hits = pygame.sprite.groupcollide(all_rockets, all_bullets, True, True)
    for rocket in hits: # As chaves são os elementos do primeiro grupo (rockets) que colidiram com alguma bala
        # O meteoro e destruido e precisa ser recriado
        assets['destroy_sound'].play()
        r = Rocket(assets)
        all_sprites.add(r)
        all_rockets.add(r)
        
        explosao = Explosion(rocket.rect.center, assets)
        all_sprites.add(explosao)
    
    # ---- Verifica se houve colisão entre player e foguete
    hits = pygame.sprite.spritecollide(player, all_rockets, True)
    if len(hits) > 0:
        dead = True
        assets['boom_sound'].play()
        time.sleep(1) # Precisa esperar senão fecha
        game = False
        
    # ---- Gera saídas
    # ---- Faz o background se mover
    window.blit(assets['background'], (0, 0))
    window.blit(assets['ground'], (ground_scroll, 0))
    
    if dead == False:
        # ---- Cria novos Rockets
        #time_now = pygame.time.get_ticks()
        #if time_now - last_Rocket > Rocket_frequency:
                #Rocket = Rocket(random.choice(Rockets))
                #all_sprites.add(Rocket)
        # ---- Faz o background se mover
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 1024:
            ground_scroll = 0
    
    # ---- Desenhando os sprites
    all_sprites.draw(window)

    # ---- Mostra o novo frame para o jogador
    pygame.display.update()  

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados