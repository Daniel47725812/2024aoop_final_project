import pygame
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from Projectile import Projectile, ProjectileConfig, ProjectileType

class FighterState(Enum):
    IDLE = "idle"
    WALKING = "walk"
    JUMPING = "jump"
    CROUCHING = "crouch"
    ATTACKING = "attack"
    DASH = "dash"
    HURT = "hurt"
    BLOCKING = "block"
    SPECIAL = "special"

@dataclass
class AnimationConfig:
    frames: List[Tuple[int, int, int, int]]  # x, y, width, height
    speed: float
    loop: bool = True
    next_state: Optional[FighterState] = None  # 動畫結束後的下一個狀態

@dataclass
class CharacterConfig:
    sprite_sheet_path: str
    sprite_width: int
    sprite_height: int
    scale: float = 1.0
    hit_box_scale: Tuple[float, float] = (0.6, 0.8)  # 碰撞箱相對大小
    
    # 基本屬性
    health: int = 100
    attack_power: int = 10
    defense: int = 5
    speed: float = 5.0
    jump_power: float = -300.0
    
    # 動畫配置
    animations: Dict[FighterState, AnimationConfig] = None
    
    # 特殊技能配置
    special_moves: Dict[str, List[str]] = None  # 招式指令表

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
        
        # 碰撞箱設置
        self.scaled_w = config.sprite_width * config.scale
        self.scaled_h = config.sprite_height * config.scale
        self.rect = pygame.Rect(x, y, self.scaled_w, self.scaled_h)
        self.hitbox = pygame.Rect(x, y, 
                                self.scaled_w * config.hit_box_scale[0],
                                self.scaled_h * config.hit_box_scale[1])
        
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
                if animation.loop:
                    self.current_frame_index = 0
                elif animation.next_state:
                    self.change_state(animation.next_state)
                else:
                    self.change_state(FighterState.IDLE)
                    if self.state == FighterState.ATTACKING:
                        self.is_attacking = False  # 结束攻击状态

    def _get_current_frame(self) -> pygame.Surface:
        animation = self._get_current_animation()
        frame_data = animation.frames[self.current_frame_index]
        
        # 創建基礎幀
        frame = pygame.Surface((self.config.sprite_width, self.config.sprite_height), 
                             pygame.SRCALPHA)
        frame.blit(self.sprite_sheet, (0, 0), frame_data)
        
        # 縮放
        if self.config.scale != 1.0:
            new_size = (self.config.sprite_width * self.config.scale,
                       self.config.sprite_height * self.config.scale)
            frame = pygame.transform.scale(frame, new_size)
        
        # 翻轉
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
            
        return frame
    
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
        self._update_input_buffer(delta_time)
        for projectile in self.projectiles[:]:
            projectile.update(delta_time)
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)
    
    def _handle_physics(self, delta_time: float):
        if not self.on_ground:
            self.velocity.y += 5  # 重力
        
        self.position += self.velocity * delta_time
        
        # 基本地面碰撞
        if self.position.y > 580 - self.scaled_h:  # 這裡應該由遊戲系統提供真實的地面高度
            self.position.y = 580 - self.scaled_h
            self.velocity.y = 0
            self.on_ground = True
        if self.position.x < 100 and self.velocity.x < 0:
            self.velocity.x = 0
            return
        elif self.position.x > 1200 - self.scaled_w and self.velocity.x > 0:
            self.velocity.x = 0
            return
    
    def _update_hitboxes(self): 
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.hitbox.x = self.rect.x + (self.rect.width - self.hitbox.width) / 2
        self.hitbox.y = self.rect.y + (self.rect.height - self.hitbox.height) / 2
    
    def _update_input_buffer(self, delta_time: float):
        self.input_timer += delta_time
        if self.input_timer > 0.5:  # 清空超時的輸入
            self.input_buffer.clear()
            self.input_timer = 0
    
    def handle_input(self, input_string: str):
        """處理輸入並檢查特殊技能"""
        self.input_buffer.append(input_string)
        self.input_timer = 0
        
        # 檢查是否觸發特殊技能
        if self.config.special_moves:
            for move_name, sequence in self.config.special_moves.items():
                if self._check_input_sequence(sequence):
                    self.perform_special_move(move_name)
                    self.input_buffer.clear()
                    break
    
    def _check_input_sequence(self, sequence: List[str]) -> bool:
        if len(self.input_buffer) < len(sequence):
            return False
        return self.input_buffer[-len(sequence):] == sequence
    
    def perform_special_move(self, move_name: str):
        """執行特殊技能（由子類實現具體效果）"""
        self.change_state(FighterState.SPECIAL)
    
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
        if not self.is_attacking and not self.is_blocking:
            self.attack_key_held = True
            if self.facing_right:
                self.move(direction)
            elif not self.facing_right:
                self.move(-direction)
            self.is_attacking = True
            self.attack_key_held = True
            self.change_state(FighterState.ATTACKING)
            
    def dash(self, direction: float):
        if not self.is_attacking and not self.is_blocking:
            self.dash_key_held = True
            if self.facing_right:
                self.move(direction)
            elif not self.facing_right:
                self.move(-direction)
            self.change_state(FighterState.DASH)
            
    def shoot(self, projectile_type: ProjectileType):
        """發射投射物"""
        if projectile_type in self.projectile_configs:
            config = self.projectile_configs[projectile_type]
            direction = 1 if self.facing_right else -1
            
            # 從角色位置發射
            projectile = Projectile(
                x=self.position.x + (self.rect.width if self.facing_right else 0),
                y=self.position.y,
                direction=direction,
                config=config
            )
            
            self.projectiles.append(projectile)
    
    def block(self):
        if not self.is_attacking:
            self.is_blocking = True
            self.change_state(FighterState.BLOCKING)
    
    def draw(self, screen: pygame.Surface):
        current_frame = self._get_current_frame()
        screen.blit(current_frame, self.position)
        for projectile in self.projectiles:
            projectile.draw(screen)

def read_sprite_map(file_path: str) -> Dict[str, List[Tuple[int, int, int, int]]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def create_kirby_config():
    mapping = read_sprite_map("resources/fighter/kirby_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/kirby_trans.png",
        sprite_width=32,
        sprite_height=32,
        scale=3.0,
        animations={
            FighterState.IDLE: AnimationConfig(
                frames=mapping["idle"],
                speed=0.3
            ),
            FighterState.WALKING: AnimationConfig(
                frames=mapping["walk"],
                speed=0.1
            ),
            FighterState.JUMPING: AnimationConfig(
                frames=mapping["jump"],
                speed=0.1
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.05,
                loop=False, 
                next_state=FighterState.IDLE
            ),
            FighterState.CROUCHING: AnimationConfig(
                frames=mapping["crouch"],
                speed=0.1
            ),
            FighterState.DASH: AnimationConfig(
                frames=mapping["dash"],
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            ),
            FighterState.HURT: AnimationConfig(
                frames=mapping["hurt"],
                speed=0.1
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SPECIAL: AnimationConfig(
                frames=[(x, 192, 32, 32) for x in range(0, 32*6, 32)],
                speed=0.1,
                next_state=FighterState.IDLE
            )
            
        },
        special_moves={
            "INHALE": ["DOWN", "B"],
            "SUPER_INHALE": ["DOWN", "DOWN", "B"],
        }
    )
    
class Kirby(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_kirby_config())
    
    def perform_special_move(self, move_name: str):
        super().perform_special_move(move_name)
        if move_name == "INHALE":
            # 實現吸入效果
            pass
        elif move_name == "SUPER_INHALE":
            # 實現超級吸入效果
            pass

def create_ryu_config():
    mapping = read_sprite_map("resources/fighter/ryu_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/ryu_trans.png",
        sprite_width=110,
        sprite_height=100,
        scale=2.0,
        animations={
            FighterState.IDLE: AnimationConfig(
                frames=mapping["idle"],
                speed=0.3
            ),
            FighterState.WALKING: AnimationConfig(
                frames=mapping["walk"],
                speed=0.1
            ),
            FighterState.JUMPING: AnimationConfig(
                frames=mapping["jump"],
                speed=0.1
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.1,
                loop=False, 
                next_state=FighterState.IDLE
            ),
            FighterState.CROUCHING: AnimationConfig(
                frames=mapping["crouch"],
                speed=0.1
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SPECIAL: AnimationConfig(
                frames=mapping["special"],
                speed=0.1,
                next_state=FighterState.IDLE
            )
            
        },
        special_moves={
            "HADOKEN": ["DOWN", "RIGHT", "PUNCH"],
            "SUPER_INHALE": ["DOWN", "DOWN", "B"],
        }
    )
    
class Ryu(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_ryu_config())
        mapping = read_sprite_map("resources/fighter/ryu_trans_mapping.json")
        self.projectile_configs[ProjectileType.WAVE] = ProjectileConfig(
            sprite_sheet_path="resources/fighter/ryu_trans.png",
            frames=mapping["hehe"],  # 假設有4幀動畫
            speed=300,
            damage=15,
            lifetime=2.0,
            scale=1.5,
            animation_speed=0.1
        )
    
    def perform_special_move(self, move_name: str):
        super().perform_special_move(move_name)
        if move_name == "HADOKEN":  # 波動拳
            self.shoot(ProjectileType.WAVE)
    