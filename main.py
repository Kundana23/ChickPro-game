import pygame
import random
import math
from pygame import mixer

#initialisation
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#background image
background = pygame.image.load('farm1.png')

#sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#caption and icon
pygame.display.set_caption("ChickPros")
icon = pygame.image.load('chicken.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('water-gun (1).png')
playerX = 100
playerY = 480
playerX_change = 0


#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('fox (1).png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)


#ready - you can't see the bullet on the screen
#fire - the bullet is moving

#bullet
bulletImg = pygame.image.load('balloon.png')
bulletX = 50
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('AlleniaRegular-Free.ttf', 32)

#gameover
over_font = pygame.font.Font('AlleniaRegular-Free.ttf', 64)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score:"+ str(score_value), True, (255, 255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+40,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False










#game loop
running = True
while running:
    #RGB= Red, Green, Blue
    screen.fill((0,0,0))

    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
           running=False

        #to check whether the key pressed is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("balloonsound.wav.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change


    if playerX <= 0:
        playerX =0
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(num_of_enemies):

        #gameover
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
    #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)



      #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"



    if bullet_state =="fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()

