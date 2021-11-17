import pygame 
import sys 
from os import path
from config import FNT_DIR  
  
pygame.init() 
res = (720,720) 
screen = pygame.display.set_mode(res) 
color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
width = screen.get_width() 
height = screen.get_height() 
smallfont = pygame.font.Font(path.join(FNT_DIR, 'NewAthleticM54.ttf'), 80)
text = smallfont.render('quit' , True , color) 
  
while True: 
      
    for ev in pygame.event.get(): 
        if ev.type == pygame.QUIT: 
            pygame.quit() 
            
        if ev.type == pygame.MOUSEBUTTONDOWN: 
                    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                        pygame.quit() 

    mouse = pygame.mouse.get_pos() 
      
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
      
    
    screen.blit(text , (width/2+50,height/2)) 
      
    
    pygame.display.update() 