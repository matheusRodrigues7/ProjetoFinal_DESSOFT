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
raio1 = pygame.image.load('assets/img/zap1.png').convert_alpha()
raio2 = pygame.image.load('assets/img/zap2.png').convert_alpha()
raio3 = pygame.image.load('assets/img/zap3.png').convert_alpha()
raio4 = pygame.image.load('assets/img/zap4.png').convert_alpha()
raio3 = pygame.image.load('assets/img/zap5.png').convert_alpha()'''

assets = {}
assets['background'] = pygame.image.load('assets/img/background.jpg').convert()
assets['ground'] = pygame.image.load('assets/img/background_ground.png').convert_alpha()
assets['background_move'] = pygame.image.load('assets/img/background_move.png').convert_alpha()
assets['player_img'] = pygame.image.load('assets/img/walk1.png').convert_alpha()
assets['img_fly'] = pygame.image.load('assets/img/flying1.png').convert_alpha()
assets['img_jump'] = pygame.image.load('assets/img/beggining.png').convert_alpha()
assets['rocket_img'] = pygame.image.load('assets/img/foguete.png').convert_alpha()
assets['rocket_img'] = pygame.transform.scale(assets['rocket_img'], (47*3, 24*3))

# Carrega os sons do jogo
pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound('assets/snd/expl3.wav')
#destroy_sound = pygame.mixer.Sound('assets/snd/expl6.wav')
pew_sound = pygame.mixer.Sound('assets/snd/pew.wav')
assets['pew_sound'] = pygame.mixer.Sound('assets/snd/pew.wav')

# ---- Setting Default Variable
ground_scroll = 0
scroll_speed = 5
dead = False
#raio_frequency = 4000 # --> Milesegundos 
#last_raio = pygame.time.get_ticks()

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

class Raio(pygame.sprite.Sprite):
    def __init__(self,assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['rocket_img']
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
            

# Variável para o ajuste de velocidade (FPS)
clock = pygame.time.Clock()
FPS = 60

# ---- Criando um grupo de sprites
all_sprites = pygame.sprite.Group()
all_rockets = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_rockets'] = all_rockets

# ---- Criando o jogador
player = Player(groups,assets)
all_sprites.add(player)

# ---- Criando os raios
#raios = [raio1, raio2]
for _ in range(3):
    #raio = Raio(random.choice(raios))
    rocket = Raio(assets)
    all_sprites.add(rocket)
    all_rockets.add(rocket)

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
                
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_UP:
                player.speedy += 20

    # ---- Verifica se houve colisão entre nave e meteoro
    

    # Finalizar jogo se colidir player com raios - !!!IMPLEMENTAR!!!
    #if len(hits) == True:
        #dead = True

    # ---- Atualiza estado do jogo 
    # Atualizando a posição dos sprites
    all_sprites.update()


    hits = pygame.sprite.spritecollide(player, all_rockets, True)
    if len(hits) > 0:
        dead = True
        boom_sound.play()
        time.sleep(1) # Precisa esperar senão fecha
        game = False
        
    # ---- Gera saídas
    # ---- Faz o background se mover
    window.blit(assets['background'], (0, 0))
    window.blit(assets['ground'], (ground_scroll, 0))
    
    if dead == False:
        # ---- Cria novos raios
        #time_now = pygame.time.get_ticks()
        #if time_now - last_raio > raio_frequency:
                #raio = Raio(random.choice(raios))
                #all_sprites.add(raio)
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