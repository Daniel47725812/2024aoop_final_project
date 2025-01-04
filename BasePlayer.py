import pygame
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from Projectile import Projectile, ProjectileConfig, ProjectileType

class FighterState(Enum):
    IDLE = "idle"
    WALKING = "walk"
    JUMPING = "jump"
    ATTACKING = "attack"
    DASH = "dash"
    BLOCKING = "block"
    SHOOT = "shoot"
    
@dataclass
class HitboxData:
    x: float  # 相對於角色基準點的 x 偏移（百分比）
    y: float  # 相對於角色基準點的 y 偏移（百分比）
    width: float  # 相對於基礎寬度的比例
    height: float  # 相對於基礎高度的比例
    is_attack_box: bool = False  # 是否為攻擊判定區域
    
@dataclass
class FrameData:
    x: int
    y: int
    width: int
    height: int
    offset_x: float = 0  # 繪製偏移量
    offset_y: float = 0
    
@dataclass
class AnimationConfig:
    frames: List[FrameData]  # 改用 FrameData 而不是 tuple
    speed: float
    loop: bool = True
    next_state: Optional[FighterState] = None
    hitboxes: List[HitboxData] = None

@dataclass
class CharacterConfig:
    sprite_sheet_path: str
    base_width: int
    base_height: int
    scale: float = 1.0
    default_hitbox: HitboxData = field(default_factory=lambda: HitboxData(0.2, 0.1, 0.6, 0.8, False))
    
    # 基本屬性
    health: int = 100
    attack_power: int = 10
    defense: int = 5
    speed: float = 5.0
    jump_power: float = -400.0
    
    # 動畫配置
    animations: Dict[FighterState, AnimationConfig] = None
    cooldowns: Dict[str, float] = None
    
@dataclass
class HitboxData:
    x: float  # 相對於角色基準點的 x 偏移（百分比）
    y: float  # 相對於角色基準點的 y 偏移（百分比）
    width: float  # 相對於基礎寬度的比例
    height: float  # 相對於基礎高度的比例
    is_attack_box: bool = False  # 是否為攻擊判定區域
    
class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, config: CharacterConfig):
        super().__init__()
        self.config = config
        self.projectiles: List[Projectile] = []
        self.projectile_configs: Dict[ProjectileType, ProjectileConfig] = {}
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.facing_right = True
        self.attack_key_held = False
        self.dash_key_held = False
        
        # 載入精靈圖和設置初始狀態
        self.sprite_sheet = pygame.image.load(config.sprite_sheet_path).convert_alpha()
        self.state = FighterState.IDLE
        self.prev_state = None
        
        # 動畫控制
        self.current_frame_index = 0
        self.animation_timer = 0
        
        # 戰鬥屬性
        self.health = config.health
        self.attack_power = config.attack_power
        self.defense = config.defense
        self.speed = config.speed
        self.jump_power = config.jump_power
        
        # 狀態標誌
        self.on_ground = False
        self.is_attacking = False
        self.is_blocking = False
        self.hit = False
        self.default_cooldown = self.config.cooldowns.copy()
        
        # 碰撞箱設置
        self.scaled_w = config.base_width * config.scale
        self.scaled_h = config.base_height * config.scale
        self.base_rect = pygame.Rect(x, y, self.scaled_w, self.scaled_h)
        
        self.hitboxes: List[pygame.Rect] = []
        self.attack_boxes: List[pygame.Rect] = []
        # 特殊技能
        self.input_buffer = []
        self.input_timer = 0
        
    def _get_current_animation(self) -> AnimationConfig:
        return self.config.animations[self.state]
    
    def _update_animation(self, delta_time: float):
        animation = self._get_current_animation()
        self.animation_timer += delta_time

        if self.animation_timer >= animation.speed:
            self.animation_timer = 0
            if self.current_frame_index < len(animation.frames) - 1:
                self.current_frame_index += 1
            else:
                if self.state == FighterState.ATTACKING or self.state == FighterState.SHOOT:
                    self.hit = False
                if animation.loop:
                    self.current_frame_index = 0
                elif animation.next_state:
                    self.change_state(animation.next_state)
                else:
                    self.change_state(FighterState.IDLE)

    def _get_current_frame(self) -> pygame.Surface:
        animation = self._get_current_animation()
        frame_data = animation.frames[self.current_frame_index]
        
        # 創建基礎幀
        frame = pygame.Surface((frame_data["width"], frame_data["height"]), 
                             pygame.SRCALPHA)
        frame.blit(self.sprite_sheet, 
                  (0, 0), 
                  (frame_data["x"], frame_data["y"], frame_data["width"], frame_data["height"]))
        
        # 縮放
        if self.config.scale != 1.0:
            new_size = (int(frame_data["width"] * self.config.scale),
                       int(frame_data["height"] * self.config.scale))
            frame = pygame.transform.scale(frame, new_size)
        
        # 翻轉
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        return frame, (frame_data["offset_x"], frame_data["offset_y"]) 
    
    def change_state(self, new_state: FighterState):
        if self.state != new_state:
            if self.state == FighterState.ATTACKING:
                self.is_attacking = False  # 离开攻击状态时重置标志
            self.prev_state = self.state
            self.state = new_state
            self.current_frame_index = 0
            self.animation_timer = 0
    
    def update(self, delta_time: float):
        self._handle_physics(delta_time)
        self._update_animation(delta_time)
        self._update_hitboxes()
        for state, cooldown in self.config.cooldowns.items():
            if cooldown > 0:
                self.config.cooldowns[state] -= delta_time
        for projectile in self.projectiles[:]:
            projectile.update(delta_time)
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)
    
    def _handle_physics(self, delta_time: float):
        if not self.on_ground:
            self.velocity.y += 15  # 重力
        
        self.position += self.velocity * delta_time
        
        # 基本地面碰撞
        if self.position.y > 580 - self.scaled_h:  # 這裡應該由遊戲系統提供真實的地面高度
            self.position.y = 580 - self.scaled_h
            self.velocity.y = 0
            self.on_ground = True
        if self.position.x < 0 and self.velocity.x < 0:
            self.velocity.x = 0
            return
        elif self.position.x > 1200 - self.scaled_w and self.velocity.x > 0:
            self.velocity.x = 0
            return
        
    def _create_hitbox_from_data(self, hitbox_data: HitboxData) -> pygame.Rect:
        # 計算實際的碰撞箱位置和大小
        x_offset = self.base_rect.width * hitbox_data.x
        y_offset = self.base_rect.height * hitbox_data.y
        width = self.base_rect.width * hitbox_data.width
        height = self.base_rect.height * hitbox_data.height
        
        x = self.position.x + x_offset
        y = self.position.y + y_offset
        
        if not self.facing_right:
            # 如果角色面向左邊，需要調整碰撞箱的 x 位置
            x = self.position.x + self.base_rect.width - (x_offset + width)
        
        return pygame.Rect(x, y, width, height)
    
    def _update_hitboxes(self):
        # 清空當前的碰撞箱列表
        self.hitboxes.clear()
        self.attack_boxes.clear()
        
        # 獲取當前幀的數據
        animation = self._get_current_animation()
        frame_data = animation.frames[self.current_frame_index]
        
        # 更新基礎矩形位置
        self.base_rect.x = self.position.x
        self.base_rect.y = self.position.y
        
        # 如果當前幀有特定的碰撞箱配置
        if self.config.animations[self.state].hitboxes and not self.hit:
            for hitbox_data in self.config.animations[self.state].hitboxes:
                # 計算碰撞箱實際位置和大小
                hitbox_rect = self._create_hitbox_from_data(hitbox_data)
                
                if hitbox_data.is_attack_box:
                    self.attack_boxes.append(hitbox_rect)
                else:
                    self.hitboxes.append(hitbox_rect)
        else:
            default_hitbox = self._create_hitbox_from_data(self.config.default_hitbox)
            self.hitboxes.append(default_hitbox)
    
    
    def move(self, direction: float):
        if not self.is_attacking and not self.is_blocking:
            self.velocity.x = direction * self.speed
            self.facing_right = direction > 0
            self.change_state(FighterState.WALKING)
    
    def jump(self):
        if self.on_ground and not self.is_attacking:
            self.velocity.y = self.jump_power
            self.on_ground = False
            self.change_state(FighterState.JUMPING)
    
    def attack(self, direction: float):
        if self.config.cooldowns["ATTACK"] > 0:
            return
        if not self.is_attacking and not self.is_blocking:
            self.config.cooldowns["ATTACK"] = self.default_cooldown["ATTACK"]
            self.attack_key_held = True
            if self.facing_right:
                self.move(direction)
            elif not self.facing_right:
                self.move(-direction)
            self.is_attacking = True
            self.attack_key_held = True
            self.change_state(FighterState.ATTACKING)
        
    def _shoot(self, projectile_type: ProjectileType):
        """發射投射物"""
        if self.config.cooldowns["SHOOT"] > 0:
            return
        self.change_state(FighterState.SHOOT)
        if projectile_type in self.projectile_configs:
            self.config.cooldowns["SHOOT"] = self.default_cooldown["SHOOT"]
            config = self.projectile_configs[projectile_type]
            direction = 1 if self.facing_right else -1
            
            # 從角色位置發射
            projectile = Projectile(
                x=self.position.x + (self.base_rect.width if self.facing_right else 0),
                y=self.position.y,
                direction=direction,
                config=config
            )
            self.projectiles.append(projectile)
                 
    def dash(self, direction: float):
        if self.config.cooldowns["DASH"] > 0:
            return
        if not self.is_attacking and not self.is_blocking:
            self.config.cooldowns["DASH"] = self.default_cooldown["DASH"]
            self.dash_key_held = True
            if self.facing_right:
                self.move(direction)
            elif not self.facing_right:
                self.move(-direction)
            self.change_state(FighterState.DASH)
            
    
    def block(self):
        if not self.is_attacking:
            self.is_blocking = True
            self.change_state(FighterState.BLOCKING)
    
    def check_collision(self, other: 'BasePlayer') -> bool:
        # 檢查我方碰撞箱與對方攻擊箱的碰撞
        if self.is_blocking:
            return False  # 如果正在格擋，忽略碰撞
        
        for my_hitbox in self.hitboxes:
            if len(other.attack_boxes) > 0:
                for other_attack_box in other.attack_boxes:
                    if my_hitbox.colliderect(other_attack_box):
                        other.hit = True
                        return True
        return False

    def draw_debug(self, screen: pygame.Surface):
        # 用於調試的繪製方法，顯示碰撞箱
        for hitbox in self.hitboxes:
            pygame.draw.rect(screen, (0, 255, 0), hitbox, 1)  # 綠色表示普通碰撞箱
        
        for attack_box in self.attack_boxes:
            pygame.draw.rect(screen, (255, 0, 0), attack_box, 1)  # 紅色表示攻擊判定
            
    def draw(self, screen: pygame.Surface):
        current_frame, (offset_x, offset_y) = self._get_current_frame()
        # 考慮偏移量進行繪製
        if not self.facing_right:
            offset_x = -offset_x
        draw_pos = (self.position.x + offset_x * self.config.scale,
                   self.position.y + offset_y * self.config.scale)
        screen.blit(current_frame, draw_pos)
        for projectile in self.projectiles:
            projectile.draw(screen)
            projectile.draw_debug(screen)
        