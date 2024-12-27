import pygame
import sys

# 初始化 Pygame
pygame.init()

# 設定畫面大小
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
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
STATE_BATTLE = "battle"
STATE_RESULT = "result"

# 初始遊戲狀態
game_state = STATE_MENU

def draw_text_centered(text, font, color, surface, x, y):
    # 渲染文字
    rendered_text = font.render(text, True, color)
    # 獲取文字的矩形邊界
    text_rect = rendered_text.get_rect(center=(x, y))
    # 將文字繪製到螢幕上
    surface.blit(rendered_text, text_rect)


#遊戲封面畫面
def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text_centered("Press Any Key to Start", font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)


#選擇玩家人數
# 玩家人數選擇初始值
player_count_selection = 1

def draw_player_select():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text_centered("Select Number of Players", font, WHITE, screen, SCREEN_WIDTH//2, 150)

    # 繪製玩家人數選項
    options = ["1 Player", "2 Players"]
    for i, option in enumerate(options):
        color = WHITE
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
characters = ["Character 1", "Character 2", "Character 3", "Random"]
player1_selection = 0
player2_selection = 0
num_players = 1  # 默認只有一位玩家

def draw_character_select():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    draw_text_centered("Select Characters", font, WHITE, screen, SCREEN_WIDTH//2, 100)

    # 繪製角色選項
    for i, char in enumerate(characters):
        color = WHITE
        if i == player1_selection:
            color = (0, 255, 0)  # 玩家1的選擇顏色（綠色）
        elif num_players == 2 and i == player2_selection:
            color = (0, 0, 255)  # 玩家2的選擇顏色（藍色）

        draw_text_centered(char, font, color, screen, SCREEN_WIDTH//2, 200 + i * 100)

def handle_character_select_input(event):
    global player1_selection, player2_selection, game_state

    if event.key == pygame.K_w:  # 上
        player1_selection = (player1_selection - 1) % len(characters)
    elif event.key == pygame.K_s:  # 下
        player1_selection = (player1_selection + 1) % len(characters)

    if num_players == 2:  # 雙人模式
        # 玩家2控制（方向鍵）
        if event.key == pygame.K_UP:  # 上
            player2_selection = (player2_selection - 1) % len(characters)
        elif event.key == pygame.K_DOWN:  # 下
            player2_selection = (player2_selection + 1) % len(characters)

        # 確認選擇（假設兩位玩家都按下 Enter）
    if event.key == pygame.K_RETURN:
        game_state = STATE_BATTLE



#打鬥場景
def draw_battle():
    global bg
    bg = pygame.image.load("./bg.gif")
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Battle Scene", font, WHITE, screen, SCREEN_WIDTH//2, 100)

def handle_battle_input(event):
    global game_state
    if event.key == pygame.K_ESCAPE:
        game_state = STATE_RESULT



#結算畫面
def draw_result():
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 74)
    draw_text_centered("Game Over, Press R to restart", font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

def handle_result_input(event):
    global game_state
    if event.key == pygame.K_r:
        game_state = STATE_MENU



#遊戲流程
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == STATE_MENU:
                game_state = STATE_PLAYER_SELECT
            elif game_state == STATE_PLAYER_SELECT:
                handle_player_select_input(event)
            elif game_state == STATE_CHARACTER_SELECT:
                handle_character_select_input(event)
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
    elif game_state == STATE_BATTLE:
        draw_battle()
    elif game_state == STATE_RESULT:
        draw_result()

    # 更新畫面
    pygame.display.flip()
    clock.tick(FPS)
