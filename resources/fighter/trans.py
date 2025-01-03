import pygame
import sys
from pygame.locals import *

def make_transparent(input_path, output_path, color_key=(173, 241, 207)):
    """
    將圖片的指定背景顏色變為透明
    
    參數:
    input_path: 輸入圖片路徑
    output_path: 輸出圖片路徑
    color_key: 要變透明的顏色 (預設為綠色 RGB(0,255,0))
    """
    # 初始化 Pygame
    pygame.init()
    
    try:
        # 載入圖片
        image = pygame.image.load(input_path)
        
        # 獲取圖片尺寸
        width, height = image.get_size()
        
        # 創建一個帶 alpha 通道的表面
        transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 將原圖轉換為像素陣列
        pixel_array = pygame.surfarray.pixels3d(image)
        
        # 遍歷每個像素
        for x in range(width):
            for y in range(height):
                pixel = pixel_array[x][y]
                # 如果像素顏色不是背景色，則保留該像素
                if tuple(pixel) != color_key:
                    transparent_surface.set_at((x, y), (*pixel, 255))
        
        # 保存結果
        pygame.image.save(transparent_surface, output_path)
        print(f"成功將圖片保存至 {output_path}")
        
    except Exception as e:
        print(f"處理圖片時發生錯誤: {str(e)}")
    
    finally:
        # 清理並退出 Pygame
        pygame.quit()

def main():
    # 使用範例
        
    input_path = 'retsu.png'
    output_path = 'retsu_trans.png'
    
    # 執行轉換
    make_transparent(input_path, output_path)

if __name__ == "__main__":
    main()