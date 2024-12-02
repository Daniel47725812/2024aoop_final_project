import pygame

# 初始化 Pygame
pygame.init()

# 窗口設置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame 格鬥遊戲")

# 顏色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 角色設置
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
PLAYER_SPEED = 5
ATTACK_RANGE = 30

# 時鐘設置
clock = pygame.time.Clock()
FPS = 60

# 玩家類
class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.is_attacking = False
        self.attack_timer = 0

    def move(self, keys, left, right, up, down):
        if keys[left]:
            self.rect.x -= PLAYER_SPEED
        if keys[right]:
            self.rect.x += PLAYER_SPEED
        if keys[up]:
            self.rect.y -= PLAYER_SPEED
        if keys[down]:
            self.rect.y += PLAYER_SPEED

    def attack(self):
        self.is_attacking = True
        self.attack_timer = 10  # 攻擊持續幀數

    def update(self):
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # 攻擊範圍顯示
        if self.is_attacking:
            attack_rect = pygame.Rect(
                self.rect.right, self.rect.top, ATTACK_RANGE, PLAYER_HEIGHT
            )
            pygame.draw.rect(screen, (255, 200, 200), attack_rect)

# 創建玩家
player1 = Player(100, HEIGHT - PLAYER_HEIGHT - 50, RED)
player2 = Player(WIDTH - 150, HEIGHT - PLAYER_HEIGHT - 50, BLUE)

# 主遊戲循環
running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    # 玩家 1 控制（WASD 和 F 攻擊）
    player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
    if keys[pygame.K_f]:
        player1.attack()

    # 玩家 2 控制（方向鍵 和 K 攻擊）
    player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
    if keys[pygame.K_k]:
        player2.attack()

    # 更新玩家狀態
    player1.update()
    player2.update()

    # 碰撞檢測
    if player1.is_attacking and player1.rect.colliderect(player2.rect):
        print("Player 1 hits Player 2!")
    if player2.is_attacking and player2.rect.colliderect(player1.rect):
        print("Player 2 hits Player 1!")

    # 繪製玩家
    player1.draw()
    player2.draw()

    # 更新畫面
    pygame.display.flip()

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制遊戲幀率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
