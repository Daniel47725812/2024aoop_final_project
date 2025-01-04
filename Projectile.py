from dataclasses import dataclass, field
import pygame
from enum import Enum
from typing import List, Optional

class ProjectileType(Enum):
    FIREBALL = "fireball"
    WAVE = "wave"
    BULLET = "bullet"
    
@dataclass
class ProjectileHitboxData:
    x: float      # 相對於投射物的 x 偏移（百分比）
    y: float      # 相對於投射物的 y 偏移（百分比）
    width: float  # 相對於投射物寬度的比例
    height: float # 相對於投射物高度的比例
    
@dataclass
class ProjectileConfig:
    sprite_sheet_path: str
    frames: List[tuple]  # Animation frames
    speed: float
    damage: int
    lifetime: float
    scale: float = 1.0
    animation_speed: float = 0.1
    hitbox: ProjectileHitboxData = field(default_factory=lambda: ProjectileHitboxData(0.2, 0.2, 0.6, 0.6))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, config: ProjectileConfig):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(direction * config.speed, 0)
        self.config = config
        self.lifetime = config.lifetime
        self.direction = direction
        
        # 載入精靈圖
        self.sprite_sheet = pygame.image.load(config.sprite_sheet_path).convert_alpha()
        self.current_frame = 0
        self.animation_timer = 0
        
        # 初始化碰撞箱
        frame = config.frames[0]
        self.base_rect = pygame.Rect(x, y, frame["width"] * config.scale, frame["height"] * config.scale)
        self.hitbox = self._create_hitbox()
    
    def _create_hitbox(self) -> pygame.Rect:
        """創建實際的碰撞箱"""
        hitbox_data = self.config.hitbox
        
        # 計算碰撞箱的實際尺寸和位置
        width = self.base_rect.width * hitbox_data.width
        height = self.base_rect.height * hitbox_data.height
        
        x_offset = self.base_rect.width * hitbox_data.x
        y_offset = self.base_rect.height * hitbox_data.y
        
        x = self.position.x + x_offset
        y = self.position.y + y_offset
        
        if self.direction < 0:  # 如果向左移動，調整 x 位置
            x = self.position.x + self.base_rect.width - (x_offset + width)
            
        return pygame.Rect(x, y, width, height)
    
    def update(self, delta_time: float):
        # 更新位置
        self.position += self.velocity * delta_time
        
        # 更新基礎矩形和碰撞箱位置
        self.base_rect.x = self.position.x
        self.base_rect.y = self.position.y
        self.hitbox = self._create_hitbox()  # 重新計算碰撞箱
        
        # 更新動畫
        self.animation_timer += delta_time
        if self.animation_timer >= self.config.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.config.frames)
        
        # 更新存活時間
        self.lifetime -= delta_time
        
    def check_collision(self, player_hitboxes: List[pygame.Rect]) -> bool:
        """檢查是否與玩家的碰撞箱發生碰撞"""
        for player_hitbox in player_hitboxes:
            if self.hitbox.colliderect(player_hitbox):
                return True
        return False
    
    def draw(self, screen: pygame.Surface):
        # 繪製投射物
        frame = self.config.frames[self.current_frame]
        frame_surface = pygame.Surface((frame["width"], frame["height"]), pygame.SRCALPHA)
        frame_rect = (frame["x"], frame["y"], frame["width"], frame["height"])
        frame_surface.blit(self.sprite_sheet, (0, 0), frame_rect)
        
        if self.direction < 0:  # 如果向左移動，翻轉圖像
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            
        if self.config.scale != 1.0:
            new_size = (int(frame["width"] * self.config.scale), 
                       int(frame["height"] * self.config.scale))
            frame_surface = pygame.transform.scale(frame_surface, new_size)
            
        screen.blit(frame_surface, self.position)
        
    def draw_debug(self, screen: pygame.Surface):
        """繪製碰撞箱（用於調試）"""
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # 紅色表示投射物碰撞箱

    