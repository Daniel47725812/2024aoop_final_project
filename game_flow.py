import pygame
import sys
import player_temp as player

# 初始化 Pygame
pygame.init()

# 設定畫面大小
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
item_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
blur_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
character_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("格鬥遊戲")

# 設定遊戲時鐘
clock = pygame.time.Clock()
FPS = 60

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 定義遊戲狀態
STATE_MENU = "menu"
STATE_PLAYER_SELECT = "player_select"
STATE_CHARACTER_SELECT = "character_select"
STATE_FIELD_SELECT = "field_select"
STATE_BATTLE = "battle"
STATE_RESULT = "result"

# 初始化玩家
player1 = player.Player(300, 300, (0, 0, 255))
player2 = player.Player(600, 300, (0, 255, 0))


# 初始遊戲狀態
game_state = STATE_MENU
player_count_selection = 1  # 預設選擇一位玩家
field_num = 0               # 預設選擇第一個場景
countdown = 20              # 遊戲時間
start_time = 0              # 遊戲開始時間
round = 1                   # 遊戲回合

def draw_text_centered(text, font, color, surface, x, y):
    # 渲染文字
    rendered_text = font.render(text, True, color)
    # 獲取文字的矩形邊界
    text_rect = rendered_text.get_rect(center=(x, y))
    # 將文字繪製到螢幕上
    surface.blit(rendered_text, text_rect)


#遊戲封面畫面
def draw_menu():
    global bg
    # bg = pygame.image.load("./resources/background/bg1.png")
    bg = pygame.image.load("./resources/Fight Font/ft_019.png")
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))
    blur_surface.fill((255, 255, 255, 100))
    screen.blit(blur_surface, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Press Any Key to Start", font, BLACK, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)


#選擇玩家人數

def draw_player_select():
    screen.blit(bg, (0, 0))
    screen.blit(blur_surface, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Select Number of Players", font, BLACK, screen, SCREEN_WIDTH//2, 150)

    # 繪製玩家人數選項
    options = ["1 Player", "2 Players"]
    for i, option in enumerate(options):
        color = BLACK
        if i + 1 == player_count_selection:
            color = (0, 255, 0)  # 高亮顏色（綠色）

        draw_text_centered(option, font, color, screen, SCREEN_WIDTH//2, 250 + i * 100)

def handle_player_select_input(event):
    global player_count_selection, game_state, num_players

    if event.key in (pygame.K_w, pygame.K_UP):  # 上移
        player_count_selection = max(1, player_count_selection - 1)
    elif event.key in (pygame.K_s, pygame.K_DOWN):  # 下移
        player_count_selection = min(2, player_count_selection + 1)
    elif event.key == pygame.K_RETURN:  # 確認選擇
        num_players = player_count_selection
        game_state = STATE_CHARACTER_SELECT



# 定義角色選項
characters = ["Character 1", "Character 2", "Character 3"]
player1_selection = 0
player2_selection = 0
num_players = 1  # 默認只有一位玩家

def draw_character_select():
    screen.blit(bg, (0, 0))
    screen.blit(blur_surface, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Select Characters", font, BLACK, screen, SCREEN_WIDTH//2, 100)
    if num_players == 1:
        draw_text_centered("Player 1", font, BLACK, screen, SCREEN_WIDTH//2, 200)
        p1 = pygame.image.load("./resources/character_" + str(player1_selection + 1) + "/000.png")
        p1 = pygame.transform.scale2x(p1)
        screen.blit(p1, (SCREEN_WIDTH//2 - p1.get_width()//2, 375 - p1.get_height()//2))
    else:
        draw_text_centered("Player 1", font, BLACK, screen, SCREEN_WIDTH//4, 200)
        p1 = pygame.image.load("./resources/character_" + str(player1_selection + 1) + "/000.png")
        p1 = pygame.transform.scale2x(p1)
        screen.blit(p1, (SCREEN_WIDTH//4 - p1.get_width()//2, 375 - p1.get_height()//2))
        draw_text_centered("Player 2", font, BLACK, screen, SCREEN_WIDTH//4 * 3, 200)
        p2 = pygame.image.load("./resources/character_" + str(player2_selection + 1) + "/000.png")
        p2 = pygame.transform.scale2x(p2)
        screen.blit(p2, (SCREEN_WIDTH//4 * 3 - p2.get_width()//2, 375 - p2.get_height()//2))
    

def handle_character_select_input(event):
    global player1_selection, player2_selection, game_state

    if event.key == pygame.K_a:  # 左
        player1_selection = (player1_selection - 1) % len(characters)
    elif event.key == pygame.K_d:  # 右
        player1_selection = (player1_selection + 1) % len(characters)

    if num_players == 2:  # 雙人模式
        # 玩家2控制（方向鍵）
        if event.key == pygame.K_LEFT:  # 左
            player2_selection = (player2_selection - 1) % len(characters)
        elif event.key == pygame.K_RIGHT:  # 右 
            player2_selection = (player2_selection + 1) % len(characters)

        # 確認選擇（假設兩位玩家都按下 Enter）
    if event.key == pygame.K_RETURN:
        game_state = STATE_FIELD_SELECT



#選擇場景
def draw_field_select():
    global bg, field_num
    bg = pygame.image.load("./resources/background/bg" + str(field_num + 1) + ".png")
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))
    screen.blit(blur_surface, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("field" + str(field_num + 1), font, BLACK, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

def handle_field_input(event):
    global game_state, field_num

    if event.key in (pygame.K_a, pygame.K_LEFT):  # 左
        field_num = (field_num - 1) % 3
    elif event.key in (pygame.K_d, pygame.K_RIGHT):  # 右
        field_num = (field_num + 1) % 3

    if event.key == pygame.K_RETURN:
        game_state = STATE_BATTLE
        start_time = pygame.time.get_ticks()
    
    


# 更新 draw_battle 函數
def draw_battle():
    global bg
    screen.blit(bg, (0, 0))
    screen.blit(item_surface, (0, 0))

    # 繪製玩家
    player1.draw(character_surface)
    if num_players == 2:  # 只有雙人模式才繪製玩家2
        player2.draw(character_surface)

    screen.blit(character_surface, (0, 0))

# 更新 handle_battle_input 函數
def handle_battle_input(event):
    global game_state
    if event.key == pygame.K_ESCAPE:
        game_state = STATE_RESULT



#結算畫面
def draw_result():
    screen.blit(bg, (0, 0))
    screen.blit(blur_surface, (0, 0))
    screen.blit(item_surface, (0, 0))
    screen.blit(character_surface, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Game Over, Press R to restart", font, BLACK, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

def handle_result_input(event):
    global game_state
    if event.key == pygame.K_r:
        game_state = STATE_MENU



# 更新遊戲循環中的輸入處理
while True:
    keys = pygame.key.get_pressed()
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# 關閉視窗
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:# 按鍵事件
            if game_state == STATE_MENU:
                game_state = STATE_PLAYER_SELECT
            elif game_state == STATE_PLAYER_SELECT:
                handle_player_select_input(event)
            elif game_state == STATE_CHARACTER_SELECT:
                handle_character_select_input(event)
            elif game_state == STATE_FIELD_SELECT:
                handle_field_input(event)
            elif game_state == STATE_BATTLE:
                handle_battle_input(event)
            elif game_state == STATE_RESULT:
                handle_result_input(event)

    # 根據遊戲狀態更新畫面
    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYER_SELECT:
        draw_player_select()
    elif game_state == STATE_CHARACTER_SELECT:
        draw_character_select()
    elif game_state == STATE_FIELD_SELECT:
        draw_field_select()
    elif game_state == STATE_BATTLE:
        item_surface.fill((0, 0, 0, 0))
        character_surface.fill((0, 0, 0, 0))
        # 計算剩餘時間
        current_time = pygame.time.get_ticks()
        remaining_time = max(0, countdown - (current_time - start_time)//1000)
        # 繪製剩餘時間
        font = pygame.font.Font(None, 74)
        draw_text_centered(str(remaining_time), font, BLACK, item_surface, SCREEN_WIDTH//2, 50)
        # 時間到，遊戲結束
        if remaining_time == 0:
            round += 1
            start_time = current_time
            if round >= 3:
                game_state = STATE_RESULT
        # 更新玩家移動與攻擊
        player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        if keys[pygame.K_f]:
            player1.attack()
        player1.update()
        if num_players == 2:  # 只有雙人模式才更新玩家2
            player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
            if keys[pygame.K_k]:
                player2.attack()
            player2.update()
            # 碰撞檢測
            if player1.is_attacking and player1.rect.colliderect(player2.rect):
                print("Player 1 hits Player 2!")
            if player2.is_attacking and player2.rect.colliderect(player1.rect):
                print("Player 2 hits Player 1!")
        draw_battle()
    elif game_state == STATE_RESULT:
        draw_result()
    
    # 更新畫面
    pygame.display.flip()
    clock.tick(FPS)

