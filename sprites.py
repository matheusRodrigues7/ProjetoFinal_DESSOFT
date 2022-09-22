from asyncio.windows_events import NULL
import random
import pygame
from math import *
from config import WIDTH
from assets import PLAYER_IMG, FLY_IMG, JUMP_IMG, PEW_SOUND, ROCKET_IMG, BULLET_IMG, EXPLOSION_ANIM, FIRE_SOUND

# ---- Inicia estruturas de dados
# ---- Definindo as classes
class Assets(pygame.sprite.Sprite):    #Super Classe Para Assets
    def __init__(self, image, fly, jump):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.jump = jump
        self.fly = fly

class Player(Assets):
    def __init__(self,groups,assets):
        # Construtor da classe mãe (Sprite).
        super().__init__(assets[PLAYER_IMG], assets[FLY_IMG], assets[JUMP_IMG])
        self.rect.centery = 625
        self.rect.left = 80
        self.speedy = 0
        self.images = []
        self.index = 0
        self.counter = 0
        self.groups = groups
        self.assets = assets
        #self.pew_sound = pew_sound
        
        for num in range(1,3):
            img2 = pygame.image.load(f'assets/img/walk{num}.png')
            self.images.append(img2)
        self.accel = 0

    def movement(self):
        self.speedy -= 20
        self.fogo()
        
    def update(self):
        
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
        self.assets[FIRE_SOUND].play()
    
    def shoot(self):
        # ---- O 1berto vai ser criado na direita e no meio do player 
        new_bullet = Bullet(self.assets, self.rect.right, self.rect.centery)
        self.groups['all_sprites'].add(new_bullet)
        self.groups['all_bullets'].add(new_bullet)
        self.assets[PEW_SOUND].play()

class Rocket(Assets):
    def __init__(self,assets,t=0):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.t = t
        super().__init__(assets[ROCKET_IMG], NULL, NULL)
        self.rect.top = random.randint(130, 610)
        self.rect.bottom = random.randint(0, 0)
        self.rect.x = 1024
        self.rect.y = random.randint(110, 650)
        
        self.speedx = 10 + 15 * t if t < 1 else 35

    def update(self):
        # Atualizando a posição do foguete
        self.t += 0.0001
        self.speedx = 10 + 15 * self.t if self.t < 1 else 35
        self.rect.x -= self.speedx
        
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randint(1024, 2048)
            self.rect.y = random.randint(130, 610)

# Classe Bullet que representa os tiros
class Bullet(Assets):
    # Construtor da classe.
    def __init__(self, assets, left, centery):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        super().__init__(assets[BULLET_IMG], NULL, NULL)
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

# Classe que representa uma explosão do foguete
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets[EXPLOSION_ANIM]

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