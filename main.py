import pygame
pygame.init()

winWidth = 288
winHeight = 512

WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Flappy Bird")
YELLOWBIRD = [pygame.image.load("flappy-bird-assets\sprites\yellowbird-downflap.png"),
            pygame.image.load("flappy-bird-assets\sprites\yellowbird-midflap.png"),
            pygame.image.load("flappy-bird-assets\sprites\yellowbird-upflap.png")]

BACKGROUND = pygame.image.load("flappy-bird-assets\sprites\Background-day.png")
BASE = pygame.image.load("flappy-bird-assets\sprites\Base.png")
GAMEOVER = pygame.image.load("flappy-bird-assets\sprites\gameover.png")
MESSAGE = pygame.image.load("flappy-bird-assets\sprites\message.png")
PIPE = pygame.image.load("flappy-bird-assets\sprites\pipe-green.png")

# LOGIC
# if flappy jump is false after initial start, then continue falling, but if true implement the jump


class Bird:
    XPOS = 50  # must be constant
    YPOS = 200
    FLYVEL = 1
    FLYVAL = 30
    DOWNVEL = 0.1
    def __init__(self):
        self.image = YELLOWBIRD[0]
        self.flappyRect = self.image.get_rect()  # getting current coordinates
        self.flappyRect.x = self.XPOS  # current x cor
        self.flappyRect.y = self.YPOS  # current y cor
        self.flappyJump = False

    def update(self, userInput):
        if self.flappyJump:
            self.jump()
        if userInput[pygame.K_SPACE]:
            self.flappyJump = True
            self.jump()
        if self.flappyJump == False:
            self.slideDown()
        else:
            self.flappyJump = False

    def jump(self):
        self.image = YELLOWBIRD[2] 
        self.flappyRect = self.image.get_rect()#gets x and y values
        if self.flappyJump and self.FLYVEL > -0.5:
            self.YPOS -= self.FLYVAL*self.FLYVEL
            self.FLYVEL -= 0.05
        if self.FLYVEL <= -0.3:
            self.FLYVEL = 1.25

    def slideDown(self):
        self.image = pygame.transform.rotate(YELLOWBIRD[1],-30)
        self.YPOS += self.FLYVAL*self.DOWNVEL
        self.DOWNVEL += 0.005

    def draw(self, WIN):
        WIN.blit(self.image, (self.XPOS, self.YPOS))

class Background():
    def __init__(self):
        self.image = BACKGROUND
        self.base = BASE
        self.bg_width = self.image.get_width()
        self.bgX = 0
        self.bgY = 0
        self.base_width = self.image.get_width()
        self.baseX = 0
        self.baseY = 425

    def update(self):
        if(self.bgX <= -self.bg_width):
            self.bgX = 0
            #self.bgX -= self.bg_width
        self.bgX -= 5
    def updateBase(self):
        if(self.baseX <= self.base_width):
            self.baseX = 0
        self.baseX -= 5

    def draw(self,WIN):
        WIN.blit(self.image,(self.bgX,self.bgY))
        WIN.blit(self.image,(self.bgX+self.bg_width,self.bgY))
        WIN.blit(self.base, (self.baseX, self.baseY))
        WIN.blit(self.base, (self.baseX+self.base_width, self.baseY))


def main():
    run = True
    player = Bird()
    clock = pygame.time.Clock()
    bg = Background()
    # pygame.blit(WIN,BACKGROUND)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        WIN.fill((255, 255, 255))

        input = pygame.key.get_pressed()
        bg.update()
        bg.updateBase()
        bg.draw(WIN)
        player.draw(WIN)
        player.update(input)
        pygame.display.update()
        clock.tick(45)


main()
