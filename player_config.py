from typing import Dict, List, Tuple
import json
from BasePlayer import CharacterConfig, FighterState, AnimationConfig, HitboxData

def read_sprite_map(file_path: str) -> Dict[str, List[Tuple[int, int, int, int]]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def create_kirby_config():
    mapping = read_sprite_map("resources/fighter/kirby_trans_mapping.json")
    return CharacterConfig(
        sprite_sheet_path="resources/fighter/kirby_trans.png",
        base_width=32,
        base_height=32,
        scale=6.0,
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
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(0.8, 0.3, 0.3, 0.2, True)   # 拳頭攻擊判定
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
            FighterState.SPECIAL: AnimationConfig(
                frames=mapping["special"],
                speed=0.03,
                loop=False,
                next_state=FighterState.IDLE
            )
            
        },
        special_moves={
            "INHALE": ["SHOOT"]
        },
        cooldowns={
            "SHOOT": 3.0,
            "ATTACK": 0.1,
            "DASH": 2.0
        }
    )
    
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
                speed=0.1
            ),
            FighterState.ATTACKING: AnimationConfig(
                frames=mapping["attack"],
                speed=0.05,
                loop=False, 
                next_state=FighterState.IDLE,
                hitboxes=[
                            HitboxData(0.2, 0.1, 0.6, 0.8, False),  # 身體碰撞箱
                            HitboxData(1.0, 0.3, 0.3, 0.2, True)   # 拳頭攻擊判定
                        ]
            ),
            FighterState.DASH: AnimationConfig(
                frames=mapping["dash"],
                speed=0.1
            ),
            FighterState.BLOCKING: AnimationConfig(
                frames=mapping["block"],
                speed=0.1
            ),
            FighterState.SPECIAL: AnimationConfig(
                frames=mapping["special"],
                speed=0.03,
                loop=False,
                next_state=FighterState.IDLE
            )
            
        },
        special_moves={
            "HADOKEN": ["PUNCH"]
        },
        cooldowns={
            "SHOOT": 3.0,
            "ATTACK": 0.1,
            "DASH": 2.0
        }
    )