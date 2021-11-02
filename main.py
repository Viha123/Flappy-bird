import pygame
import random
import loadImages
pygame.init()

winWidth = 288
winHeight = 515

WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Flappy Bird")
ICON = pygame.image.load("flappy-bird-assets\Favicon.ico")
pygame.display.set_icon(ICON)
global score
# LOGIC
# if flappy jump is false after initial start, then continue falling, but if true implement the jump

font = pygame.font.Font("freesansbold.ttf", 20)
class Bird:
    XPOS = 50
    YPOS = 200
    FLYVEL = 0.8
    FLYVAL = 30
    DOWNVEL = 0.1
    def __init__(self):
        self.image = loadImages.YELLOWBIRD[0]
        self.flappyJump = False
        self.imageRect = self.image.get_rect()  
        self.imageWidth = self.image.get_width()
        self.imageRect.x = self.XPOS
        self.imageRect.y = self.YPOS

    def update(self, userInput):
        self.pressed = False
        self.imageRect = self.image.get_rect()
        if userInput[pygame.K_SPACE] and not self.pressed:
            self.flappyJump = True
            self.jump()
            self.pressed = True

        if self.flappyJump == False:
            self.pressed = False
            self.slideDown()
        else:
            self.flappyJump = False

    def jump(self):
        self.imageRect = self.image.get_rect()
        self.image = loadImages.YELLOWBIRD[2] 
        self.YPOS -= self.FLYVAL*self.FLYVEL
        self.FLYVAL -= 10
        if self.FLYVAL < -20:
            self.FLYVAL = 35
        
    def slideDown(self):
        self.FLYVAL = 35
        self.imageRect = self.image.get_rect()
        self.image = pygame.transform.rotate(loadImages.YELLOWBIRD[1],-30)
        self.YPOS += self.FLYVAL*self.DOWNVEL
        self.DOWNVEL += 0.001
        if self.YPOS >= 415:
            self.YPOS = 425

    def draw(self, WIN):
        self.imageRect = self.image.get_rect()
        WIN.blit(self.image, (self.XPOS, self.YPOS))

class Base:
    def __init__(self):
        self.base = loadImages.BASE
        self.base_width = self.base.get_width()
        self.baseX = 0
        self.baseY = 425
        self.baseRect = self.base.get_rect()

    def updateBase(self):
        self.baseX -= 5
        if(self.baseX <= -self.base_width):
            self.baseX = 0
            self.baseX -= 5
    def draw(self,WIN):
        WIN.blit(self.base, (self.baseX, self.baseY))
        WIN.blit(self.base, (self.baseX+self.base_width, self.baseY))

class Background:
    def __init__(self):
        self.image = loadImages.BACKGROUND
        self.bg_width = self.image.get_width()
        self.bgX = 0
        self.bgY = 0

    def draw(self, WIN):
        WIN.blit(self.image, (self.bgX, self.bgY))
        WIN.blit(self.image, (self.bgX+self.bg_width, self.bgY))


class Pipe():
    #2 pipes max at a time. as soon as the second pipe leaves another can come
    def __init__(self):
        self.imageDown = loadImages.PIPE
        self.imageUp = pygame.transform.rotate(loadImages.PIPE,180)
        self.imageWidth = self.imageDown.get_width()
        self.imageDownRect= self.imageDown.get_rect()
        self.imageUpRect = self.imageUp.get_rect()
        self.pipeX = 220 #both x values always the same
        self.downPipeMaxY = 400 #down is the down pipe and up is the up pipe
        self.downPipeMinY = 180
        self.newRand()
        

        
    def newRand(self):
        self.imageDownRect = self.imageDown.get_rect()
        self.imageUpRect = self.imageUp.get_rect()
        self.pipeYDown = random.randrange(
            self.downPipeMinY, self.downPipeMaxY)  # 250,420
        self.gap = 430
        self.pipeYUp = self.pipeYDown - self.gap

    def update(self):
        self.imageDownRect = self.imageDown.get_rect()
        self.imageUpRect = self.imageUp.get_rect()
        self.pipeX -= 5
        if self.pipeX <= -self.imageWidth:
            self.pipeX = 300
            self.newRand()
        
    def draw(self,WIN):
        self.imageDownRect = self.imageDown.get_rect()
        self.imageUpRect = self.imageUp.get_rect()
        WIN.blit(self.imageDown, (self.pipeX,self.pipeYDown))  # self.pipeYDown
        WIN.blit(self.imageUp, (self.pipeX,self.pipeYUp)) #self.pipeYUp

player = Bird()
clock = pygame.time.Clock()
bg = Background()
ground = Base()
obs1 = Pipe()
deathCount = 0
def checkAbove():
    if ((player.YPOS < (obs1.pipeYUp+320)) and (player.XPOS > obs1.pipeX) and (player.XPOS < (obs1.pipeX + obs1.imageWidth))):
        return True
    else:
        return False
def checkBelow():
    if ((player.YPOS > (obs1.pipeYDown)) and (player.XPOS > obs1.pipeX) and (player.XPOS < (obs1.pipeX + obs1.imageWidth))):
        return True
    else:
        return False
def deathMessage(deathCount,score):
    run = True
    while run: 
        if deathCount == 1:
            text = font.render("Press any key to restart", True, (0,0,0))
            text2 = font.render("Your score was" + str(score),True,(0,0,0))
            textRect=text.get_rect()
            WIN.blit(text, (winWidth/4,winHeight/2))
            WIN.blit(text2, (winWidth/4, winHeight/2 + 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    deathCount = 0
                    score = 0
                    main()
                if event.type == pygame.QUIT:
                    pygame.quit()
            
        if deathCount == 0:
            WIN.fill((255,255,255))
            text = font.render("Press any key to start", True, (0,0,0))
            textRect = text.get_rect()
            WIN.blit(text, textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run = False
                    main()
                if event.type == pygame.QUIT:
                    pygame.quit()

def scorePrint(score):
    #its fine I'll just blit numbers onto the screen
    font = pygame.font.Font("freesansbold.ttf", 30)
    text = font.render(str(score), True, (0,0,0))
    textRect = text.get_rect()
    
    WIN.blit(text, (winWidth/2 - (textRect.x), 30) )
    pygame.display.update()
    return score

def main():
    score = 0
    scorePrint(score)
    run = True
    obs1.pipeX = 220
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        WIN.fill((255, 255, 255))
        input = pygame.key.get_pressed()
        bg.draw(WIN) #very background 
        ground.updateBase()
        obs1.update()
        obs1.draw(WIN)
        ground.draw(WIN)
        player.draw(WIN)
        player.update(input)
        if(checkAbove() or checkBelow()): #collision detection
            deathMessage(1,score)
        if(player.XPOS > obs1.pipeX and player.XPOS < obs1.pipeX + 10 ): #score increases when player has crossed 5 px after the pipe
            score += 1
            
        scorePrint(score)
        pygame.display.update()
        clock.tick(20)
WIN.fill((255, 255, 255))
deathMessage(0,score = 0)
main()
