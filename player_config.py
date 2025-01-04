from typing import Dict, List, Tuple
import json
from BasePlayer import CharacterConfig, FighterState, AnimationConfig, HitboxData
from BasePlayer import BasePlayer
from Projectile import ProjectileType, ProjectileConfig, ProjectileHitboxData

def read_sprite_map(file_path: str) -> Dict[str, List[Tuple[int, int, int, int]]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def create_kirby_config():
    mapping = read_sprite_map("resources/fighter/kirby_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/kirby_trans.png",
        base_width=32,
        base_height=32,
        scale=5.0,
        health=100,
        attack_power=10,
        speed=10,
        jump_power=-600.0,
        
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
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.05,
                loop=False, 
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(0.8, 0.5, 0.3, 0.2, True)   # 拳頭攻擊判定
                        ]
            ),
            FighterState.DASH: AnimationConfig(
                frames=mapping["dash"],
                speed=0.03,
                loop=False,
                next_state=FighterState.IDLE
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SHOOT: AnimationConfig(
                frames=mapping["shoot"],
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            )
            
        },
        cooldowns={
            "SHOOT": 3.0,
            "ATTACK": 0.1,
            "DASH": 2.0
        }
    )
    
class Kirby(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_kirby_config())
        mapping = read_sprite_map("resources/fighter/kirby_trans_mapping.json")
        self.projectile_configs[ProjectileType.FIREBALL] = ProjectileConfig(
            sprite_sheet_path="resources/fighter/kirby_trans.png",
            frames=mapping["hehe"],
            speed=300,
            damage=50,
            lifetime=3,
            scale=1.5,
            animation_speed=0.01
        )
        
    def shoot(self):
        self._shoot(ProjectileType.FIREBALL)
    

def create_ryu_config():
    mapping = read_sprite_map("resources/fighter/ryu_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/ryu_trans.png",
        base_width=110,
        base_height=100,
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
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.05,
                loop=False, 
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(1.0, 0.09, 0.3, 0.2, True)   # 拳頭攻擊判定
                        ]
            ),
            FighterState.DASH: AnimationConfig(
                frames=mapping["dash"],
                speed=0.05
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SHOOT: AnimationConfig(
                frames=mapping["shoot"],
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            )
            
        },
        cooldowns={
            "SHOOT": 3.0,
            "ATTACK": 0.1,
            "DASH": 2.0
        }
    )
    
class Ryu(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_ryu_config())
        mapping = read_sprite_map("resources/fighter/ryu_trans_mapping.json")
        self.projectile_configs[ProjectileType.WAVE] = ProjectileConfig(
            sprite_sheet_path="resources/fighter/ryu_trans.png",
            frames=mapping["hehe"],
            speed=300,
            damage=50,
            lifetime=2,
            scale=1.5,
            animation_speed=0.1,
            hitbox=ProjectileHitboxData(
                        x=0.25,    # 碰撞箱從投射物寬度的 25% 處開始
                        y=0.25,    # 碰撞箱從投射物高度的 25% 處開始
                        width=0.5, # 碰撞箱寬度為投射物寬度的 50%
                        height=0.5 # 碰撞箱高度為投射物高度的 50%
                    )
        )
    
    def shoot(self):
        self._shoot(ProjectileType.WAVE)
    
def create_restu_config():
    mapping = read_sprite_map("resources/fighter/retsu_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/retsu_trans.png",
        base_width=70,
        base_height=110,
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
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.05,
                loop=False, 
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(1.0, 0.09, 0.3, 0.2, True)   # 拳頭攻擊判定
                        ]
            ),
            FighterState.DASH: AnimationConfig(
                frames=mapping["dash"],
                speed=0.05
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SHOOT: AnimationConfig(
                frames=mapping["shoot"],
                speed=0.1,
                loop=False,
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(1.0, 0.09, 0.3, 0.2, True)   # 拳頭攻擊判定
                        ]
            )
            
        },
        cooldowns={
            "SHOOT": 3.0,
            "ATTACK": 0.1,
            "DASH": 2.0
        }
    )
    
class Retsu(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_restu_config())
        
    def shoot(self, other: BasePlayer):
        self.change_state(FighterState.SHOOT)
        if self.facing_right:
            self.velocity.x = 1500
        else:
            self.velocity.x = -1500
        if self.position.x == other.position.x:
            print("hit")
            self.velocity.x = 0
            self.change_state(FighterState.IDLE)
        