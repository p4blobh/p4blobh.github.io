import pygame
import asyncio

pygame.init()


Screen_width = 800
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Pie-Clicker')

icon_image = pygame.image.load("assets/PieClicker_logo.png")
pygame.display.set_icon(icon_image)



#-------------------------------
#----------- Fonts ------------#
#-------------------------------
comicsans = "assets/ComicSansMS.ttf"

titlefont = pygame.font.Font(comicsans, 50)
mainfont = pygame.font.Font(comicsans, 30)
smallerfont = pygame.font.Font(comicsans, 20)
upgradefont = pygame.font.Font(comicsans, 14)

#-------------------------------
#----------- Images -----------#
#-------------------------------
applepie = "assets/applepie1.png"
peachpie = "assets/peachpie1.png"
cursorimg = "assets/cursor.png"
grandmaimg = "assets/grandma.png"
ovenimg = "assets/oven.png"

#------- Load Images ----------#

pie_apple = pygame.transform.scale(pygame.image.load(applepie), (300, 150))
pie_peach = pygame.transform.scale(pygame.image.load(peachpie), (300, 150))
pietiersloaded = [pie_apple, pie_peach]

cursorimgload = pygame.image.load(cursorimg)
cursorimgresize = pygame.transform.scale(cursorimgload, (30, 60))
cursorimgbg = cursorimgresize.convert_alpha()  

grandmaimgload = pygame.image.load(grandmaimg)
grandmaimgresize = pygame.transform.scale(grandmaimgload, (45, 55))
grandmaimgbg = grandmaimgresize.convert_alpha()

ovenimgload = pygame.image.load(ovenimg)
ovenimgresize = pygame.transform.scale(ovenimgload, (45, 55))
ovenimgbg = ovenimgresize.convert_alpha()
#-------------------------------
#------- Clicker Setup --------#
#-------------------------------

pie_tiers = [applepie, peachpie]

pie_loct = (120,200)

wrecord= open("highscore.txt", "r").read()

waitrecord = False

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

        #Grandma Upgrade
        self.grandmaupgradeBtn = pygame.Rect(510, 150, 280, 70)
        self.grandmaupgradedesc = upgradefont.render('Grandma: Pies per second +1', True, (0,0,0))
        self.grandmaupgradecost = 50

        #Oven Upgrade
        self.ovenupgradeBtn = pygame.Rect(510, 230, 280, 70)
        self.ovenupgradedesc = upgradefont.render('Oven: Pies per second +5', True, (0,0,0))
        self.ovenupgradecost = 200

        #Record Submission Button
        self.submitrecordBtn = pygame.Rect(15, 575, 275, 22)
        self.submitrecordtxt = smallerfont.render('Submit Your Record (W.I.P)', True, (255, 255, 255))
        
    def upgrades(self):
            pygame.draw.rect(screen, (9, 146, 214), (500,0,300,600))

            #Cursor Upgrade
            self.clickupgradeshowcost = upgradefont.render(f'Cost: {self.clickupgradecost}', True, (0,0,0))
            pygame.draw.rect(screen, (9, 101, 214), self.clickupgradeBtn, border_radius=5)
            screen.blit(self.clickupgradeshowcost, (580, 110))
            screen.blit(self.clickupgradedesc, (580, 80))
            pygame.draw.rect(screen, (9, 80, 214),(520,75,50,60),border_radius=7)
            screen.blit(cursorimgbg, (530,75))

            #Grandma Upgrade
            self.grandmaupgradeshowcost = upgradefont.render(f'Cost: {self.grandmaupgradecost}', True, (0,0,0))
            pygame.draw.rect(screen, (9, 101, 214), self.grandmaupgradeBtn, border_radius=5)
            screen.blit(self.grandmaupgradeshowcost, (580, 190))
            screen.blit(self.grandmaupgradedesc, (580, 160))
            pygame.draw.rect(screen, (9, 80, 214),(520,155,50,60),border_radius=7)
            screen.blit(grandmaimgbg, (524,156))


            #Oven Upgrade
            self.ovenupgradeshowcost = upgradefont.render(f'Cost: {self.ovenupgradecost}', True, (0,0,0))
            pygame.draw.rect(screen, (9, 101, 214), self.ovenupgradeBtn, border_radius=5)
            screen.blit(self.ovenupgradeshowcost, (580, 270))
            screen.blit(self.ovenupgradedesc, (580, 240))
            pygame.draw.rect(screen, (9, 80, 214),(520,235,50,60),border_radius=7)
            screen.blit(ovenimgbg, (524,238))

            #Record Submission Button
            
            if self.mostpies > float(wrecord[:-5]):
                global waitrecord 
                pygame.draw.rect(screen, (9, 80, 214), self.submitrecordBtn, border_radius=6)
                screen.blit(self.submitrecordtxt, (20, 570))
                waitrecord=True

    def pietier(self):
        
        
        current_tier = 0 #Tier 1 - Apple

        if self.pies >= self.grandmaupgradecost: #Tier 2 - Peach
            current_tier = 1
        
        self.pie = pietiersloaded[current_tier]
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
                        self.clickupgradecost = int(self.clickupgradecost * 1.1)
                    self.clicked = False

        if self.grandmaupgradeBtn.collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    if self.pies >= self.grandmaupgradecost:
                        self.pies -= self.grandmaupgradecost
                        self.pies_per_second += 1
                        self.grandmaupgradecost = int(self.grandmaupgradecost * 1.1)
                    self.clicked = False

        if self.ovenupgradeBtn.collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    if self.pies >= self.ovenupgradecost:
                        self.pies -= self.ovenupgradecost
                        self.pies_per_second += 5
                        self.ovenupgradecost = int(self.ovenupgradecost * 1.1)
                    self.clicked = False

        if self.mostpies > float(wrecord[:-5]) and waitrecord==True: 
            if self.submitrecordBtn.collidepoint(self.mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    global nametyping
                    nametyping=True

        

    

    def render(self):
        self.pietier()
        self.click()
        self.upgrades()
        

    
overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 230))

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
typename = titlefont.render('ENTER YOUR NAME:', True, (255,255,255))
entersubmit = mainfont.render("PRESS ENTER TO SUBMIT", True,(255,255,255))



#-------------------------------
#---------- The Game ----------#
#-------------------------------

async def main():
    global event
    global nametyping

    run = True
    nametyping=False
    wrecord= open("highscore.txt", "r").read()
    username = ""
    
    

    while run:
    
        screen.fill ((255,255,255))
        screen.blit(titletext, (145,50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
            if event.type == pygame.KEYDOWN and nametyping:
                if event.key == pygame.K_RETURN:
                    if len(username) == 3:
                        nametyping=False
                        open("highscore.txt", "w").write(str(game.mostpies)+" - "+username)
                        wrecord= open("highscore.txt", "r").read()
                elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1] 
                elif len(username) < 3 and event.unicode.isalpha():
                        username += event.unicode.upper()
                if event.key == pygame.K_ESCAPE:
                    nametyping=False

        if game.pies > game.mostpies:
            game.mostpies = game.pies
        
        recordpiestxt = smallerfont.render('Your Record: {:.0f}'.format(game.mostpies), True, (0, 0, 0))
        worldrecordpiestext = smallerfont.render('World Record: {:.0f} - {}'.format(float(wrecord[:-5]),wrecord[-3:]), True, (0, 0, 0))
                   

        piestxt = mainfont.render('Pies: {:.0f}'.format(game.pies), True, (0, 0, 0))
        piesperclicktxt = mainfont.render('Pies/Click: {0}'.format(game.pies_per_click), True, (0, 0, 0))
        piespersectxt = mainfont.render('Pies/Sec: {0}'.format(game.pies_per_second), True, (0, 0, 0))
        
        screen.blit(recordpiestxt, (20,530))
        screen.blit(piestxt, (150,350))
        screen.blit(piesperclicktxt, (150,400))
        screen.blit(piespersectxt, (150,450))
        screen.blit(worldrecordpiestext, (20,550)) 
        
        
        game.pies += game.pies_per_second / 60  
        game.render()    

        if nametyping==True:
            username_display = titlefont.render(username, True, (255,255,255))

            screen.blit(overlay, (0, 0))
            screen.blit(username_display, (410, 300))
            screen.blit(typename, (230, 200))
           
            if len(username) == 3:
                screen.blit(entersubmit, (270, 430))

        pygame.display.update()
        await asyncio.sleep(0)  
        clock.tick(60)
        
    pygame.quit()

asyncio.run(main())













#tiers  
# Common -  Apple, Lemon, Blueberry, Cherry, Pumpkin
# Rare -  Peach, Pecan, Coconut, Blackberry, Watermelon
# Exotic - Pineapple on, Jelly Bean, Lollipop, Donut, Pie