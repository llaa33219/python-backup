import pygame, pymunk, pymunk.pygame_util # pip install pygame으로 pygame 설치, pip install pymunk로 pymunk 설치
# 1. 게임 초기화 ( game initialize)
pygame.init()
# 2. 게임창 옵션 설정 ( window option)
size = (900, 900) # 게임창 크기 ( window size)
screen = pygame.display.set_mode(size)
title = "Physics Simulator" # 창 제목 ( window title)
pygame.display.set_caption(title)
# 3. 게임 내 필요한 설정 ( option for game)
clock = pygame.time.Clock() # 시계 ( clock)
# 공간 만들기 ( space)
space = pymunk.Space()
space.gravity = (0, 1000)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# 바닥 만들기 ( floor)
floor = pymunk.Body(body_type = pymunk.Body.STATIC)
floor.position = (0, size[1]-50)
floor_shape = pymunk.Segment(floor, (0,0), (size[0],-100), 1)
floor_shape.elasticity = 1
floor_shape.friction = 0.2
space.add(floor, floor_shape)
# 공 만들기 ( ball)
ball = pymunk.Body(1, 1)
ball.position = (size[0]/1, 50)
ball_shape = pymunk.Circle(ball, 50)
ball_shape.elasticity = 0.5
ball_shape.friction = 0.2
space.add(ball, ball_shape)
# 4. 메인 이벤트 ( main event)
running = True
while running:
    # 4-1. FPS 설정 ( frame per second)
    clock.tick(60) # 메인 이벤트 반복이 1 초에 60회 (60 frames per 1 second)
    space.step(1/60) # 시뮬레이션 주기 ( Simulation cycle)
    # 4-2. 각종 입력 감지 ( event detection)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
    # 4-3. 입력, 시간에 따른 변화 ( change with event or time)
    # 4-4. 그리기 ( drawing)
    screen.fill((0,0,0))
    space.debug_draw(draw_options)
    # 4-5. 업데이트 ( update)
    pygame.display.flip()
# 5. 게임 종료 ( quit)
pygame.quit()
