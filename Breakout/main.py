import pygame
import asyncio
from random import uniform

pygame.init()

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

#-------------------------------
#----------- Fonts ------------#
#-------------------------------

blockyfont = ("assets/BoldPixels.ttf")

bigfont = pygame.font.Font(blockyfont, 72)
smallerfont = pygame.font.Font(blockyfont, 46)
evensmallerfont = pygame.font.Font(blockyfont, 36)

starttxt = smallerfont.render("PRESS UP/W KEY TO START", True, (255, 255, 255))
instructions = evensmallerfont.render("USE ARROW KEYS OR A/D TO MOVE", True, (255, 255, 255))

wintxt = smallerfont.render("CONGRATULATIONS!",True, (255,255,255))
wintxtpt2 = smallerfont.render("YOU HAVE WON",True, (255,255,255))

losttxt = smallerfont.render("GAME OVER", True, (255,255,255))

againtxt = smallerfont.render("TRY AGAIN?", True, (255,255,255))


#-------------------------------
#----------- Set Up -----------#
#-------------------------------
yblockcol = (181, 184, 29)
gblockcol = (27, 130, 27)
oblockcol = (189, 116, 32)
rblockcol = (171, 31, 19)

rows = 8
columns = 10
score = 0

cheat = False
once = True

class blocks:
    def __init__ (self):
        self.gap = 5
        self.width = (screen_width - (columns + 1) * self.gap) // columns
        self.height = 30
        self.topgap = 70

    def wall(self):
        self.blocks = []
        single_block = []
        for row in range(rows):
            block_row = []
            for column in range (columns):
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
                
                single_block = [rect, strength]
                block_row.append(single_block)

            self.blocks.append(block_row)

    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 1:
                    colour = yblockcol
                if block[1] == 2:
                    colour = gblockcol
                if block[1] == 3:
                    colour = oblockcol
                if block[1] == 4:
                    colour = rblockcol
                if block[1] >= 1:
                    pygame.draw.rect(screen, colour, block[0])

class paddle:
    def __init__ (self):
        self.width = (screen_width // columns) * 2
        self.height =20
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 50
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, (26, 109, 186), self.rect)


class ball:
    def __init__ (self, x, y):
        self.radius = 10
        self.x = x - self.radius
        self.y = y - self.radius
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.speed_x = uniform(-5, 5)
        while self.speed_x in range(-2,2):
            self.speed_x = uniform(-5, 5)
        self.speed_y = -5
        self.maxspeed = 15
        self.minspeed = -15
        

    def move(self, player, wall):
        global score, once
        
        if cheat==True and once == True:
            self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
            once = False

        collision_threshold = 13
        self.lose = False
        #block walls collisions
        destroyed = True
        rowcount = 0
        for row in wall.blocks:
            blockcount = 0
            for block in row:
                if self.rect.colliderect(block[0]):
                    if cheat ==False:
                        if abs(self.rect.bottom - block[0].top) < collision_threshold and self.speed_y > 0: #from above
                            self.speed_y *= -1
                        if abs(self.rect.top - block[0].bottom) < collision_threshold and self.speed_y < 0: #from below
                            self.speed_y *= -1
                        if abs(self.rect.right - block[0].left) < collision_threshold and self.speed_x > 0: #from left
                            self.speed_x *= -1
                        if abs(self.rect.left - block[0].right) < collision_threshold and self.speed_x < 0: #from right
                            self.speed_x *= -1
                    if cheat ==True:
                        wall.blocks[rowcount][blockcount][1] -= 4
                    if wall.blocks[rowcount][blockcount][1] > 1:
                        wall.blocks[rowcount][blockcount][1] -= 1
                    else:
                        wall.blocks[rowcount][blockcount][1] = 0
                        wall.blocks[rowcount][blockcount][0] = (0,0,0,0) # deletes the block
                    score += 50
                print (wall.blocks[rowcount][blockcount][1])
                if wall.blocks[rowcount][blockcount][1] > 0:
                    destroyed = False
                blockcount += 1
            rowcount += 1
        if destroyed:
            self.win = True
            return 'win'
        #border collisions
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.bottom >= screen_height and cheat == False:
            self.lose = True
        if self.rect.bottom >= screen_height and cheat == True:
            self.speed_y *= -1
            
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #player collisions
        if self.rect.colliderect(player.rect):
            if abs(self.rect.bottom - player.rect.top) < collision_threshold and self.speed_y > 0: #this is if moving down from above paddle
                self.speed_y *= -1
                self.speed_x += player.direction
                if self.speed_x > self.maxspeed and cheat==False:
                    self.speed_x = self.maxspeed
                elif self.speed_x < self.minspeed and cheat ==False: #if going left
                    self.speed_x = self.minspeed
            else:
                self.speed_x *= -1
            self.speed_y *= 1.01
            if self.speed_y < -12 and cheat ==False:
                self.speed_y = -12
            self.speed_x *= 1.05
            if cheat == True:
                self.speed_y = 20
                self.speed_x = 20
        return self.lose

    def draw(self):
        if cheat == True:
            self.radius = 50
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
        

#-------------------------------
#------------ Game ------------#
#-------------------------------
async def loop():
    while True:
        global score, cheat, once
        running = True
        presstostart = True
        firsttime = True
        cheat = False
        once = True
        score = 0
        ballsleft = 3
        buffer = pygame.time.get_ticks() + 700
        time = 0
        pt1=False
        pt2=False
        pt3=False
        wall = blocks()
        wall.wall()
        player = paddle()

        while running:
            startkey = False
            won = False
            lost = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_UP] or keys[pygame.K_w]):
                    startkey = True
                if (keys[pygame.K_p]):
                    pt1 = True
                if pt1 ==True and (keys[pygame.K_i]):
                    pt2 = True
                if pt2 == True and (keys[pygame.K_e]):
                    pt3 = True
                if pt3 == True and (keys[pygame.K_RETURN]):
                    cheat = True

                if event.type == pygame.KEYDOWN:
                    if not keys[pygame.K_p] and not keys[pygame.K_i] and not keys[pygame.K_e]:
                        pt1 = False
                        pt2 = False
                        pt3 = False


            screen.fill((0,0,0))
            scoretxt = bigfont.render(f"{score:04}", True, (255, 255, 255))
            screen.blit(scoretxt, (screen_width//5 - scoretxt.get_width()//2, 10))
            
            wall.draw() 

            player.draw()
            player.move()
            x = screen_width//1.4
            for balls in range(ballsleft):
                pygame.draw.circle(screen, (255, 255, 255), (x, 45), 20)
                x += 60
            
            if presstostart:
                temptime = pygame.time.get_ticks()
                screen.blit(starttxt, (screen_width//2 - starttxt.get_width()//2, screen_height//1.8 - starttxt.get_height()//2))
                if firsttime:
                    screen.blit(instructions, (screen_width//2 - instructions.get_width()//2, screen_height//1.5 - instructions.get_height()//2))
                if temptime >= buffer:
                    if startkey == True:
                        presstostart = False
                        firsttime = False
                        ballsleft -= 1
                        ball1 = ball(player.rect.x + player.width // 2, player.rect.y - 20)

            else:
                time += clock.get_time()

                ball1.draw()
                end = ball1.move(player, wall)
                if end == 'win':
                    running = False
                    won = True

                if end:
                    if ballsleft == 0:
                        running = False
                        lost = True
                    else:
                        ball1 = ball(player.rect.x + player.width // 2, player.rect.y - 20)
                        presstostart = True
                        buffer = pygame.time.get_ticks() + 700

            timetxt = bigfont.render(f"{time//1000:03}", True, (26, 109, 186))
            screen.blit(timetxt, (screen_width//2.5, 10))

            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

        if won == True:
            wintxtpt3 = smallerfont.render(f"WITH {ballsleft} LIVES LEFT", True, (255,255,255))
            wintxtpt4 = smallerfont.render(f"IN {time//1000:03} SECONDS", True, (255,255,255))
            scoretxt = bigfont.render(f"{score:04}", True, (255, 255, 255))
            againtxt = smallerfont.render("PLAY AGAIN?", True, (255,255,255))
            againbtn = pygame.Rect(screen_width//2 - 300//2, screen_height//2 + 200, 300, 100)

        else:
            againtxt = smallerfont.render("TRY AGAIN?", True, (255,255,255))
            againbtn = pygame.Rect(screen_width//2 - 250//2, screen_height//2 + 200, 250, 100)


        ended = True
        while ended:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if againbtn.collidepoint(mouse_pos):
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

            if won:
                screen.blit(wintxt, (screen_width//2-wintxt.get_width()//2, 200))
                screen.blit(wintxtpt2, (screen_width//2-wintxtpt2.get_width()//2, 250))
                screen.blit(wintxtpt3, (screen_width//2-wintxtpt3.get_width()//2, 300))
                screen.blit(wintxtpt4, (screen_width//2-wintxtpt4.get_width()//2, 350))
                
            if lost:
                screen.blit(losttxt, (screen_width//2 - losttxt.get_width()//2, 500))
            pygame.draw.rect(screen, (26, 109, 186), againbtn)
            screen.blit(againtxt, (againbtn.x + againbtn.width//2 - againtxt.get_width()//2, againbtn.y + againbtn.height//2 - againtxt.get_height()//2))
            
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

asyncio.run(loop())