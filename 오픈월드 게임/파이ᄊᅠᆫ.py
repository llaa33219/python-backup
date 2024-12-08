import pygame
import pymunk
import sys
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Sandbox Game with Physics")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# 블록 크기
BLOCK_SIZE = 40

# 물리 엔진 초기화
space = pymunk.Space()
space.gravity = (0, 900)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (BLOCK_SIZE, BLOCK_SIZE)))
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (BLOCK_SIZE, BLOCK_SIZE))
        self.shape.friction = 1
        space.add(self.body, self.shape)
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.body.apply_impulse_at_local_point((-200, 0))
        elif keys[pygame.K_d]:
            self.body.apply_impulse_at_local_point((200, 0))
        else:
            self.body.velocity = (0, self.body.velocity.y)

        if keys[pygame.K_w] and self.on_ground:
            self.body.apply_impulse_at_local_point((0, -600))

        self.rect.x = self.body.position.x - BLOCK_SIZE // 2
        self.rect.y = self.body.position.y - BLOCK_SIZE // 2

# 블록 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2
        self.shape = pymunk.Poly.create_box(self.body, (BLOCK_SIZE, BLOCK_SIZE))
        self.shape.friction = 1
        space.add(self.body, self.shape)
        self.update_image()

    def update_image(self):
        pygame.draw.rect(self.image, BROWN, (0, 0, BLOCK_SIZE, BLOCK_SIZE))
        # 여기서 더 부드러운 연결을 위해 추가적인 이미지 처리 가능

# 지형 생성 함수
def generate_terrain():
    terrain = pygame.sprite.Group()
    last_height = SCREEN_HEIGHT // 2
    for i in range(0, SCREEN_WIDTH * 5, BLOCK_SIZE):
        height = last_height + random.randint(-BLOCK_SIZE, BLOCK_SIZE)
        height = max(min(height, SCREEN_HEIGHT - BLOCK_SIZE), SCREEN_HEIGHT // 3)
        for j in range(height, SCREEN_HEIGHT, BLOCK_SIZE):
            block = Block(i, j)
            terrain.add(block)
        last_height = height
    return terrain

# 플레이어 생성
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 지형 생성
terrain = generate_terrain()
all_sprites.add(terrain)

# 게임 루프
running = True
camera_x = 0
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = (x + camera_x) // BLOCK_SIZE * BLOCK_SIZE
            y = y // BLOCK_SIZE * BLOCK_SIZE
            block = Block(x, y)
            terrain.add(block)
            all_sprites.add(block)

    # 물리 엔진 스텝
    space.step(1 / 60.0)

    # 화면 업데이트
    all_sprites.update()
    
    # 플레이어가 바닥에 있는지 확인
    player.on_ground = False
    for shape in space.shape_query(player.shape):
        if isinstance(shape.shape, pymunk.Poly) and shape.shape != player.shape:
            player.on_ground = True
            break

    # 카메라 이동
    camera_x = player.rect.x - SCREEN_WIDTH // 2

    # 화면 그리기
    screen.fill(WHITE)

    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
