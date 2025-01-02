from PIL import Image
import os

def crop_and_center_image(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            # 打開圖片
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            
            # 獲取圖片的 alpha 通道（透明度）
            if img.mode != 'RGBA':
                continue
            alpha = img.split()[-1]
            
            # 找到有圖案的部分（非透明區域的邊界）
            bbox = alpha.getbbox()
            if bbox:
                cropped_img = img.crop(bbox)  # 裁切非透明區域
                new_size = max(cropped_img.size)  # 找到寬高的最大值，確保正方形
                
                # 建立一個新的透明背景圖片
                centered_img = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))
                offset = ((new_size - cropped_img.size[0]) // 2, 
                          (new_size - cropped_img.size[1]) // 2)
                centered_img.paste(cropped_img, offset)  # 將裁切後的圖片貼到中心
                
                # 儲存結果
                output_path = os.path.join(output_folder, filename)
                centered_img.save(output_path)
                print(f"Processed: {filename}")

# 使用範例
input_folder = "./character3"  # 替換成你的輸入資料夾路徑
output_folder = "./character_3"  # 替換成你的輸出資料夾路徑
crop_and_center_image(input_folder, output_folder)
