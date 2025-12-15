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

bigfont = pygame.font.Font(roboto, 72)
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
lose_text = bigfont.render("YOU HAVE LOST!", True, (222, 53, 38))
again_text = difffont.render("TRY AGAIN?", True, (0,0,0))
lmousetxt = difffont.render("LEFT CLICK: REVEAL TILE", True, (0,0,0))
rmousetxt = difffont.render("RIGHT CLICK: FLAG/UNFLAG TILE", True, (0,0,0))
mmousetxt = difffont.render("MIDDLE CLICK: REVEAL NEIGHBORS", True, (0,0,0))


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
flagicon = pygame.transform.scale(flag, (100, 100))
bomb = pygame.image.load("assets/bomb.png")
boom = pygame.image.load("assets/boom.png")
wrong = pygame.image.load("assets/wrong.png")
clockicon = pygame.image.load("assets/clock.png")
Lmouse = pygame.image.load("assets/Lmouse.png")
Rmouse = pygame.image.load("assets/Rmouse.png")
Mmouse = pygame.image.load("assets/Mmouse.png")

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
                       int((screen_height - self.grid_surface.get_height()) // 1.2))
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
    
    # def display(self):                    This is just for testing in console, is not necessary
    #     for row in self.grid_list:           if ever testing, make sure to also uncomment grid.display() in the main loop
    #         print(row)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if easyBtn.collidepoint(mouse_pos):
                            mainmenu = False
                            return "EASY"
                    if mediumBtn.collidepoint(mouse_pos):
                            mainmenu = False
                            return "MEDIUM"
                    if hardBtn.collidepoint(mouse_pos):
                            mainmenu = False
                            return "HARD"

        
        
        pygame.draw.rect(screen, (9, 80, 214), easyBtn)
        pygame.draw.rect(screen, (9, 80, 214), mediumBtn)
        pygame.draw.rect(screen, (9, 80, 214), hardBtn)
        pygame.draw.rect(screen, (9, 80, 214), titlebg)

        screen.blit(title, (screen_width//2 - title.get_width()//2, 270))
        screen.blit(diff, (screen_width//2 - diff.get_width()//2, 500))
        screen.blit(easy_text, (easyBtn.x + easyBtn.width//2 - easy_text.get_width()//2, easyBtn.y + easyBtn.height//2 - easy_text.get_height()//2))
        screen.blit(medium_text, (mediumBtn.x + mediumBtn.width//2 - medium_text.get_width()//2, mediumBtn.y + mediumBtn.height//2 - medium_text.get_height()//2))
        screen.blit(hard_text, (hardBtn.x + hardBtn.width//2 - hard_text.get_width()//2, hardBtn.y + hardBtn.height//2 - hard_text.get_height()//2))
        screen.blit(flagicon, (920,375))

        pygame.display.flip()
        await asyncio.sleep(0)      
        clock.tick(10)
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
    #Grid.display()     for testing, also uncomment grid.display in class if testing
    global time
    global flagslefttxt, timetxt
    time = 0
    while True:
        for event in pygame.event.get():
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
                if event.button == 2:
                    if Grid.grid_list[mx][my].revealed and Grid.grid_list[mx][my].type == "n":
                        flagged_neighbors = sum(1 for dx in range(-1, 2) for dy in range(-1, 2) 
                                               if Grid.inside_grid(mx + dx, my + dy) and Grid.grid_list[mx + dx][my + dy].flagged)
                        tile_number = numbers.index(Grid.grid_list[mx][my].image) + 1
                        if flagged_neighbors == tile_number:
                            hit_bomb = False
                            for dx in range(-1, 2):
                                for dy in range(-1, 2):
                                    if Grid.inside_grid(mx + dx, my + dy) and not Grid.grid_list[mx + dx][my + dy].flagged and not Grid.grid_list[mx + dx][my + dy].revealed:
                                        if not Grid.dig(mx + dx, my + dy):
                                            hit_bomb = True
                            if hit_bomb:
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
        screen.blit(flagicon, (screen_width//1.7 - flagicon.get_width()//1.7, 50))
        screen.blit(clockicon, (screen_width//2.3 - clockicon.get_width(), 50))
        flagslefttxt = bigfont.render(f"{num_mines - sum(tile.flagged for row in Grid.grid_list for tile in row)}", True, (222, 53, 38))
        screen.blit(flagslefttxt, (screen_width//1.7 + 70 , 70))
        time += clock.get_time()
        timetxt = bigfont.render(f"{time//1000:03}", True, (222, 53, 38))
        screen.blit(timetxt, (screen_width//2.3 + 50 , 70))

        screen.blit(Lmouse, (screen_width//6 - 150, screen_height - 600))
        screen.blit(lmousetxt, (screen_width//6 - 50, screen_height - 590))
        screen.blit(Rmouse, (screen_width//6 - 150, screen_height - 500))
        screen.blit(rmousetxt, (screen_width//2 - 50, screen_height - 490))
        screen.blit(Mmouse, (screen_width//6 - 150, screen_height - 400))
        screen.blit(mmousetxt, (screen_width//6 - 50, screen_height - 390))

        
        Grid.draw(screen)



        pygame.display.flip()
        await asyncio.sleep(0)      
        clock.tick(10)


#-------------------------------

async def loop(): 
    global empty, unknown, flag, mine, explode, wrongflag
    global b1, b2, b3, b4, b5, b6, b7, b8
    global numbers, Grid
    global grid_length, grid_height, num_mines, tilesize
    global difficulty
    while True:
        random.seed()

        difficulty = await main_menu()

        if difficulty=="EASY":
            grid_length = 9
            grid_height = 9
            num_mines = 10
        elif difficulty=="MEDIUM":
            grid_length = 16
            grid_height = 16
            num_mines = 40
        elif difficulty=="HARD":
            grid_length = 22
            grid_height = 22
            num_mines = 99
        
        tilesize = min(screen_width // grid_length, (screen_height-(screen_height//6)) // grid_height)

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
            win = True
            lose = False
        else:
            lose = True
            win = False
        
        if win == True:
            win_text = bigfont.render(f"YOU HAVE WON", True, (16, 125, 38))
            win_textpt2 = bigfont.render(f"{difficulty} DIFFICULTY", True, (16, 125, 38))
            win_textpt3 = bigfont.render(f"IN {time//1000:03} SECONDS!", True, (16, 125, 38))
            endbox = pygame.Rect(screen_width//2 - 300, screen_height//2 - 140, 600, 500)
            againbtn = pygame.Rect(screen_width//2 - 100, screen_height//2 + 225, 250, 100)

        if lose == True:
            endbox = pygame.Rect(screen_width//2 - 300, screen_height//2 - 200, 600, 400)
            againbtn = pygame.Rect(screen_width//2 - 100, screen_height//2 + 80, 250, 100)
        endboxborder = pygame.Rect(endbox.x - 10, endbox.y - 10, endbox.width + 20, endbox.height + 20)
        open = True
        xout = pygame.Rect(endbox.x + endbox.width - 40, endbox.y + 10, 30, 30)
        ended = True

        while ended:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:

                        if open == True:
                            if xout.collidepoint(mouse_pos):
                                againbtn = pygame.Rect(screen_width//6 - 150, screen_height//2 + 100, 250, 100)
                                open = False
                            elif againbtn.collidepoint(mouse_pos):
                                ended = False
                        else:
                            if againbtn.collidepoint(mouse_pos):
                                ended = False

            screen.fill((77, 77, 77))
            Grid.draw(screen)
            screen.blit(flagicon, (screen_width//1.7 - flagicon.get_width()//1.7, 50))
            screen.blit(clockicon, (screen_width//2.3 - clockicon.get_width(), 50))
            screen.blit(flagslefttxt, (screen_width//1.7 + 70 , 70))
            screen.blit(timetxt, (screen_width//2.3 + 50 , 70))

            if open == True:
                
                pygame.draw.rect(screen, (0,0,0), endboxborder)
                pygame.draw.rect(screen, (127,127,127), endbox)
                pygame.draw.rect(screen, (222, 53, 38), xout)

                if win == True:
                    screen.blit(win_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - win_text.get_height()//2))
                    screen.blit(win_textpt2, (screen_width//2 - win_textpt2.get_width()//2, screen_height//2 - win_textpt2.get_height()//2 + 80))
                    screen.blit(win_textpt3, (screen_width//2 - win_textpt3.get_width()//2, screen_height//2 - win_textpt3.get_height()//2 + 160))  

                if lose == True:
                    screen.blit(lose_text, (screen_width//2 - lose_text.get_width()//2, screen_height//2 - lose_text.get_height()//2))
                
                pygame.draw.rect(screen, (9, 80, 214), againbtn)
                screen.blit(again_text, (againbtn.x + againbtn.width//2 - again_text.get_width()//2, againbtn.y + againbtn.height//2 - again_text.get_height()//2))

            else: 
                pygame.draw.rect(screen, (9, 80, 214), againbtn)
                screen.blit(again_text, (againbtn.x + againbtn.width//2 - again_text.get_width()//2, againbtn.y + againbtn.height//2 - again_text.get_height()//2))
        
            pygame.display.flip()
            await asyncio.sleep(0)
            clock.tick(10)
            
                

asyncio.run(loop())
