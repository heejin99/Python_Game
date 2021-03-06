import os
import pygame
import random
import sys
#################################################
# 기본 초기화 (반드시 해야하는 것들)

# 화면 크기 설정 (480 x 640)
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
destroy_count = 0
s_num = 3 # 우주선 3대

def startGame():
    global screen, clock, background, character, enemy, weapon

    pygame.init() 

    screen = pygame.display.set_mode((screen_width, screen_height))

    # 화면 타이틀 설정
    pygame.display.set_caption("Hee AirPlane") # 게임 이름

    # FPS
    clock = pygame.time.Clock()
    #################################################

    # 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
    current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
    image_path = os.path.join(current_path, "images") # image 폴더 위치 반환

    # 배경
    background = pygame.image.load(os.path.join(image_path, "background.png"))

    # 캐릭터
    character = pygame.image.load(os.path.join(image_path, "airplane.png"))
    # 무기
    weapon = pygame.image.load(os.path.join(image_path, "weapon.png")) 
    
    # 적
    enemy = pygame.image.load(os.path.join(image_path, "enemy.png"))

# def drawObject(obj, x, y):
#     screen.blit(obj, (x, y))

def explode():
    pygame.display.update()
    pygame.time.delay(2000)
    runGame()

def showScore(count):
    global screen
    font = pygame.font.SysFont('malgungothic', 20)
    text = font.render("점수: "+str(count),True, (0, 0, 255))
    heart = font.render("생명: "+str(s_num), True, (0,0,255))
    screen.blit(text,(0,0))
    screen.blit(heart,(0,20))

def gameOver():
    global screen_height
    font = pygame.font.SysFont('malgungothic', 50)
    if destroy_count == 100:
        msg = font.render("Mission Complete!", True, (0,0,255))
        msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(msg, msg_rect)
    else :
        msg = font.render("Game Over!", True, (255,0,0))
        msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(msg, msg_rect)

    pygame.display.update()
    pygame.time.delay(2000)
    runGame()


def runGame():
    global destroy_count, s_num

    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - character_height

    # 캐릭터 이동 방향
    character_x = 0
    character_y = 0

    # 캐릭터 스피드
    character_speed = 10

    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]

    weapons = []

    enemy_size = enemy.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_x_pos = random.randint(0, screen_width-enemy_width)
    enemy_y_pos = 0
    enemy_speed = 5

    running = True # 게임이 진행 중인가
    while running:
        dt = clock.tick(60) 
    
        # 2. 이벤트 처리 (키보드, 마우스 등)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False 
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    character_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    character_x += character_speed
                elif event.key == pygame.K_UP:
                    character_y -= character_speed
                elif event.key == pygame.K_DOWN:
                    character_y += character_speed
                elif event.key == pygame.K_SPACE:
                    if len(weapons) < 2:
                        weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                        weapon_y_pos = character_y_pos 
                        weapons.append([weapon_x_pos, weapon_y_pos])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    character_y = 0

        # 3. 게임 캐릭터 위치 정의
        
        character_x_pos += character_x
        character_y_pos += character_y
    
        # 가로 경계값 처리
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 세로 경계값 처리
        if character_y_pos < 0:
            character_y_pos = 0
        elif character_y_pos > screen_height - character_height:
            character_y_pos = screen_height - character_height

        # 무기 처리
        if len(weapons) != 0:
            for i, w_y in enumerate(weapons):
                w_y[1] -= 10
                weapons[i][1] = w_y[1]
                if w_y[1] < enemy_y_pos: # 미사일의 y좌표가 운석의 y좌표보다 작은 경우
                    if w_y[0] > enemy_x_pos and w_y[0] < enemy_x_pos + enemy_width: # x 좌표가 겹치면
                        weapons.remove(w_y)# 미사일 제거
                        enemy_x_pos = random.randint(0, screen_width-enemy_width)
                        enemy_y_pos = 0 # 운석 위치 조정
                        destroy_count += 10

            if w_y[1] <= 0: # 미사일이 0의 위치까지 간 경우
                try:
                    weapons.remove(w_y)
                except:
                    pass
        
        enemy_y_pos += enemy_speed
        if enemy_y_pos > screen_height:
            enemy_y_pos = 0
            enemy_x_pos = random.randint(0, screen_width - enemy_width)
        
        # 4. 충돌 처리    
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        enemy_rect= enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

        if character_rect.colliderect(enemy_rect):
            s_num -= 1
            explode()

        if s_num == 0:
            gameOver()

        if destroy_count == 100:
            gameOver()

        # 5. 화면에 그리기
        screen.blit(background, (0,0))
        
        showScore(destroy_count)

        if len(weapons) != 0:
            for w_x, w_y in weapons:
                screen.blit(weapon, (w_x, w_y))

        screen.blit(character, (character_x_pos, character_y_pos))
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
        
        pygame.display.update() # 게임 화면을 다시 그리기(반드시 계속 호출 되어야 함)

startGame()
runGame()

# # pygame 종료
# pygame.quit()