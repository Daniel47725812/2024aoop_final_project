#ifndef __player__
#define __player__
import pygame

# 角色設置
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
PLAYER_SPEED = 5
ATTACK_RANGE = 30

# 添加玩家類別
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

    def update(self
               ):
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 攻擊範圍顯示
        if self.is_attacking:
            attack_rect = pygame.Rect(
                self.rect.right, self.rect.top, ATTACK_RANGE, PLAYER_HEIGHT
            )
            pygame.draw.rect(screen, (255, 200, 200), attack_rect)


#endif