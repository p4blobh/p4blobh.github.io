import pygame
from sys import exit
import asyncio

pygame.init()

Screen_width = 800
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Pie-Clicker')

run = True


#-------------------------------
#------- Clicker Setup --------#
#-------------------------------
applepie = r"images/apple_pie1.png"
pie_tier = [applepie]
current_tier = 0
class Game:
    def __init__(self):
        self.pies = 0
        self.pies_per_click = 1
        self.pies_per_second = 0
        self.pie = pygame.image.load(pie_tier[current_tier])
        self.clicked = False

    def click(self):
        pie_loct = (70,200)
        self.mouse_pos = pygame.mouse.get_pos()
        if self.pie.get_rect(topleft=(pie_loct)).collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
             if self.clicked:
                self.pies += self.pies_per_click
                self.clicked = False
        screen.blit(self.pie,(pie_loct))
    def upgrades(self):
        pass
    def render(self):
        self.click()
        self.upgrades()
        




clock = pygame.time.Clock()
game = Game()

#-------------------------------
#----------- Text -------------#
#-------------------------------
titlefont = pygame.font.SysFont('Comic Sans MS', 50)
font = pygame.font.SysFont('Comic Sans MS', 30)

titletext = titlefont.render('Pie-Clicker', True, (0, 0, 0))
piestxt = font.render('Pies: {0}'.format(game.pies), True, (0, 0, 0))

#-------------------------------xx
#---------- The Game ----------#
#-------------------------------
async def main():
    while run:
    
        screen.fill ((255,255,255))
        screen.blit(titletext, (100,50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        piestxt = font.render('Pies: {0}'.format(game.pies), True, (0, 0, 0))
        screen.blit(piestxt, (150,350))
        pygame.draw.rect(screen, (0,10,200), (500,0,300,600))
        game.render()    

        pygame.display.update()

        clock.tick(60)
        await asyncio.sleep(0)
        
asyncio.run(main())















#tiers  
# Common -  Apple, Lemon, Blueberry, Cherry, Pumpkin
# Rare -  Peach, Pecan, Coconut, Blackberry, Watermelon
# Exotic - Pineapple on, Jelly Bean, Lollipop, Donut, Pie