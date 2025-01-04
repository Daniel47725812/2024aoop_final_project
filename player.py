from BasePlayer import BasePlayer
from player_config import create_kirby_config, create_ryu_config
import json
from typing import Dict, List, Tuple
from Projectile import ProjectileType, ProjectileConfig, ProjectileHitboxData

def read_sprite_map(file_path: str) -> Dict[str, List[Tuple[int, int, int, int]]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
class Kirby(BasePlayer):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_kirby_config())
        mapping = read_sprite_map("resources/fighter/kirby_trans_mapping.json")
        self.projectile_configs[ProjectileType.WAVE] = ProjectileConfig(
            sprite_sheet_path="resources/fighter/kirby_trans.png",
            frames=mapping["hehe"],
            speed=300,
            damage=50,
            lifetime=3,
            scale=1.5,
            animation_speed=0.01
        )
    
    def perform_special_move(self, move_name: str):
        super().perform_special_move(move_name)
        if move_name == "INHALE":
            self.shoot(ProjectileType.WAVE)
       
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
    
    def perform_special_move(self, move_name: str):
        super().perform_special_move(move_name)
        if move_name == "HADOKEN":  # 波動拳
            self.shoot(ProjectileType.WAVE)
    