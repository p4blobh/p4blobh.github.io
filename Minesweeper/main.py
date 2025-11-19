import pygame
import asyncio

pygame.init()

screen_width = 1920
screen_height = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

icon = pygame.image.load("Minesweeper/assets/flag.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

#-------------------------------
#----------- Fonts ------------#
#-------------------------------
roboto =("Minesweeper/assets/Roboto.ttf")

menufont = pygame.font.Font(roboto, 48)
difffont = pygame.font.Font(roboto, 36)

#-------------------------------
#----------- Text -------------#
#-------------------------------
title = menufont.render("MINESWEEPER", True, (0, 0, 0))
diff = menufont.render("SELECT DIFFICULTY", True, (0, 0, 0))
easy_text = difffont.render("EASY", True, (0, 0, 0))
medium_text = difffont.render("MEDIUM", True, (0, 0, 0))
hard_text = difffont.render("HARD", True, (0, 0, 0))

#-------------------------------
#---------- Minesweeper/assets ------------#
#-------------------------------

unknown = pygame.image.load("Minesweeper/assets/unknown.png")
b = pygame.image.load("Minesweeper/assets/b.png")
b1 = pygame.image.load("Minesweeper/assets/b1.png")
b2 = pygame.image.load("Minesweeper/assets/b2.png")
b3 = pygame.image.load("Minesweeper/assets/b3.png")
b4 = pygame.image.load("Minesweeper/assets/b4.png")
b5 = pygame.image.load("Minesweeper/assets/b5.png")
b6 = pygame.image.load("Minesweeper/assets/b6.png")
b7 = pygame.image.load("Minesweeper/assets/b7.png")
b8 = pygame.image.load("Minesweeper/assets/b8.png")
flag = pygame.image.load("Minesweeper/assets/flag.png")
bomb = pygame.image.load("Minesweeper/assets/bomb.png")
boom = pygame.image.load("Minesweeper/assets/boom.png")
wrong = pygame.image.load("Minesweeper/assets/wrong.png")

#-------------------------------
#----------- Set Up -----------#
#-------------------------------

class tile:
    def __init__ (self, x, y, image, type, revealed=False, flagged=False):  
        self.x,self.y = x*tilesize, y*tilesize
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
        
    def __repr__(self):
        return self.type

class grid:
    def __init__ (self):
        self.grid_surface = pygame.Surface((grid_length*tilesize, grid_height*tilesize))
        self.grid_list = [[tile(col,row,unknown, ".")  for row in range(grid_height)] for col in range(grid_length)]

    def display(self):
        for row in self.grid_list:
            print(row)

#-------------------------------
#--------- Main Menu ----------#
#-------------------------------



async def main_menu():
    menu = True
    easyBtn = pygame.Rect(860, 600, 200, 50)
    mediumBtn = pygame.Rect(860, 700, 200, 50)
    hardBtn = pygame.Rect(860, 800, 200, 50)
    titlebg = pygame.Rect(765, 250, 400, 110)
    while menu:
        screen.fill((127, 127, 127))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        

        mouse_pos = pygame.mouse.get_pos()

        if easyBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return "easy"
        if mediumBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return "medium"
        if hardBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return "hard"
        
        pygame.draw.rect(screen, (9, 80, 214), easyBtn)
        pygame.draw.rect(screen, (9, 80, 214), mediumBtn)
        pygame.draw.rect(screen, (9, 80, 214), hardBtn)
        pygame.draw.rect(screen, (9, 80, 214), titlebg)

        screen.blit(title, (screen_width//2 - title.get_width()//2, 270))
        screen.blit(diff, (screen_width//2 - diff.get_width()//2, 500))
        screen.blit(easy_text, (easyBtn.x + easyBtn.width//2 - easy_text.get_width()//2, easyBtn.y + easyBtn.height//2 - easy_text.get_height()//2))
        screen.blit(medium_text, (mediumBtn.x + mediumBtn.width//2 - medium_text.get_width()//2, mediumBtn.y + mediumBtn.height//2 - medium_text.get_height()//2))
        screen.blit(hard_text, (hardBtn.x + hardBtn.width//2 - hard_text.get_width()//2, hardBtn.y + hardBtn.height//2 - hard_text.get_height()//2))
        screen.blit(flag, (100,100))

        pygame.display.update()
        await asyncio.sleep(0)      
        clock.tick(20)
#-------------------------------
#------------ Game ------------#
#-------------------------------

async def main():

    grids = grid()
    grids.display()




    pygame.display.update()
    await asyncio.sleep(0)      
    clock.tick(20)


while True:
    difficulty = asyncio.run(main_menu())

    if difficulty=="easy":
        grid_length = 9
        grid_height = 9
        num_mines = 10
        tilesize = 64

    elif difficulty=="medium":
        grid_length = 16
        grid_height = 16
        num_mines = 40
        tilesize = 32

    elif difficulty=="hard":
        grid_length = 22
        grid_height = 22
        num_mines = 99
        tilesize = 28
    
    empty = pygame.transform.scale(b, (tilesize, tilesize))
    unknown = pygame.transform.scale(unknown, (tilesize, tilesize))
    flag = pygame.transform.scale(flag, (tilesize, tilesize))
    mine = pygame.transform.scale(bomb, (tilesize, tilesize))
    explode = pygame.transform.scale(boom, (tilesize, tilesize))
    wrongflag = pygame.transform.scale(wrong, (tilesize, tilesize))
    b1 = pygame.transform.scale(b1, (tilesize, tilesize))
    b2 = pygame.transform.scale(b2, (tilesize, tilesize))
    b3 = pygame.transform.scale(b3, (tilesize, tilesize))
    b4 = pygame.transform.scale(b4, (tilesize, tilesize))
    b5 = pygame.transform.scale(b5, (tilesize, tilesize))
    b6 = pygame.transform.scale(b6, (tilesize, tilesize))
    b7 = pygame.transform.scale(b7, (tilesize, tilesize))
    b8 = pygame.transform.scale(b8, (tilesize, tilesize))

    asyncio.run(main())




