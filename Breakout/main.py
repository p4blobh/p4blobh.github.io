import pygame
import asyncio
from random import uniform 
#^^^ Importing modules to create the game

pygame.init() #initalizes pygame

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")
#^^^^ sets screen width and height as well as sets caption (name)
clock = pygame.time.Clock() #sets the clock which will be used to set fps for game

#-------------------------------
#----------- Fonts ------------#
#-------------------------------

blockyfont = ("assets/BoldPixels.ttf") #file path to the font

bigfont = pygame.font.Font(blockyfont, 72)
smallerfont = pygame.font.Font(blockyfont, 46)
evensmallerfont = pygame.font.Font(blockyfont, 36)
#^^^Creates fonts to use for texts
starttxt = smallerfont.render("PRESS UP/W KEY TO START", True, (255, 255, 255))
instructions = evensmallerfont.render("USE ARROW KEYS OR A/D TO MOVE", True, (255, 255, 255))

wintxt = smallerfont.render("CONGRATULATIONS!",True, (255,255,255))
wintxtpt2 = smallerfont.render("YOU HAVE WON",True, (255,255,255))

losttxt = smallerfont.render("GAME OVER", True, (255,255,255))

againtxt = smallerfont.render("TRY AGAIN?", True, (255,255,255))
#^^^^^^ Creating the texts that aren't needed to be refreshed due to variable changes 

#-------------------------------
#----------- Set Up -----------#
#-------------------------------
yblockcol = (181, 184, 29)
gblockcol = (27, 130, 27)
oblockcol = (189, 116, 32)
rblockcol = (171, 31, 19)
#sets the colours im using for the blocks

rows = 8
columns = 10
score = 0
#^^^sets the rows, columns, and score 
cheat = False
once = True
#two variables for a quick win for demonstration, needed to set here so it's before any classes
class blocks: #this is the class that essentially determines any properties of the blocks
    def __init__ (self): #initalizes the class, sets some values, this will not be used after inital startup
        self.gap = 5
        self.width = (screen_width - (columns + 1) * self.gap) // columns
        self.height = 30
        self.topgap = 70

    def wall(self): #creates all the blocks and tells them where to go and some values, this is called at every round startup
        self.blocks = []
        single_block = [] #[] are lists to store all the blocks and their properties
        for row in range(rows):
            block_row = []
            for column in range (columns): #for every block (each one for row and column) sets its x and y value and makes it a rect (essentially a surface)
                blockx = self.gap + column * (self.width + self.gap)
                blocky = self.topgap + row * (self.height + self.gap)
                rect = pygame.Rect(blockx, blocky, self.width, self.height)
                
                if row < 8:
                    strength = 1
                if row < 6:
                    strength = 2
                if row < 4:
                    strength = 3
                if row < 2:
                    strength = 4
                #^^^^configures its strength depending on which row it is in
                single_block = [rect, strength] #adds the rect and the strength to a list called single_block
                block_row.append(single_block) #adds the single_block list to block_row list
            
            self.blocks.append(block_row) 
            #after every block in a row gets set, the block_row list gets added to self.blocks list, it then moves onto the row of the next column 
    def draw(self): #this is the part that actually draws the rect onto the screen
        for row in self.blocks:
            for block in row: #looks at every individual block, block[1] is the strength of the block and colour gets assigned based on it
                if block[1] == 1:
                    colour = yblockcol
                if block[1] == 2:
                    colour = gblockcol
                if block[1] == 3:
                    colour = oblockcol
                if block[1] == 4:
                    colour = rblockcol 
                if block[1] >= 1: # if the block has a strength that is greater than/equal to 1, then it draws (to avoid strength of 0 being drawn invisibly)
                    pygame.draw.rect(screen, colour, block[0])

class paddle: #this is the object that the player controls at the bottom
    def __init__ (self): #initalizes  properties, like stated previously
        self.width = (screen_width // columns) * 2
        self.height =20
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 50
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self): # this is what checks if the player is clicking a button and then moves the player accordingly
        self.direction = 0
        keys = pygame.key.get_pressed()  
        #vvv also checks if the paddle is going to leave the screen and prevents it from moving if so
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0: #if player clicks left or A, moves  player to left
            self.rect.x -= self.speed #moves the rectangle (paddle) to the left by going minus speed
            self.direction = -1 #sets a direction (-1 being to the left) to apply to the ball
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width: #if players clicks right or D, moves player to right
            self.rect.x += self.speed
            self.direction = 1 #like above, 1 is to the right
    
    def draw(self): #draws the rect (paddle) to the screen
        pygame.draw.rect(screen, (26, 109, 186), self.rect)


class ball: #class that includes everything about the ball
    def __init__ (self, x, y): #initalizes properties of ball, like classes above
        self.radius = 10
        self.x = x - self.radius
        self.y = y - self.radius
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2) #yes, the ball is actually a square
        self.speed_x = uniform(-5, 5) #sets the x speed (left/right) of the ball to a random number (including decimals) between -5 to 5
        while self.speed_x in range(-2,2):#if that random number is between -2 and 2, it gets resetting until it is not in that range
            self.speed_x = uniform(-5, 5)
        self.speed_y = -5 
        self.maxspeed = 15
        self.minspeed = -15
        

    def move(self, player, wall): #this is what moves the ball and looks at all its collisions
        global score, once #globals these variables so that it is accesible everywhere, meaning outside of this class
        
        if cheat==True and once == True: #this is for a quick victory to demonstrate victory, sets the size of the ball large
            self.radius = 50
            self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
            self.speed_y = 20
            self.speed_x = 20 #makes it super fast
            once = False #so it doesnt keep resetting the position of the ball so it doesnt move

        collision_threshold = 13 #this is so that the ball doesnt get inside the block or player
        self.lose = False
        #block walls collisions
        destroyed = True
        rowcount = 0
        for row in wall.blocks:
            blockcount = 0
            for block in row: #checks every block
                if self.rect.colliderect(block[0]): #if it collides with one of the rect (block[0]), will change its speed accordingly
                    if cheat ==False:#so that the ball doesnt bounce while quick win so it's faster
                        if abs(self.rect.bottom - block[0].top) < collision_threshold and self.speed_y > 0: #from above
                            self.speed_y *= -1 #will go up (change y (up/down) to opposite way)
                        if abs(self.rect.top - block[0].bottom) < collision_threshold and self.speed_y < 0: #from below
                            self.speed_y *= -1 #will go down (change y (up/down) to opposite way)
                        if abs(self.rect.right - block[0].left) < collision_threshold and self.speed_x > 0: #from left
                            self.speed_x *= -1 #will go left (change x (left/right) to opposite way)
                        if abs(self.rect.left - block[0].right) < collision_threshold and self.speed_x < 0: #from right
                            self.speed_x *= -1 #will go right (change x (left/right) to opposite way)
                    if cheat ==True: 
                        wall.blocks[rowcount][blockcount][1] -= 4 #if the cheat is enabled, will instant destroy any block no matter strength
                    if wall.blocks[rowcount][blockcount][1] > 1: #otherwise will lower strength by 1 if hit without cheat and its strength is greater than 1
                        wall.blocks[rowcount][blockcount][1] -= 1
                    else: #if strength is 1 or lower, will make strength 0 and delete it by making the rect have no width/height
                        wall.blocks[rowcount][blockcount][1] = 0 
                        wall.blocks[rowcount][blockcount][0] = (0,0,0,0) # deletes the block
                    score += 50 #adds 50 to the score when a block is hit
                if wall.blocks[rowcount][blockcount][1] > 0: #if any block still has a strength, destroyed will be set to false
                    destroyed = False
                blockcount += 1 #adds one to blockcount for when adjusting blocks above
            rowcount += 1 #adds one to rowcount for when adjusting blocks above
        if destroyed: #if every single block has strength of 0, will return with a value of 'win'
            return 'win'
        #border (the wall) collisions
        if self.rect.left <= 0 or self.rect.right >= screen_width: #if it hits the left or right wall, x (left/right) speed will inverse
            self.speed_x *= -1
        if self.rect.top <= 0: #if it hits the top, y (up/down) speed will inverse
            self.speed_y *= -1
        if self.rect.bottom >= screen_height and cheat == False: #if it hits the bottom, will set lose to true (unless cheat is active)
            self.lose = True
        if self.rect.bottom >= screen_height and cheat == True: #makes it inverse y speed if cheat is active
            self.speed_y *= -1
            
        self.rect.x += self.speed_x #this adjusts the location of the rect (the ball) according to the speed
        self.rect.y += self.speed_y

        #player collisions
        if self.rect.colliderect(player.rect):
            self.speed_x *= 1.05 #increases the x (right/left) speed of ball by *1.05 when it hits the player
            if abs(self.rect.bottom - player.rect.top) < collision_threshold and self.speed_y > 0: #this is if moving down from above paddle and not hitting left or right side
                self.speed_y *= -1
                self.speed_x += player.direction #adds -1/1 to speed depending on if player is moving in the direction
                if self.speed_x > self.maxspeed and cheat==False: #sets the max speed and ensures it doesnt go over unless cheat active
                    self.speed_x = self.maxspeed
                elif self.speed_x < self.minspeed and cheat ==False: #if going left instead of right
                    self.speed_x = self.minspeed
            else:
                self.speed_x *= -1 #if it hits the right or left of the player (this means they will lose though)
            self.speed_y *= 1.01 #increases the y (up/down) speed of ball every time it hits the player by *1.01
            if self.speed_y < -12 and cheat ==False: #sets that max y speed to -12 (- means going up which it is when hitting player)
                self.speed_y = -12
                  
        return self.lose #returns whether lose is True/False

    def draw(self): #draws the rect as a circle 
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
        

#-------------------------------
#------------ Game ------------#
#-------------------------------
async def loop(): #this is the main game loop which is always active
    while True:
        global score, cheat, once #globals these variables so it is accessible everywhere (including classes)
        running = True
        presstostart = True
        firsttime = True
        cheat = False
        once = True 
        pt1=False
        pt2=False
        pt3=False #these 3 are for enabling the cheat
        #setting values to true/false for various reasons, such as running being true so that it doesnt loop this part until game resets
        score = 0 #sets score to 0 every game reset
        ballsleft = 3 #3 lives for the player
        buffer = pygame.time.get_ticks() + 700 #adds a buffer so that game doesnt immedietly start after losing a life
        time = 0 #sets the time to 0
        
        wall = blocks() #this basically activates/initalizes blocks() class 
        wall.wall() #runs the wall part of the blocks class
        player = paddle() #initalizes the paddle() class

        while running:
            startkey = False #this is for the beginning of the game (w/up to start the game)
            won = False
            lost = False
            for event in pygame.event.get(): #checks every event happening, which in this case is used for key presses
                if event.type == pygame.QUIT: #if the player quits the game, it will actually close (this doesnt matter for the website)
                    pygame.quit()
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_UP] or keys[pygame.K_w]): #if up or W is pressed, the startkey is True so that the ball launches
                    startkey = True
                if (keys[pygame.K_p]): #this is for the cheat as well as whats below
                    pt1 = True
                if pt1 ==True and (keys[pygame.K_i]): 
                    pt2 = True
                if pt2 == True and (keys[pygame.K_e]): 
                    pt3 = True
                if pt3 == True and (keys[pygame.K_RETURN]) or (keys[pygame.K_KP_ENTER]): 
                    cheat = True

                if event.type == pygame.KEYDOWN:
                    if not keys[pygame.K_p] and not keys[pygame.K_i] and not keys[pygame.K_e]: #if wrong button pressed, it resets so keyboard spamming doesnt enable cheat
                        pt1 = False
                        pt2 = False
                        pt3 = False #this is where cheat stuff ends


            screen.fill((0,0,0)) #gives the screen a black background
            scoretxt = bigfont.render(f"{score:04}", True, (255, 255, 255)) #renders the score text according to the score
            screen.blit(scoretxt, (screen_width//5 - scoretxt.get_width()//2, 10)) #places the text on the screen
            
            wall.draw()  #draws the blocks from the blocks class

            player.draw() #draws the player from the paddle class
            player.move() #checks if player is moving from the paddle class

            x = screen_width//1.4 #this sets a x value for the balls that are drawn at the top signifying lives
            for balls in range(ballsleft): #for however many lives are left, will drwaw that many balls
                pygame.draw.circle(screen, (255, 255, 255), (x, 45), 20)
                x += 60 #adds 60 to x so that balls do not get placed in same location
            
            if presstostart:#this is for before the round starts and it waits for w or up to get pressed (from startkey above)
                temptime = pygame.time.get_ticks() #this time is used to compare against the buffer
                screen.blit(starttxt, (screen_width//2 - starttxt.get_width()//2, screen_height//1.8 - starttxt.get_height()//2))
                if firsttime: #if this is when the game first begins (not each life) will give additional instructions
                    screen.blit(instructions, (screen_width//2 - instructions.get_width()//2, screen_height//1.5 - instructions.get_height()//2))
                if temptime >= buffer: #compares set time to buffer
                    if startkey == True:
                        presstostart = False
                        firsttime = False 
                        ballsleft -= 1 #removes a life when up/W is pressed
                        ball1 = ball(player.rect.x + player.width // 2, player.rect.y - 20) #initalizes the ball from ball class and gives it the players coordinates

            else: #when presstostart is not enabled (aka game started)
                time += clock.get_time() #adds to the time

                ball1.draw() #draws the ball from ball class
                end = ball1.move(player, wall) #it plays out the move part of ball variable and assigns whatever it returns to end variable
                if end == 'win': 
                    running = False #sets running to false so that game loop ends
                    won = True

                if end:
                    if ballsleft == 0: #if no lives left, will set running to false so game loop ends
                        running = False
                        lost = True
                    else: #if still lives left, will reset ball position and enable presstostart 
                        ball1 = ball(player.rect.x + player.width // 2, player.rect.y - 20)
                        presstostart = True
                        buffer = pygame.time.get_ticks() + 700

            timetxt = bigfont.render(f"{time//1000:03}", True, (26, 109, 186)) #sets the time to a txt (have to divide by 1000 to be in seconds, :03 is so it shows 3 positions)
            screen.blit(timetxt, (screen_width//2.5, 10))#adds time txt to screen

            pygame.display.flip() #updates the entire screen to show everythoing that has been added 
            clock.tick(60) #sets the game at 60 fps
            await asyncio.sleep(0) #this is for when uploading to website through pygbag as is everything else that includes async

        if won == True: #configures some text and a button if won (no need to do so if not won)
            wintxtpt3 = smallerfont.render(f"WITH {ballsleft} LIVES LEFT", True, (255,255,255))
            wintxtpt4 = smallerfont.render(f"IN {time//1000:03} SECONDS", True, (255,255,255))
            scoretxt = bigfont.render(f"{score:04}", True, (255, 255, 255))
            againtxt = smallerfont.render("PLAY AGAIN?", True, (255,255,255))
            againbtn = pygame.Rect(screen_width//2 - 300//2, screen_height//2 + 200, 300, 100)

        else: #if lost, configures some text and the button
            againtxt = smallerfont.render("TRY AGAIN?", True, (255,255,255))
            againbtn = pygame.Rect(screen_width//2 - 250//2, screen_height//2 + 200, 250, 100)


        ended = True #loops this ended loop
        while ended:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if againbtn.collidepoint(mouse_pos): #checks if the person clicks the button to play again and ends the loop if so
                            ended = False

            screen.fill((0,0,0))
            screen.blit(timetxt, (screen_width//2.5, 10))
            screen.blit(scoretxt, (screen_width//5 - scoretxt.get_width()//2, 10))
            wall.draw() 
            player.draw()
            x = screen_width//1.45
            for balls in range(ballsleft):
                pygame.draw.circle(screen, (255, 255, 255), (x, 45), 20)
                x += 60
            #places stuff down that was also there previously but since no longer in running loop, need to place it again
            if won: #places down all the text
                screen.blit(wintxt, (screen_width//2-wintxt.get_width()//2, 200)) 
                screen.blit(wintxtpt2, (screen_width//2-wintxtpt2.get_width()//2, 250))
                screen.blit(wintxtpt3, (screen_width//2-wintxtpt3.get_width()//2, 300))
                screen.blit(wintxtpt4, (screen_width//2-wintxtpt4.get_width()//2, 350))
                
            if lost:
                screen.blit(losttxt, (screen_width//2 - losttxt.get_width()//2, 500))
            pygame.draw.rect(screen, (26, 109, 186), againbtn) #draws the rect that houses the play again button
            screen.blit(againtxt, (againbtn.x + againbtn.width//2 - againtxt.get_width()//2, againbtn.y + againbtn.height//2 - againtxt.get_height()//2)) #places again text in center of button
            
            pygame.display.flip() 
            clock.tick(60)
            await asyncio.sleep(0)

asyncio.run(loop()) #runs the code starting from the beginning of loop()