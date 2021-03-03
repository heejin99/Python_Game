import pygame
import random
#################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init() 

# 화면 크기 설정 (480 x 640)
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Hee DDONG Game") # 게임 이름

# FPS
clock = pygame.time.Clock()
#################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
# 배경 만들기
background = pygame.image.load("C:\\Users\\wkdgm\\OneDrive\\Documents\\Python_Game\\pygame_ddong\\background.png")

# 캐릭터 만들기
character = pygame.image.load("C:\\Users\\wkdgm\\OneDrive\\Documents\\Python_Game\\pygame_ddong\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height 

# 이동 위치
to_x = 0
character_speed = 10

# 똥 만들기 (적군)
ddong = pygame.image.load("C:\\Users\\wkdgm\\OneDrive\\Documents\\Python_Game\\pygame_ddong\\enemy.png")
ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]
ddong_height = ddong_size[1]
ddong_x_pos = random.randint(0, screen_width - ddong_width)
ddong_y_pos = 0
ddong_speed = 10


# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 10
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지 
game_result = "Game Over"

running = True # 게임이 진행 중인가
while running:
    dt = clock.tick(30) 
   
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    ddong_y_pos += ddong_speed # 똥이 떨어짐

    if ddong_y_pos > screen_height:
        ddong_y_pos = 0
        ddong_x_pos = random.randint(0, screen_width - ddong_width)
        
    # 4. 충돌 처리    
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    ddong_rect= ddong.get_rect()
    ddong_rect.left = ddong_x_pos
    ddong_rect.top = ddong_y_pos

    if character_rect.colliderect(ddong_rect):
        game_result = "Game Over"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(ddong, (ddong_x_pos, ddong_y_pos))

     # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10, 10))

    # 시간 초과 했다면
    if total_time-elapsed_time <= 0:
        game_result = "Mission Complete"
        running = False
    
    pygame.display.update() # 게임 화면을 다시 그리기(반드시 계속 호출 되어야 함)

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0))  # 노란색
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2초 대기
pygame.time.delay(2000)

# pygame 종료
pygame.quit()