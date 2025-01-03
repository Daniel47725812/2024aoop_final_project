from dataclasses import dataclass
import pygame
from enum import Enum
from typing import List, Optional

class ProjectileType(Enum):
    FIREBALL = "fireball"
    WAVE = "wave"
    BULLET = "bullet"

@dataclass
class ProjectileConfig:
    sprite_sheet_path: str
    frames: List[tuple]  # Animation frames
    speed: float
    damage: int
    lifetime: float  # 持續時間(秒)
    scale: float = 1.0
    animation_speed: float = 0.1

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, config: ProjectileConfig):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(direction * config.speed, 0)
        self.config = config
        self.lifetime = config.lifetime
        
        # 載入精靈圖
        self.sprite_sheet = pygame.image.load(config.sprite_sheet_path).convert_alpha()
        self.current_frame = 0
        self.animation_timer = 0
        
        # 初始化碰撞箱
        frame = config.frames[0]
        self.rect = pygame.Rect(x, y, frame[2] * config.scale, frame[3] * config.scale)
        
    def update(self, delta_time: float):
        # 更新位置
        self.position += self.velocity * delta_time
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        # 更新動畫
        self.animation_timer += delta_time
        if self.animation_timer >= self.config.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.config.frames)
        
        # 更新存活時間
        self.lifetime -= delta_time
        
    def draw(self, screen: pygame.Surface):
        frame = self.config.frames[self.current_frame]
        frame_surface = pygame.Surface((frame[2], frame[3]), pygame.SRCALPHA)
        frame_surface.blit(self.sprite_sheet, (0, 0), frame)
        
        if self.velocity.x < 0:  # 如果向左移動，翻轉圖像
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            
        if self.config.scale != 1.0:
            new_size = (frame[2] * self.config.scale, frame[3] * self.config.scale)
            frame_surface = pygame.transform.scale(frame_surface, new_size)
            
        screen.blit(frame_surface, self.position)