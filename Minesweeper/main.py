import pygame
import asyncio
import random
#^^^ importing modules to use them to help create the game
pygame.init() #initalizes pygame

screen_width = 1920
screen_height = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")
#sets screen dimensions and gives it a name

icon = pygame.image.load("assets/flag.png") #loads the flag image to use for icon (this doesnt matter for website)
pygame.display.set_icon(icon)

clock = pygame.time.Clock() #sets the clock which is used to set fps for the game

#-------------------------------
#----------- Fonts ------------#
#-------------------------------
roboto =("assets/Roboto.ttf") #downloads the fonts and sets them to use

bigfont = pygame.font.Font(roboto, 72)
menufont = pygame.font.Font(roboto, 48)
difffont = pygame.font.Font(roboto, 36)
tutorialfont = pygame.font.Font(roboto, 32)

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
lmousetxt = tutorialfont.render("REVEAL TILE", True, (0,0,0))
rmousetxt = tutorialfont.render("FLAG/UNFLAG TILE", True, (0,0,0))
mmousetxt = tutorialfont.render("REVEAL NEIGHBOURS", True, (0,0,0))
#creating the texts that dont need to update according to variable changes so it doesnt keep getting loaded

#-------------------------------
#---------- assets ------------#
#-------------------------------
 #sets/loads all the images to variables to use
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

class tile: #this class essentially determines the properties of every tile
    def __init__ (self, x, y, image, type, revealed=False, flagged=False): #initalizes the class and sets its base values, this is only loaded once per game
        self.x,self.y = x*tilesize, y*tilesize
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
    
    def draw(self, surface): #this draws the tiles onto the screen
        if not self.flagged and self.revealed: #if it has not been flagged and revealed, it shows its actual icon (the number or blank)
            surface.blit(self.image, (self.x, self.y))
        elif self.flagged and not self.revealed: #if it has been flagged and not revealed, it shows the flag icon
            surface.blit(flag, (self.x, self.y))  
        elif not self.revealed: #if not revealed, it shows the unknown block
            surface.blit(unknown, (self.x, self.y))
  


class grid: #this class determines the properties of the entire grid
    def __init__ (self): #initalizes the class and gives it some base properties, this is only run once per game
        #quick note, "." means the tile is unrevealed, "x" means the tile is a bomb, "n" means the tile is a number, this is applied to the "type" in the class above

        self.grid_surface = pygame.Surface((grid_length*tilesize, grid_height*tilesize)) #makes the grid the appropriate size according to height, length, and tile size
        self.grid_list = [[tile(col,row,empty, ".") for row in range(grid_length)] for col in range(grid_height)] #this triggers the tile class and creates the appropriate # of tiles and stores them all in a list and makes them unrevealed
        self.offset = ((screen_width - self.grid_surface.get_width()) // 2,
                       int((screen_height - self.grid_surface.get_height()) // 1.2)) #this just helps center the grid onto the screen (offset applied when placing grid on screen)
        self.place_mines() #runs the place mines below
        self.place_numbers() #runs the place numbers below
        self.dug = [] #creates an empty list to store all the tiles that are dug
    def place_mines(self): #this makes random tiles mines
        for e in range(num_mines): #for the # of mines there are, it runs the below
            while True: #will repeat until it lands on a non bomb tile
                x = random.randint(0, grid_length-1)
                y = random.randint(0, grid_height-1) #chooses a random x and y to choose random tile in grid list

                if self.grid_list[x][y].type == ".": #if the tile is empty, this is to prevent the bombs being placed in same place
                    self.grid_list[x][y].image = mine #sets the image to mine
                    self.grid_list[x][y].type = "x" #sets the type of tile to bomb
                    break #when it does it, it breaks the while True loop

    def place_numbers(self): #this is what places the numbers
        for x in range(grid_length):
            for y in range(grid_height): #for every single tile in the grid, will check the following
                if self.grid_list[x][y].type != "x": #if it is not a bomb
                    total = self.check_neighbours(x, y) #will run check_neighbours below to check adjacent squares to assign proper number
                    if total > 0: #if there are any bombs, will asign it as a number tile
                        self.grid_list[x][y].image = numbers[total-1] #numbers list is near bottom pf the file
                        self.grid_list[x][y].type = "n" 
                    

    @staticmethod #not entirely sure tbh but something to do with not having to include "self" to prevent returning 3 arguments instead of 2 and how it runs as if it was not in a class
    def inside_grid(x, y): #makes sure that location that is being checked is within the grid (if looking at a tile at an edge)
        return 0 <= x < grid_length and 0 <= y < grid_height #this returns a True or False to check if the x/y coord is in the grid     

    def check_neighbours(self, x, y):
        total = 0 #sets the total at 0 everytime this is called
        for dx in range(-1, 2): 
            for dy in range(-1, 2): #checks the 8 squares around the tile (3x3)
                neighbour_x = x + dx 
                neighbour_y = y + dy #for example if tile coordinate is (5,5) and this neighbour is (4,4), it adds -1 to both x and y to get the neighbours coords
                if self.inside_grid(neighbour_x, neighbour_y) and self.grid_list[neighbour_x][neighbour_y].type == "x": #if the tile is both inside and grid and a bomb
                    total += 1 #adds to the total (number of mines around the tile)
        return total #returns the total number of mines around the tile
      
    def draw(self, screen): #draws the entire grid on the screen
        for row in self.grid_list:
            for tile in row:
                tile.draw(self.grid_surface)
        screen.blit(self.grid_surface, self.offset) #places it onto the screen with the offset determined earlier
    
    def dig(self,x,y): #this is when the player digs a tile
        self.dug.append((x,y)) #adds the tile to the dug list
        if self.grid_list[x][y].type == "x": #if its a bomb, reveals it, changes its image, and returns false (game over)
            self.grid_list[x][y].revealed = True
            self.grid_list[x][y].image = explode
            return False
        
        elif self.grid_list[x][y].type == "n": #if it is a number, reveals it and returns true (game not over)
            self.grid_list[x][y].revealed = True
            return True
        
        self.grid_list[x][y].revealed = True #reveals the tile (this is for blank tiles)

        for row in range(x-1,x+2): #this checks every neighbour and reveals them too, they wont be bombs since this is only for blank tiles
            for col in range(y-1,y+2):
                if self.inside_grid(row,col):
                    if (row,col) not in self.dug: #if not already dug
                        self.dig(row,col) #will call this again to run the same things to that tile
        return True #returns with true (game not over)
    
    # def display(self):                    This is just for testing in console, is not necessary
    #     for row in self.grid_list:           if ever testing, make sure to also uncomment grid.display() in the main loop
    #         print(row)

#-------------------------------
#--------- Main Menu ----------#
#-------------------------------


#this and anything else that has async in it is for displaying on the website using pygbag
async def main_menu(): #this is for the starting screen
    mainmenu = True #enables it
    easyBtn = pygame.Rect(860, 600, 200, 50)
    mediumBtn = pygame.Rect(860, 700, 200, 50)
    hardBtn = pygame.Rect(860, 800, 200, 50)
    titlebg = pygame.Rect(765, 250, 400, 110) #making to display on screen rects
    while mainmenu:
        screen.fill((127, 127, 127)) #fills screen background
        for event in pygame.event.get(): #for every event that occurs, in this case it is beinng used for mouse presses
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #if the button is pressed down and it is the left button, will check mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    #if the mouse position is overlapping with any of these three buttons, will end main  menu loop and return appropriate difficulty to loop below
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
        #^^^^ draws the rect on screen

        screen.blit(title, (screen_width//2 - title.get_width()//2, 270))
        screen.blit(diff, (screen_width//2 - diff.get_width()//2, 500))
        screen.blit(easy_text, (easyBtn.x + easyBtn.width//2 - easy_text.get_width()//2, easyBtn.y + easyBtn.height//2 - easy_text.get_height()//2))
        screen.blit(medium_text, (mediumBtn.x + mediumBtn.width//2 - medium_text.get_width()//2, mediumBtn.y + mediumBtn.height//2 - medium_text.get_height()//2))
        screen.blit(hard_text, (hardBtn.x + hardBtn.width//2 - hard_text.get_width()//2, hardBtn.y + hardBtn.height//2 - hard_text.get_height()//2))
        screen.blit(flagicon, (920,375))
        #^^^^^^ adds the text and icons onto the screen

        pygame.display.flip() #updates the screen to show everything added onto the screen
        await asyncio.sleep(0) #this is for the website
        clock.tick(10) #this is the fps of the game, since minesweeper, high frame rate is not required (typical rate for web games is 60)
#-------------------------------
#------------ Game ------------#
#-------------------------------

def checkforwin(): #this function checks if every none bomb tile has been revealed and if so, will return true
    for row in Grid.grid_list:
            for tile in row:
                if tile.type != "x" and not tile.revealed:
                    return False
    return True

async def main(): #this functon is for the actual game
    #Grid.display()     for testing, also uncomment grid.display in class if testing
    global time
    global flagslefttxt, timetxt #globals these variables to be accessed anywhere, even outside this function
    time = 0 #sets the time to 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos() #mx and my are the position of the mouse when a button has been clicked
                mx = (mx - Grid.offset[0]) // tilesize
                my = (my - Grid.offset[1]) // tilesize # minuses mx and my by offset then divides by tile size to place it on appropriate grid tile

                if not Grid.inside_grid(mx, my):
                    continue #if outside of grid, ends this loop
                if event.button == 1: #if left button is clicked
                    if not Grid.grid_list[mx][my].flagged: #if it is not flagged (if flagged nothing will happen)
                        if not Grid.dig(mx, my): #runs dig as shown earlier, if returns False (bomb hit), the following happens
                            for row in Grid.grid_list: 
                                for tile in row: #for every tile
                                    if tile.flagged and tile.type != "x": #if a tile is flagged and not a bomb, will show wrong flag image
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = wrongflag
                                    elif tile.type == "x": #if a bomb, will reveal it
                                        tile.revealed = True
                            
                            return False #returns to loop below with false (meaning game over)
                if event.button == 2: #if middle button is clicked
                    if Grid.grid_list[mx][my].revealed and Grid.grid_list[mx][my].type == "n": #only if tile is a number and revealed
                        flagged_neighbours = sum(1 for dx in range(-1, 2) for dy in range(-1, 2) #for the 3x3 around it
                                                 if Grid.inside_grid(mx + dx, my + dy) and Grid.grid_list[mx + dx][my + dy].flagged)#only counts if it is both in the grid and flagged
                        tile_number = numbers.index(Grid.grid_list[mx][my].image) + 1 #the number of the tile (+1 added because lists start at 0, not 1)
                        if flagged_neighbours == tile_number: #will only proceed if flags are equal to the number of the tile - like original minesweeper
                            hit_bomb = False
                            for dx in range(-1, 2):
                                for dy in range(-1, 2): #checks the 3x3 around the tile
                                    if Grid.inside_grid(mx + dx, my + dy) and not Grid.grid_list[mx + dx][my + dy].flagged and not Grid.grid_list[mx + dx][my + dy].revealed:
                                        if not Grid.dig(mx + dx, my + dy): #if a bomb is hit, hit_bomb variable is set to true
                                            hit_bomb = True
                            if hit_bomb: #if it hits a bomb, will do same things as above when player digs a bomb
                                for row in Grid.grid_list:
                                    for tile in row:
                                        if tile.flagged and tile.type != "x":
                                            tile.flagged = False
                                            tile.revealed = True
                                            tile.image = wrongflag
                                        elif tile.type == "x":
                                            tile.revealed = True
                                return False 
                if event.button == 3: #if right mouse button is clicked, the tile will become a flaggef tile
                    if not Grid.grid_list[mx][my].revealed: #if not revealed
                        if Grid.grid_list[mx][my].flagged or sum(tile.flagged for row in Grid.grid_list for tile in row) < num_mines: #if already flagged OR there are still flags remaining
                            Grid.grid_list[mx][my].flagged = not Grid.grid_list[mx][my].flagged #will make it opposite of what it is - if not flagged, becomes flagged, vice versa
        
        
        if checkforwin() == True: #if it returns true
            for row in Grid.grid_list:
                for tile in row:
                    if not tile.revealed: #if not already revealed
                        tile.flagged = True #if not already flagged, theyll be auto flagged
            return True #returns to loop with true (meaning game won)
       
        screen.fill((77, 77, 77)) #sets background of scren
        screen.blit(flagicon, (screen_width//1.7 - flagicon.get_width()//1.7, 50))
        screen.blit(clockicon, (screen_width//2.3 - clockicon.get_width(), 50))
        flagslefttxt = bigfont.render(f"{num_mines - sum(tile.flagged for row in Grid.grid_list for tile in row)}", True, (222, 53, 38))
        screen.blit(flagslefttxt, (screen_width//1.7 + 70 , 70))
        time += clock.get_time() #adds time for the timer
        timetxt = bigfont.render(f"{time//1000:03}", True, (222, 53, 38))
        screen.blit(timetxt, (screen_width//2.3 + 50 , 70))

        screen.blit(Lmouse, (screen_width//6 - 300, screen_height - 650))
        screen.blit(lmousetxt, (screen_width//6 - 200, screen_height - 640))
        screen.blit(Rmouse, (screen_width//6 - 300, screen_height - 550))
        screen.blit(rmousetxt, (screen_width//6 - 200, screen_height - 540))
        screen.blit(Mmouse, (screen_width//6 - 300, screen_height - 450))
        screen.blit(mmousetxt, (screen_width//6 - 200, screen_height - 440))
        #^^^^^^^^^^A bunch of text and images just added to the screen
        
        Grid.draw(screen) #draws the grid on the screen



        pygame.display.flip() #updates the screen to show everything added onto the screen
        await asyncio.sleep(0) 
        clock.tick(10) 
#-------------------------------

async def loop(): #this is the loop which will never end 
    global empty, unknown, flag, mine, explode, wrongflag
    global b1, b2, b3, b4, b5, b6, b7, b8
    global numbers, Grid
    global grid_length, grid_height, num_mines, tilesize
    global difficulty
    #^^^^^Globals a bunch of variables to be accessed from anywhere
    while True:
        random.seed() #makes it so pygame resets random factors, otherwise game is the same everytime for some reason

        difficulty = await main_menu() #runs the main_menu() function and whatever is returned is what difficulty is set to

        if difficulty=="EASY":  #sets length,height and mine # depending on difficulty
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
        #^ SEts tilesize to the smallest number between the two calculations
        # right now, it will always be the second one, i was originally planning to add a custom difficulty where the player could choose their size, might still do so in future

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
        #^^^^^^^^^Scales all the images according to tile size
        numbers = [b1, b2, b3, b4, b5, b6, b7, b8] #assigns all the number tiles to a list
        Grid = grid() #initalizes the grid() class
        
        if await main() == True: #runs the main() function
            win = True
            lose = False
        else:
            lose = True
            win = False
        
        if win == True: #win text and box(which is slightly different size from lose box)
            win_text = bigfont.render(f"YOU HAVE WON", True, (16, 125, 38))
            win_textpt2 = bigfont.render(f"{difficulty} DIFFICULTY", True, (16, 125, 38))
            win_textpt3 = bigfont.render(f"IN {time//1000:03} SECONDS!", True, (16, 125, 38))
            endbox = pygame.Rect(screen_width//2 - 350, screen_height//2 - 140, 700, 500)
            againbtn = pygame.Rect(screen_width//2 - 100, screen_height//2 + 225, 250, 100)

        if lose == True:
            endbox = pygame.Rect(screen_width//2 - 300, screen_height//2 - 200, 600, 400)
            againbtn = pygame.Rect(screen_width//2 - 100, screen_height//2 + 80, 250, 100)
        endboxborder = pygame.Rect(endbox.x - 10, endbox.y - 10, endbox.width + 20, endbox.height + 20)
        open = True
        xout = pygame.Rect(endbox.x + endbox.width - 40, endbox.y + 10, 30, 30) #x out of box that covers part of grid
        ended = True

        while ended:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:

                        if open == True: #checks if mouse clicks the red box or play again button
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
            screen.blit(timetxt, (screen_width//2.3 + 50 , 70)) #stuff from the game so it is still displayed

            if open == True:
                
                pygame.draw.rect(screen, (0,0,0), endboxborder)
                pygame.draw.rect(screen, (127,127,127), endbox)
                pygame.draw.rect(screen, (222, 53, 38), xout) 
                #^The box containing text below

                #win and lose text
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
            
                

asyncio.run(loop()) #begins the actual code beginning from the start of loop() function
