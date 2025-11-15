import pygame
import asyncio

pygame.init()

Screen_width = 800
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Pie-Clicker')

icon_image = pygame.image.load(r"PieClicker_logo.png")
pygame.display.set_icon(icon_image)



#-------------------------------
#----------- Fonts ------------#
#-------------------------------
titlefont = pygame.font.SysFont('Comic Sans MS', 50)
mainfont = pygame.font.SysFont('Comic Sans MS', 30)
smallerfont = pygame.font.SysFont('Comic Sans MS', 20)
upgradefont = pygame.font.SysFont('Comic Sans MS', 14)

#-------------------------------
#----------- Images -----------#
#-------------------------------
applepie = r"applepie1.png"
peachpie = r"peachpie1.png"
cursorimg = r"cursor.png"


#-------------------------------
#------- Clicker Setup --------#
#-------------------------------

pie_tiers = [applepie, peachpie]

pie_loct = (120,200)

class Game:
    def __init__(self):
        self.pies = 0
        self.mostpies = 0
        self.pies_per_click = 1
        self.pies_per_second = 0
        self.clicked = False

        #Upgrade stuff that don't need to keep rendering

        #Cursor Upgrade
        self.clickupgradeBtn = pygame.Rect(510, 70, 280, 70)
        self.clickupgradedesc = upgradefont.render('Cursor: Pies per click +1', True, (0,0,0))
        self.clickupgradecost = 10


        
    def upgrades(self):
            pygame.draw.rect(screen, (9, 146, 214), (500,0,300,600))

            #Cursor Upgrade
            self.clickupgradeshowcost = upgradefont.render(f'Cost: {self.clickupgradecost}', True, (0,0,0))
            pygame.draw.rect(screen, (9, 101, 214), self.clickupgradeBtn, border_radius=5)
            screen.blit(self.clickupgradeshowcost, (580, 110))
            screen.blit(self.clickupgradedesc, (580, 80))
            cursorimgload = pygame.image.load(cursorimg)
            cursorimgresize = pygame.transform.scale(cursorimgload, (30, 60))
            cursorimgbg = cursorimgresize.convert_alpha()  
            pygame.draw.rect(screen, (9, 80, 214),(520,75,50,60),border_radius=7)
            screen.blit(cursorimgbg, (530,75))




            # Next Upgrade Here
    def pietier(self):
        
        if self.pies <= 20: #Tier 1 - Apple
            current_tier = 0
        if self.pies >= 20: #Tier 2 - Peach for now
            current_tier = 1
        
        self.pie = pygame.transform.scale(pygame.image.load(pie_tiers[current_tier]), (300, 150))
        screen.blit(self.pie,(pie_loct))
    def click(self):
        
        self.mouse_pos = pygame.mouse.get_pos()
        if self.pie.get_rect(topleft=(pie_loct)).collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
             if self.clicked:
                self.pies += self.pies_per_click
                self.clicked = False
        if self.clickupgradeBtn.collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    if self.pies >= self.clickupgradecost:
                        self.pies -= self.clickupgradecost
                        self.pies_per_click += 1
                        self.clickupgradecost = int(self.clickupgradecost * 1.5)
                    self.clicked = False

        

    

    def render(self):
        self.pietier()
        self.click()
        self.upgrades()
        

def enterrecord():
    global username
    global nametyping
    overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    username=""
    while nametyping==True:
        screen.blit(overlay, (0, 0))
        typename = titlefont.render('ENTER YOUR INITIALS:\n'+ username, True, (0,0,0))
        screen.blit(typename, (350, 200))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(username) == 3:
                    nametyping=False
                    open("highscore.txt", "w").write(str(game.mostpies)+" - "+username)
            elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1] 
            elif len(username) < 3 and event.unicode.isalpha():
                    username += event.unicode.upper()
            if len(username) == 3:
                entersubmit = mainfont.render("PRESS ENTER TO SUBMIT", True,(0,0,0))
                screen.blit(entersubmit, (350, 450))
            if event.key == pygame.K_ESCAPE:
                nametyping=False


clock = pygame.time.Clock()
game = Game()

#-------------------------------
#----------- Text -------------#
#-------------------------------

titletext = titlefont.render('Pie-Clicker', True, (0, 0, 0))
piestxt = mainfont.render('Pies: {0}'.format(game.pies), True, (0, 0, 0))
piesperclicktxt = mainfont.render('Pies/Click: {0}'.format(game.pies_per_click), True, (0, 0, 0))
piespersectxt = mainfont.render('Pies/Sec: {0}'.format(game.pies_per_second), True, (0, 0, 0))
recordpiestxt = smallerfont.render('Most Pies: {0}'.format(game.mostpies), True, (0, 0, 0))


#-------------------------------
#---------- The Game ----------#
#-------------------------------

async def main():
    global event
    global nametyping

    run = True
    nametyping=False
    

    while run:
    
        screen.fill ((255,255,255))
        screen.blit(titletext, (120,50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if game.pies > game.mostpies:
            game.mostpies = game.pies
        
        recordpiestxt = smallerfont.render('Your Record Pies: {:.0f}'.format(game.mostpies), True, (0, 0, 0))
        wrecord= open("highscore.txt", "r").read()
        
        worldrecordpiestext = smallerfont.render('World Record Pies: {:.0f}'.format(int(wrecord[:-5])), True, (0, 0, 0))
        screen.blit(worldrecordpiestext, (20,530))
        
        
        if game.mostpies > int(wrecord[:-5]):
            submitrecordBtn = pygame.Rect(10, 550, 200, 30)
            submitrecordtxt = smallerfont.render('Submit Your Record', True, (255, 255, 255))
            pygame.draw.rect(screen, (9, 80, 214), submitrecordBtn, border_radius=5)
            screen.blit(submitrecordtxt, (20, 550))


            mouse_pos = pygame.mouse.get_pos()
            if submitrecordBtn.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    nametyping=True
                    
            if nametyping==True:
                enterrecord()

        piestxt = mainfont.render('Pies: {:.0f}'.format(game.pies), True, (0, 0, 0))
        piesperclicktxt = mainfont.render('Pies/Click: {0}'.format(game.pies_per_click), True, (0, 0, 0))
        piespersectxt = mainfont.render('Pies/Sec: {0}'.format(game.pies_per_second), True, (0, 0, 0))
        
        screen.blit(recordpiestxt, (180,130))
        screen.blit(piestxt, (150,350))
        screen.blit(piesperclicktxt, (150,400))
        screen.blit(piespersectxt, (150,450))
        
        
        game.pies += game.pies_per_second / 60  
        game.render()    

        pygame.display.update()
        await asyncio.sleep(0)  
        clock.tick(60)
        
    pygame.quit()

asyncio.run(main())













#tiers  
# Common -  Apple, Lemon, Blueberry, Cherry, Pumpkin
# Rare -  Peach, Pecan, Coconut, Blackberry, Watermelon
# Exotic - Pineapple on, Jelly Bean, Lollipop, Donut, Pie