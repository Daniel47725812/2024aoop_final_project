import pygame
import json
import os
from dataclasses import asdict, dataclass
from typing import List

@dataclass
class FrameData:
    x: int
    y: int
    width: int
    height: int
    offset_x: float = 0
    offset_y: float = 0

class EnhancedSpriteMapper:
    def __init__(self, image_path, sprite_width, sprite_height):
        pygame.init()
        self.original_image = pygame.image.load(image_path)
        self.image_path = image_path
        self.width, self.height = self.original_image.get_size()
        
        # 設置視窗
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Enhanced Sprite Mapper - 按住 Shift 調整選擇框大小')
        
        # 選擇框設置
        self.selection_rect = pygame.Rect(0, 0, sprite_width, sprite_height)
        self.original_size = (sprite_width, sprite_height)
        self.resizing = False
        self.resize_start_pos = None
        
        # 狀態變數
        self.scale_factor = 1.0
        self.sprite_map = {}
        self.current_sprite_name = ""
        self.current_frame = 0
        self.offset_x = 0
        self.offset_y = 0
        
        # 顏色設置
        self.SELECT_COLOR = (255, 255, 0)
        self.OFFSET_COLOR = (0, 255, 0)
        
        # 隱藏滑鼠游標
        pygame.mouse.set_visible(False)

    def handle_zoom(self, zoom_in):
        if zoom_in:
            self.scale_factor = min(self.scale_factor + 0.1, 3.0)
        else:
            self.scale_factor = max(self.scale_factor - 0.1, 0.5)
            
        scaled_width = int(self.width * self.scale_factor)
        scaled_height = int(self.height * self.scale_factor)
        self.screen = pygame.display.set_mode((scaled_width, scaled_height))

    def handle_input(self):
        if not self.current_sprite_name:
            self.current_sprite_name = input("請輸入動畫名稱 (例如: 'idle'): ")
    
    def save_sprite_data(self):
        output_path = os.path.splitext(self.image_path)[0] + '_mapping.json'
        
        # 轉換數據格式為 FrameData
        formatted_data = {}
        for anim_name, frames in self.sprite_map.items():
            formatted_data[anim_name] = []
            for frame in frames:
                frame_data = FrameData(
                    x=frame['x'],
                    y=frame['y'],
                    width=frame['width'],
                    height=frame['height'],
                    offset_x=frame.get('offset_x', 0),
                    offset_y=frame.get('offset_y', 0)
                )
                formatted_data[anim_name].append(asdict(frame_data))
        
        with open(output_path, 'a', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=4, ensure_ascii=False)
        print(f"Sprite 映射已保存到: {output_path}")
    
    def draw(self):
        # 縮放原始圖片
        scaled_image = pygame.transform.smoothscale(
            self.original_image, 
            (int(self.width * self.scale_factor), 
             int(self.height * self.scale_factor))
        )
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_image, (0, 0))
        
        # 繪製選擇框
        scaled_rect = self.selection_rect.copy()
        scaled_rect.x *= self.scale_factor
        scaled_rect.y *= self.scale_factor
        scaled_rect.width *= self.scale_factor
        scaled_rect.height *= self.scale_factor
        pygame.draw.rect(self.screen, self.SELECT_COLOR, scaled_rect, 2)
        
        # 繪製偏移點
        offset_x = (self.selection_rect.x + self.offset_x) * self.scale_factor
        offset_y = (self.selection_rect.y + self.offset_y) * self.scale_factor
        pygame.draw.circle(self.screen, self.OFFSET_COLOR, (int(offset_x), int(offset_y)), 3)
    
    def run(self):
        running = True
        self.handle_input()
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左鍵點擊
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shift + 左鍵開始調整大小
                            self.resizing = True
                            self.resize_start_pos = pygame.mouse.get_pos()
                        else:  # 一般左鍵點擊，保存幀
                            if self.current_sprite_name not in self.sprite_map:
                                self.sprite_map[self.current_sprite_name] = []
                            
                            frame_data = {
                                'x': self.selection_rect.x,
                                'y': self.selection_rect.y,
                                'width': self.selection_rect.width,
                                'height': self.selection_rect.height,
                                'offset_x': self.offset_x,
                                'offset_y': self.offset_y
                            }
                            
                            self.sprite_map[self.current_sprite_name].append(frame_data)
                            self.current_frame += 1
                            print(f"已添加幀 {self.current_frame-1} 到 '{self.current_sprite_name}'")
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.resizing = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.resizing:
                        current_pos = pygame.mouse.get_pos()
                        dx = (current_pos[0] - self.resize_start_pos[0]) / self.scale_factor
                        dy = (current_pos[1] - self.resize_start_pos[1]) / self.scale_factor
                        self.selection_rect.width = max(1, int(self.original_size[0] + dx))
                        self.selection_rect.height = max(1, int(self.original_size[1] + dy))
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS:  # '+' 放大
                        self.handle_zoom(True)
                    elif event.key == pygame.K_MINUS:  # '-' 縮小
                        self.handle_zoom(False)
                    elif event.key == pygame.K_SPACE:
                        self.save_sprite_data()
                        self.current_sprite_name = ""
                        self.current_frame = 0
                        self.handle_input()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if self.current_sprite_name in self.sprite_map and self.sprite_map[self.current_sprite_name]:
                            self.sprite_map[self.current_sprite_name].pop()
                            self.current_frame = max(0, self.current_frame - 1)
                            print("已復原上一次選擇")
                    # 使用方向鍵調整偏移量
                    elif event.key == pygame.K_LEFT:
                        self.offset_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.offset_x += 1
                    elif event.key == pygame.K_UP:
                        self.offset_y -= 1
                    elif event.key == pygame.K_DOWN:
                        self.offset_y += 1
            
            if not self.resizing:
                mouse_pos = pygame.mouse.get_pos()
                scaled_mouse_pos = (mouse_pos[0] / self.scale_factor, 
                                  mouse_pos[1] / self.scale_factor)
                self.selection_rect.center = scaled_mouse_pos
            
            self.selection_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        self.save_sprite_data()

def main():
    import sys
    
    if len(sys.argv) != 4:
        print("使用方式: python enhanced_sprite_mapper.py <sprite_sheet.png> <sprite_width> <sprite_height>")
        print("例如: python enhanced_sprite_mapper.py kirby.png 32 32")
        return
        
    image_path = sys.argv[1]
    sprite_width = int(sys.argv[2])
    sprite_height = int(sys.argv[3])
    
    mapper = EnhancedSpriteMapper(image_path, sprite_width, sprite_height)
    mapper.run()

if __name__ == "__main__":
    main()