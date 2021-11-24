import pygame,sys,math,numpy,random

# Intialize the pygame
pygame.init()
clock=pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((800, 700))

# Colors
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)

# Background
# background = pygame.image.load('background.png')

# Making the players
width = 10
height = 80
player1= pygame.Rect((80,400-height/2),(width,height))
player1.center=(50,350)
player1Y_change=0
player2= pygame.Rect((720-width,400-height/2),(width,height))
player2.center=(750,350)
player2Y_change=0

# Making the ball
ball=pygame.Rect((350,400),(30,30))
ball.center=(400,350)
speed=5
vel=[0,0]
serve=True

# Caption and Icon
pygame.display.set_caption("Pong")
icon = pygame.image.load('pong.png')
pygame.display.set_icon(icon)

font = pygame.font.Font('freesansbold.ttf', 100)

# scoreP1=font.render("1", True, white, black)
# scoreP1Rect=scoreP1.get_rect()
# scoreP1Rect.center=(350,50)

scoreP1=0
scoreP1Rect=pygame.Rect(400,50,100,100)
scoreP1Rect.center=(350,50)

scoreP2=0
scoreP2Rect=pygame.Rect(400,50,100,100)
scoreP2Rect.center=(450,50)


def line(start_pos, end_pos):
    pygame.draw.line(screen,white,start_pos,end_pos,2)

def rect(rect,width=0):
    pygame.draw.rect(screen,white,rect,width)

def circle(center,radius):
    pygame.draw.circle(screen,white,center,radius)


def dashedLine(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = 10

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(screen, white, start, end, width=2)

def displayText(text,center):
    temp=font.render(text, True, white, black)
    rect=temp.get_rect()
    rect.center=center
    screen.blit(temp,rect)

def move(player,change):
    player.top+=change
    if player.top<105:
        player.top=105
    elif player.bottom>595:
        player.bottom=595

def launch(speed):
    angle=random.randint(0,360)
    vel=[speed*math.cos(math.radians(angle)),speed*math.sin(math.radians(angle))]
    return vel

def ballCollisons(p1,p2,b):
    if p1.collidepoint(b.midleft) or p2.collidepoint(b.midright):
        return "s"
    elif p1.collidepoint(b.midbottom) or p2.collidepoint(b.midbottom) or p1.collidepoint(b.midtop) or p2.collidepoint(b.midtop) or ball.top<105 or ball.bottom>595:
        return "t" 
    return "n"

prevCol="n"
ticks=60

while True:
    screen.fill(black)
    for event in pygame.event.get():
        # Allowing program to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2Y_change=-5
            elif event.key == pygame.K_DOWN:
                player2Y_change=5
            elif event.key == pygame.K_w:
                player1Y_change=-5
            elif event.key == pygame.K_s:
                player1Y_change=5
            elif event.key==pygame.K_SPACE:
                if serve==True:
                    vel=launch(speed)
                    serve=False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2Y_change = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                player1Y_change = 0

    # Movement for the players
    if player1Y_change!=0:
        move(player1,player1Y_change)
    if player2Y_change!=0:
        move(player2,player2Y_change)

    col=ballCollisons(player1,player2,ball)
    print(ball.center,vel,col,prevCol)
    if col=="s" and prevCol!="s":
        prevCol=col
        vel[0]*=-1
    elif col=="t" and prevCol!="t":
        vel[1]*=-1
        prevCol=col
    elif col=="s1" and prevCol!="s1":
        vel[0]*=-1
        prevCol=col
        # ticks=1
    else:
        prevCol="n"
    ball.centerx+=vel[0]
    ball.centery+=vel[1]

    if ball.right>800:
        serve=True
        ball.center=(400,350)
        vel=[0,0]
        scoreP1+=1
    if ball.left<0:
        scoreP2+=1
        serve=True
        ball.center=(400,350)
        vel=[0,0]

    displayText(str(scoreP1),(350,50))
    displayText(str(scoreP2),(450,50))
    

    rect(scoreP1Rect,1)
    rect(scoreP2Rect,1)
    # Background
    line((400,0),(400,100))
    line((0,600),(800,600))
    line((0,100),(800,100))
    dashedLine((400,100),(400,600))
    rect(player1)
    rect(player2)
    circle(ball.center,15)
    pygame.display.update()
    clock.tick(ticks)