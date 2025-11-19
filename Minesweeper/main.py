import pygame
import asyncio
import random
pygame.init()

screen_width = 1920
screen_height = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

icon = pygame.image.load("assets/flag.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

#-------------------------------
#----------- Fonts ------------#
#-------------------------------
roboto =("assets/Roboto.ttf")

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
#---------- assets ------------#
#-------------------------------

unknown = pygame.image.load("assets/unknown.png")
b = pygame.image.load("assets/b.png")
b1 = pygame.image.load("assets/b1.png")
b2 = pygame.image.load("assets/b2.png")
b3 = pygame.image.load("assets/b3.png")
b4 = pygame.image.load("assets/b4.png")
b5 = pygame.image.load("assets/b5.png")
b6 = pygame.image.load("assets/b6.png")
b7 = pygame.image.load("assets/b7.png")
b8 = pygame.image.load("assets/b8.png")
flag = pygame.image.load("assets/flag.png")
bomb = pygame.image.load("assets/bomb.png")
boom = pygame.image.load("assets/boom.png")
wrong = pygame.image.load("assets/wrong.png")

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
    
    def draw(self, surface): 
        if not self.flagged and self.revealed:
            surface.blit(self.image, (self.x, self.y))
        elif self.flagged and not self.revealed:
            surface.blit(flag, (self.x, self.y))  
        elif not self.revealed:
            surface.blit(unknown, (self.x, self.y))
    def __repr__(self):
        return self.type


class grid:
    def __init__ (self):
        self.grid_surface = pygame.Surface((grid_length*tilesize, grid_height*tilesize))
        self.grid_list = [[tile(col,row,empty, ".") for row in range(grid_length)] for col in range(grid_height)] 
        self.offset = ((screen_width - self.grid_surface.get_width()) // 2,
                       (screen_height - self.grid_surface.get_height()) // 2)
        self.place_mines()
        self.place_numbers()
        self.dug = []

    def place_mines(self):
        for e in range(num_mines):
            while True:
                x = random.randint(0, grid_length-1)
                y = random.randint(0, grid_height-1)

                if self.grid_list[x][y].type == ".":
                    self.grid_list[x][y].image = mine
                    self.grid_list[x][y].type = "x"
                    break

    def place_numbers(self):
        for x in range(grid_length):
            for y in range(grid_height):
                if self.grid_list[x][y].type != "x":
                    total = self.check_neighbors(x, y)
                    if total > 0:
                        self.grid_list[x][y].image = numbers[total-1]
                        self.grid_list[x][y].type = "n"
                    

    @staticmethod
    def inside_grid(x, y): 
        return 0 <= x < grid_length and 0 <= y < grid_height

    def check_neighbors(self, x, y):
        total = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbour_x = x + dx
                neighbour_y = y + dy
                if self.inside_grid(neighbour_x, neighbour_y) and self.grid_list[neighbour_x][neighbour_y].type == "x":
                    total += 1
        return total
     
    def draw(self, screen):
        for row in self.grid_list:
            for tile in row:
                tile.draw(self.grid_surface)
        screen.blit(self.grid_surface, self.offset)
    
    def dig(self,x,y):
        self.dug.append((x,y))
        if self.grid_list[x][y].type == "x":
            self.grid_list[x][y].revealed = True
            self.grid_list[x][y].image = explode
            return False
        
        elif self.grid_list[x][y].type == "n":
            self.grid_list[x][y].revealed = True
            return True
        
        self.grid_list[x][y].revealed = True

        for row in range(max(0,x-1), min(grid_length-1, x+1)+1): #this checks every neighbour and reveals them too
            for col in range(max(0,y-1), min(grid_height-1, y+1)+1):
                if (row,col) not in self.dug:
                    self.dig(row,col)
        return True
        

    def display(self):
        for row in self.grid_list:
            print(row)

#-------------------------------
#--------- Main Menu ----------#
#-------------------------------



async def main_menu():
    mainmenu = True
    easyBtn = pygame.Rect(860, 600, 200, 50)
    mediumBtn = pygame.Rect(860, 700, 200, 50)
    hardBtn = pygame.Rect(860, 800, 200, 50)
    titlebg = pygame.Rect(765, 250, 400, 110)
    while mainmenu:
        screen.fill((127, 127, 127))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        

        mouse_pos = pygame.mouse.get_pos()

        if easyBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                mainmenu = False
                return "easy"
        if mediumBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                mainmenu = False
                return "medium"
        if hardBtn.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                mainmenu = False
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
        screen.blit(flag, (920,375))

        pygame.display.flip()
        await asyncio.sleep(0)      
        clock.tick(50)
#-------------------------------
#------------ Game ------------#
#-------------------------------

def checkforwin():
    for row in Grid.grid_list:
            for tile in row:
                if tile.type != "x" and not tile.revealed:
                    return False
    return True

async def main():
    Grid.display()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mx, my = pygame.mouse.get_pos()
                mx = (mx - Grid.offset[0]) // tilesize
                my = (my - Grid.offset[1]) // tilesize

                if mx < 0 or my < 0: #both of these are if outside the grid
                    continue
                if not Grid.inside_grid(mx, my):
                    continue

                if event.button == 1:
                    if not Grid.grid_list[mx][my].flagged:
                        if not Grid.dig(mx, my):
                            for row in Grid.grid_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "x":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = wrongflag
                                    elif tile.type == "x":
                                        tile.revealed = True
                            return False
                            
                if event.button == 3:
                    if not Grid.grid_list[mx][my].revealed:
                        Grid.grid_list[mx][my].flagged = not Grid.grid_list[mx][my].flagged
        
        
        if checkforwin() == True:
            for row in Grid.grid_list:
                for tile in row:
                    if not tile.revealed:
                        tile.flagged = True
            return True
        screen.fill((77, 77, 77))

        
        Grid.draw(screen)



        pygame.display.flip()
        await asyncio.sleep(0)      
        clock.tick(50)


#-------------------------------

async def loop():
    global empty, unknown, flag, mine, explode, wrongflag
    global b1, b2, b3, b4, b5, b6, b7, b8
    global numbers, Grid
    global grid_length, grid_height, num_mines, tilesize

    while True:
        difficulty = await main_menu()

        if difficulty=="easy":
            grid_length = 9
            grid_height = 9
            num_mines = 10
            tilesize = 64
            menu = False
        elif difficulty=="medium":
            grid_length = 16
            grid_height = 16
            num_mines = 40
            tilesize = 32
            menu = False
        elif difficulty=="hard":
            grid_length = 22
            grid_height = 22
            num_mines = 99
            tilesize = 28
            menu = False
        

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
        numbers = [b1, b2, b3, b4, b5, b6, b7, b8]
        Grid = grid()
        
        if await main() == True:
            print("You win")
        else:
            print("You lose")
        

asyncio.run(loop())
