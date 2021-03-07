import pygame
import os
import sys
import random

#################################################
# 기본 초기화 (반드시 해야하는 것들)
# 화면 크기 설정 (480 x 640)
screen_width = 800 # 가로 크기
screen_height = 600 # 세로 크기


def startGame():
    global screen, background, titleimg, selectText, startimg, quitimg, \
        clickstart, clickquit, dogimg, dogimg2, clickdog1, clickdog2, \
            clock, playparms, dog1parms, dog2parms, boneimg, chocolateimg, vacuumimg, score, s_num

    pygame.init() 

    screen = pygame.display.set_mode((screen_width, screen_height))

    # 화면 타이틀 설정
    pygame.display.set_caption("Hee Dog") # 게임 이름

    # FPS
    clock = pygame.time.Clock()
    #################################################

    # 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
    score = 0
    s_num = 3

    current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
    image_path = os.path.join(current_path, "images") # image 폴더 위치 반환

    background = pygame.image.load(os.path.join(image_path, "background.png"))
    titleimg = pygame.image.load(os.path.join(image_path, "titleimg.png"))
    selectText = pygame.image.load(os.path.join(image_path, "selectText.png"))

    startimg = pygame.image.load(os.path.join(image_path, "startimg.png"))
    quitimg = pygame.image.load(os.path.join(image_path, "quitimg.png"))
    clickstart = pygame.image.load(os.path.join(image_path, "clickstart.png"))
    clickquit = pygame.image.load(os.path.join(image_path, "clickquit.png"))

    dogimg = pygame.image.load(os.path.join(image_path, "dogimg.png"))
    dogimg2 = pygame.image.load(os.path.join(image_path, "dogimg2.png"))
    clickdog1 = pygame.image.load(os.path.join(image_path, "clickdog1.png"))
    clickdog2 = pygame.image.load(os.path.join(image_path, "clickdog2.png"))

    playparms= []
    dog1parms = [dogimg, 5, 377, 450, 36, 30, 1.1]
    dog2parms = [dogimg2, 3.5, 380, 450, 30, 25, 1.02]

    boneimg = pygame.image.load(os.path.join(image_path, "bone.png"))
    chocolateimg = pygame.image.load(os.path.join(image_path, "chocolate.png"))
    vacuumimg = pygame.image.load(os.path.join(image_path, "vacuum.png"))

class Player:
    def __init__(self, p_img, speed, dog_x, dog_y, hitbox_x, hitbox_y, upspeed):
        self.p_img = p_img
        self.speed= speed
        self.dog_x = dog_x
        self.dog_y = dog_y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y
        self.upspeed = upspeed

class GObject:
    def __init__(self, oob_img, speed, ob_x, ob_y, hitbox_x, hitbox_y):
        self.oob_img = oob_img
        self.speed = speed
        self.ob_x = ob_x
        self.ob_y = ob_y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y

class Background:
    def __init__(self, bg_img, bg_x, bg_y):
        self.bg_x = bg_x
        self.bg_y = bg_y
        screen.blit(bg_img, (bg_x, bg_y))

class Button:
    def __init__(self, img_idx, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos() # 마우스 좌표저장
        click = pygame.mouse.get_pressed() # 클릭시
        if x + width > mouse[0] > x and y + height > mouse[1] > y: # 이미지 안에 있으면
            screen.blit(img_act, (x_act, y_act)) # 클릭 이미지 로드
            if click[0] and action != None:
                pygame.time.delay(1000)
                action()
        else:
            screen.blit(img_idx, (x,y)) # 마우스가 이미지 바깥이면 기본 이미지

class Button2:
    def __init__(self, img_idx, x, y, width, height, img_act, x_act, y_act, parms, action=None):
        mouse = pygame.mouse.get_pos() # 마우스 좌표저장
        click = pygame.mouse.get_pressed() # 클릭시
        if x + width > mouse[0] > x and y + height > mouse[1] > y: # 이미지 안에 있으면
            screen.blit(img_act, (x_act, y_act)) # 클릭 이미지 로드
            if click[0] and action != None:
                playparms.append(parms[0])
                playparms.append(parms[1])
                playparms.append(parms[2])
                playparms.append(parms[3])
                playparms.append(parms[4])
                playparms.append(parms[5])
                playparms.append(parms[6])
                pygame.time.delay(1000)
                action()
        else:
            screen.blit(img_idx, (x,y)) # 마우스가 이미지 바깥이면 기본 이미지


def quitgame():
    pygame.quit()
    sys.exit()

def startmenu():
    running = True # 게임이 진행 중인가
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False 
                sys.exit()
        Background(background, 0, 0) 
        titleText = screen.blit(titleimg, (200, 200))
        startButton = Button(startimg, 180, 350, 150, 100, clickstart, 180, 350, selectDog)
        quitButton = Button(quitimg, 460, 350, 150, 100, clickquit, 460, 350, quitgame)
    
        pygame.display.update() # 게임 화면을 다시 그리기(반드시 계속 호출 되어야 함)
        clock.tick(15)

def selectDog():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitgame()
        Background(background, 0, 0) 
        screen.blit(selectText, (200, 200))
        dogselect = Button2(dogimg, 280, 350, 40, 150, clickdog1, 280, 350, dog1parms, gameScreen)
        dog2select = Button2(dogimg2, 460, 350, 40, 150, clickdog2, 460, 350, dog2parms, gameScreen)

        pygame.display.update()
        clock.tick(15)

def eatdog(player, obj):
    global score
    if player.dog_y < obj.ob_y + obj.hitbox_y and player.dog_y > obj.ob_y \
            or player.dog_y + player.hitbox_y > obj.ob_y and \
                player.dog_y + player.hitbox_y < obj.ob_y + obj.hitbox_y :
                if player.dog_x > obj.ob_y and player.dog_x < obj.ob_x + obj.hitbox_x \
                    or player.dog_x + player.hitbox_x > obj.ob_x \
                        and player.dog_x + player.hitbox_x < obj.ob_x + obj.hitbox_x:
                        obj.ob_y = -10
                        obj.ob_x = random.randrange(0, screen_width - 25)
                        score += 10

def crash(text) :
    largeText = pygame.font.SysFont("malgungothic", 46)
    Textsurf = largeText.render(text, True, (255,0,0))  
    TextRect= Textsurf.get_rect()
    TextRect.center = ((screen_width / 2), (screen_height/2))
    screen.blit(Textsurf, TextRect)
    pygame.display.update()
    pygame.time.delay(1000)
    gameScreen()

def crushdog(player, obj):
    global s_num
    if player.dog_y < obj.ob_y + obj.hitbox_y and player.dog_y > obj.ob_y \
            or player.dog_y + player.hitbox_y > obj.ob_y and \
                player.dog_y + player.hitbox_y < obj.ob_y + obj.hitbox_y :
                if player.dog_x > obj.ob_y and player.dog_x < obj.ob_x + obj.hitbox_x \
                    or player.dog_x + player.hitbox_x > obj.ob_x \
                        and player.dog_x + player.hitbox_x < obj.ob_x + obj.hitbox_x:
                        obj.ob_y = -10
                        obj.ob_x = random.randrange(0, screen_width - 25)
                        s_num -= 1
                        crash("생명 -1")

def scoreScreen(count):
    global s_num
    font = pygame.font.SysFont("malgungothic", 25)
    text = font.render("점수: "+ str(count), True, (0,255,0))
    heart = font.render("생명: "+ str(s_num), True, (0,255,0))
    screen.blit(text, (20, 20))
    screen.blit(heart, (20, 50))

def gameScreen():
    dog = Player(playparms[0],playparms[1], playparms[2], playparms[3], playparms[4], playparms[5], playparms[6])
    bone = GObject(boneimg, 5, random.randint(0, screen_width-20), -600, 40, 35)
    chocolate1 = GObject(chocolateimg, 3, random.randint(0, screen_width-20), -600, 40, 35)
    chocolate2 = GObject(chocolateimg, 3, random.randint(0, screen_width-20), -1000, 40, 35)
    vacuum = GObject(vacuumimg, 4, random.randint(0, screen_width-20), random.randint(-2000,-1000), 55, 100)
    
    dog_x_change = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog_x_change = dog.speed * -1 + -1 * dog.upspeed
                elif event.key == pygame.K_RIGHT:
                    dog_x_change = dog.speed + dog.upspeed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dog_x_change = 0
        
        dog.dog_x += dog_x_change

        Background(background, 0,0)

        screen.blit(boneimg, (bone.ob_x, bone.ob_y))
        screen.blit(chocolateimg, (chocolate1.ob_x, chocolate1.ob_y))
        screen.blit(chocolateimg, (chocolate2.ob_x, chocolate2.ob_y))
        screen.blit(vacuumimg, (vacuum.ob_x, vacuum.ob_y))
        
        screen.blit(dog.p_img, (dog.dog_x, dog.dog_y))

        # 낙하 속도
        bone.ob_y += bone.speed
        chocolate1.ob_y += chocolate1.speed
        chocolate2.ob_y += chocolate2.speed
        vacuum.ob_y += vacuum.speed
        
        # 가로 경계값 처리
        if dog.dog_x < 0:
            dog.dog_x = 0
        elif dog.dog_x > screen_width - 40:
            dog.dog_x = screen_width - 40

        # 오브젝트 재생성
        if bone.ob_y > screen_height:
            bone.ob_y = -10
            bone.ob_x = random.randint(0, screen_width - 25)
        if chocolate1.ob_y > screen_height:
            chocolate1.ob_y = -10
            chocolate1.ob_x = random.randint(0, screen_width - 25)
        if chocolate2.ob_y > screen_height:
            chocolate2.ob_y = -410
            chocolate2.ob_x = random.randint(0, screen_width - 25)
        if vacuum.ob_y > screen_height:
            vacuum.ob_y = -2000
            vacuum.ob_x = random.randint(0, screen_width - 25)

        # 충돌 처리
        
        eatdog(dog, bone)
        crushdog(dog, chocolate1)
        crushdog(dog, chocolate2)
        crushdog(dog, vacuum)

        scoreScreen(score)

        if s_num == 0:
            crash("Game Over")
        if score == 100:
            crash("Mission Complete")

        pygame.display.update()
        clock.tick(60)

startGame()
startmenu()
selectDog()
gameScreen()

# pygame 종료
# pygame.quit()