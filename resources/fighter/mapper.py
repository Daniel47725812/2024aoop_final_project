import pygame
import json
import os

class CleanSpriteMapper:
    def __init__(self, image_path, sprite_width, sprite_height):
        """
        初始化完全無軌跡的 sprite sheet 映射器
        """
        pygame.init()
        # 載入並轉換圖片以優化性能
        self.original_image = pygame.image.load(image_path)
        self.image_path = image_path
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite_map = {}
        self.current_sprite_name = ""
        self.current_frame = 0
        
        # 設置視窗
        self.width, self.height = self.original_image.get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sprite Mapper - 移動選擇框，點擊確認')
        
        # 創建背景圖層
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))  # 黑色背景
        
        # 選擇框設置
        self.selection_rect = pygame.Rect(0, 0, sprite_width, sprite_height)
        
        # 顏色設置
        self.SELECT_COLOR = (255, 255, 0)  # 黃色選擇框

        # 隱藏滑鼠游標
        pygame.mouse.set_visible(False)

        # 縮放設置
        self.scale_factor = 1.0  # 預設縮放比例為 1.0

    def handle_zoom(self, zoom_in):
        """處理縮放"""
        if zoom_in:
            self.scale_factor = min(self.scale_factor + 0.1, 3.0)  # 最大放大到 3 倍
        else:
            self.scale_factor = max(self.scale_factor - 0.1, 0.5)  # 最小縮小到 0.5 倍
        
        # 根據縮放比例更新畫面尺寸
        scaled_width = int(self.width * self.scale_factor)
        scaled_height = int(self.height * self.scale_factor)
        self.screen = pygame.display.set_mode((scaled_width, scaled_height))

    def handle_input(self):
        """處理使用者輸入"""
        if not self.current_sprite_name:
            self.current_sprite_name = input("請輸入動畫名稱 (例如: 'walk_right'): ")
    
    def save_sprite_data(self):
        """保存 sprite 數據到 JSON 文件"""
        output_path = os.path.splitext(self.image_path)[0] + '_mapping.json'
        with open(output_path, 'a', encoding='utf-8') as f:
            json.dump(self.sprite_map, f, indent=4, ensure_ascii=False)
        print(f"Sprite 映射已保存到: {output_path}")
    
    def draw(self):
        """重新繪製整個畫面"""
        # 縮放原始圖片
        scaled_image = pygame.transform.smoothscale(self.original_image, 
                                                    (int(self.width * self.scale_factor), 
                                                     int(self.height * self.scale_factor)))
        
        # 先清空畫面
        self.screen.fill((0, 0, 0))
        
        # 繪製縮放後的圖片
        self.screen.blit(scaled_image, (0, 0))
        
        # 繪製當前選擇框（需要縮放位置）
        scaled_rect = self.selection_rect.copy()
        scaled_rect.x *= self.scale_factor
        scaled_rect.y *= self.scale_factor
        scaled_rect.width *= self.scale_factor
        scaled_rect.height *= self.scale_factor
        pygame.draw.rect(self.screen, self.SELECT_COLOR, scaled_rect, 2)
    
    def run(self):
        """運行主循環"""
        running = True
        self.handle_input()
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左鍵點擊
                        # 保存選擇的區域
                        if self.current_sprite_name not in self.sprite_map:
                            self.sprite_map[self.current_sprite_name] = []
                        
                        frame_data = (self.selection_rect.x, self.selection_rect.y, self.sprite_width, self.sprite_height)
                        
                        self.sprite_map[self.current_sprite_name].append(frame_data)
                        self.current_frame += 1
                        print(f"已添加幀 {self.current_frame-1} 到 '{self.current_sprite_name}'")
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # '+' 放大
                        self.handle_zoom(True)
                    elif event.key == pygame.K_MINUS:  # '-' 縮小
                        self.handle_zoom(False)
                    elif event.key == pygame.K_SPACE:
                        # 完成當前動畫，開始新的
                        self.save_sprite_data()
                        self.current_sprite_name = ""
                        self.current_frame = 0
                        self.handle_input()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # 復原上一次的選擇
                        if self.current_sprite_name in self.sprite_map and self.sprite_map[self.current_sprite_name]:
                            self.sprite_map[self.current_sprite_name].pop()
                            self.current_frame = max(0, self.current_frame - 1)
                            print("已復原上一次選擇")
                    elif event.key == pygame.K_UP:
                        self.sprite_height += 1
                    elif event.key == pygame.K_DOWN:
                        self.sprite_height = max(1, self.sprite_height - 1)
                    elif event.key == pygame.K_LEFT:
                        self.sprite_width = max(1, self.sprite_width - 1)
                    elif event.key == pygame.K_RIGHT:
                        self.sprite_width += 1
            
            # 更新選擇框位置到滑鼠位置
            mouse_pos = pygame.mouse.get_pos()
            scaled_mouse_pos = (mouse_pos[0] / self.scale_factor, mouse_pos[1] / self.scale_factor)
            self.selection_rect.center = scaled_mouse_pos
            
            # 確保選擇框不會超出圖片範圍
            self.selection_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
            
            # 完全重新繪製畫面
            self.draw()
            
            # 更新顯示
            pygame.display.flip()
            
            # 控制更新率
            clock.tick(60)
        
        pygame.quit()
        self.save_sprite_data()

def main():
    """主函數"""
    import sys
    
    if len(sys.argv) != 4:
        print("使用方式: python clean_sprite_mapper.py <sprite_sheet.png> <sprite_width> <sprite_height>")
        print("例如: python clean_sprite_mapper.py kirby.png 32 32")
        return
        
    image_path = sys.argv[1]
    sprite_width = int(sys.argv[2])
    sprite_height = int(sys.argv[3])
    
    mapper = CleanSpriteMapper(image_path, sprite_width, sprite_height)
    mapper.run()

if __name__ == "__main__":
    main()
