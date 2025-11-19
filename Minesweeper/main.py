import pygame

pygame.init()

screen_width = 1920
screen_height = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

icon = pygame.image.load("assets/flag.png")
pygame.display.set_icon(icon)

#-------------------------------
#----------- Fonts ------------#
#-------------------------------
roboto =("assets/Roboto.ttf")

menufont = pygame.font.Font(roboto, 48)

#-------------------------------
#---------- Assets ------------#
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




difficulty = ""

if difficulty=="easy":
    grid_length = 9
    grid_height = 9
    num_mines = 10

elif difficulty=="medium":
    grid_length = 16
    grid_height = 16
    num_mines = 40

elif difficulty=="hard":
    grid_length = 22
    grid_height = 22
    num_mines = 99