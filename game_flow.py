import pygame
import sys
from player_config import Kirby, Ryu, Retsu
from BasePlayer import FighterState
import random
import gif_pygame

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
game_time = clock.get_time()
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

# 定義字體
font_path = "Font/PressStart2P-Regular.ttf"

# 初始遊戲狀態
def init_game():
    global game_state, player_count_selection, field_num, countdown, start_time, round, goal1, goal2, player1, player2, characters, characters2
        
    game_state = STATE_MENU
    player_count_selection = 1  # 預設選擇一位玩家
    field_num = 0               # 預設選擇第一個場景
    countdown = 60              # 遊戲時間
    start_time = 0              # 遊戲開始時間
    round = 1                   # 遊戲回合
    goal1 = 0                   # 1p得分
    goal2 = 0                   # 2p得分
    characters = [Kirby(0, 0), Ryu(0, 0), Retsu(0, 0)]
    characters2 = [Kirby(0, 0), Ryu(0, 0), Retsu(0, 0)]
    player1 = characters[0]
    player2 = characters2[0]

# 載入圖片
def load_image():
    global menu, bg, point_img, blood_bar_0, blood_bar_1, blood_bar_2, num_img, round_img, dash_img, skill_img, cd_img

    menu = pygame.image.load("./resources/Fight Font/image.png")
    menu = pygame.transform.scale(menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bg = []
    temp = gif_pygame.load("resources/background/bg1_t.gif")
    bg.append(temp)
    temp1 = gif_pygame.load("resources/background/bg2_t.gif")
    bg.append(temp1)
    temp2 = gif_pygame.load("resources/background/bg3_t.gif")
    bg.append(temp2)

    point_img = pygame.image.load("./resources/Fight Font/coin.png")
    point_img = pygame.transform.scale(point_img, (50, 50))

    blood_bar_0 = pygame.image.load("./resources/Fight Font/ft_018.png")
    blood_bar_0 = pygame.transform.scale(blood_bar_0, (400, 30))
    blood_bar_1 = pygame.image.load("./resources/Fight Font/ft_002.png")
    blood_bar_1 = pygame.transform.scale(blood_bar_1, (400, 30))
    blood_bar_2 = pygame.image.load("./resources/Fight Font/ft_002.png")
    blood_bar_2 = pygame.transform.scale(blood_bar_2, (400, 30))

    num_img = []
    for i in range(10):
        num_img.append(pygame.image.load(f"./resources/Fight Font/ft_{(i+3):03d}.png"))
        num_img[i] = pygame.transform.scale2x(num_img[i])

    round_img = []
    for i in range(4):
        round_img.append(pygame.image.load(f"./resources/Fight Font/ft_{(i+51):03d}.png"))
        round_img[i] = pygame.transform.scale2x(round_img[i])
    
    dash_img = pygame.image.load("./resources/Fight Font/dash.png")
    dash_img = pygame.transform.scale(dash_img, (50, 50))

    skill_img = pygame.image.load("./resources/Fight Font/fire_ball.png")
    skill_img = pygame.transform.scale(skill_img, (50, 50))

    cd_img = pygame.image.load("./resources/Fight Font/icon.png")
    cd_img = pygame.transform.scale(cd_img, (70, 70))


def draw_text_centered(text, font_path, font_size, color, surface, x, y):
    # 渲染文字
    font = pygame.font.Font(font_path, font_size)
    rendered_text = font.render(text, True, color)
    # 獲取文字的矩形邊界
    text_rect = rendered_text.get_rect(center=(x, y))
    # 將文字繪製到螢幕上
    surface.blit(rendered_text, text_rect)


#遊戲封面畫面
def draw_menu():
    screen.blit(menu, (0, 0))
    blur_surface.fill((255, 255, 255, 100))
    screen.blit(blur_surface, (0, 0))
    
    draw_text_centered("WILD PUNCH", font_path, 74, (235, 142, 85), screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
    
    if current_time % 1000 < 500:
        draw_text_centered("Press Any Key to Start", font_path, 24, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)


#選擇玩家人數

def draw_player_select():
    screen.blit(menu, (0, 0))
    screen.blit(blur_surface, (0, 0))
    draw_text_centered("Select Number of Players", font_path, 40, (235, 142, 85), screen, SCREEN_WIDTH//2, 150)

    # 繪製玩家人數選項
    options = ["1 Player", "2 Players"]
    for i, option in enumerate(options):
        color = WHITE
        if i + 1 == num_players and current_time % 1000 < 500:
            color = (0, 255, 0)  # 高亮顏色（綠色）

        draw_text_centered(option, font_path, 30, color, screen, SCREEN_WIDTH//2, 250 + i * 100)

def handle_player_select_input(event):
    global game_state, num_players

    if event.key in (pygame.K_w, pygame.K_UP):  # 上移
        num_players = 1
    elif event.key in (pygame.K_s, pygame.K_DOWN):  # 下移
        num_players = 2
    elif event.key == pygame.K_RETURN:  # 確認選擇
        game_state = STATE_CHARACTER_SELECT



# 定義角色選項
player1_selection = 0
player2_selection = 0
num_players = 1  # 默認只有一位玩家

def draw_character_select():
    screen.blit(menu, (0, 0))
    screen.blit(blur_surface, (0, 0))
    
    draw_text_centered("Select Characters", font_path, 40, (235, 142, 85), screen, SCREEN_WIDTH//2, 100)
    if current_time % 1000 < 500:
        draw_text_centered("Press Enter To Confirm", font_path, 24, (255, 227, 132), screen, SCREEN_WIDTH//2, 530)
    
    draw_text_centered("Player 1", font_path, 30, WHITE, screen, SCREEN_WIDTH//4, 200)
    global player1, player2
    if num_players == 2:  # 雙人模式
        draw_text_centered("Player 2", font_path, 30, WHITE, screen, SCREEN_WIDTH//4 * 3, 200)
    else:
        draw_text_centered("Computer", font_path, 30 , WHITE, screen, SCREEN_WIDTH//4 * 3, 200)
    player1.position.x = SCREEN_WIDTH//4 - player1.scaled_w//2
    player1.position.y = 460 - player1.scaled_h
    player1.draw(character_surface)
    player1.update(1/60)
    player2.position.x = SCREEN_WIDTH//4 * 3 - player2.scaled_w//2
    player2.position.y = 460 - player2.scaled_h
    player2.draw(character_surface)
    player2.update(1/60)

    screen.blit(character_surface, (0, 0))
    

def handle_character_select_input(event):
    global player1, player1_selection, player2, player2_selection, game_state

    if event.key == pygame.K_a:  # 左
        player1_selection = (player1_selection - 1) % len(characters)
    elif event.key == pygame.K_d:  # 右
        player1_selection = (player1_selection + 1) % len(characters)
    player1 = characters[player1_selection]

        # 玩家2控制（方向鍵）
    if event.key == pygame.K_LEFT:  # 左
        player2_selection = (player2_selection - 1) % len(characters)
    elif event.key == pygame.K_RIGHT:  # 右 
        player2_selection = (player2_selection + 1) % len(characters)
    player2 = characters2[player2_selection]

        # 確認選擇（假設兩位玩家都按下 Enter）
    if event.key == pygame.K_RETURN:
        game_state = STATE_FIELD_SELECT
        

#選擇場景
def draw_field_select():
    global field
    field = bg[field_num].blit_ready()
    screen.blit(field, (0, 0))
    screen.blit(blur_surface, (0, 0))
    draw_text_centered("field" + str(field_num + 1), font_path, 50, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

def handle_field_input(event):
    global game_state, field_num, start_time

    if event.key in (pygame.K_a, pygame.K_LEFT):  # 左
        field_num = (field_num - 1) % 3
    elif event.key in (pygame.K_d, pygame.K_RIGHT):  # 右
        field_num = (field_num + 1) % 3

    if event.key == pygame.K_RETURN:
        game_state = STATE_BATTLE
        start_time = pygame.time.get_ticks()

   
    
def simulate_keypress(key):
    global pre_key
    event = pygame.event.Event(pygame.KEYUP, {"key": pre_key, "is_simulated": True})
    pygame.event.post(event)
    pre_key = key
    event = pygame.event.Event(pygame.KEYDOWN, {"key": key, "is_simulated": True})
    pygame.event.post(event)

# computer
last_ai_action_time = 0
ai_action_interval = 0.5
pre_key = None
def ai_player_logic():
    global last_ai_action_time, simulate_key
    if pygame.time.get_ticks() - last_ai_action_time < ai_action_interval * 1000:
        return
    last_ai_action_time = pygame.time.get_ticks()
    
    # 角色距離
    x = player1.position.x - player2.position.x
    y = player1.position.y - player2.position.y
    if random.random() < 0.05:
        simulate_keypress(pygame.K_k)
    elif abs(x) > player1.scaled_w/1.6:
        if x < 0:
            simulate_keypress(pygame.K_LEFT)
        else:
            simulate_keypress(pygame.K_RIGHT)
        if abs(x) > player1.scaled_w*2:
            simulate_keypress(pygame.K_l)
    else:
        if y < -player1.scaled_h:
            simulate_keypress(pygame.K_UP)
        elif random.random() < 0.5:
            simulate_keypress(pygame.K_SEMICOLON)
        elif player2.health < 50:
            simulate_keypress(pygame.K_DOWN)
        else:
            simulate_keypress(None)

def detect_collision(player1, player2):
    # 攻擊
    if player2.check_collision(player1):
        player2.health -= player1.attack_power
        player1.is_attacking = False
    if player1.check_collision(player2):
        player1.health -= player2.attack_power
        player2.is_attacking = False
    # 飛行物
    if len(player1.projectiles) > 0:
        if player1.projectiles[-1].check_collision(player2.hitboxes):
            if not player2.is_blocking:
                player2.health -= player1.projectiles[-1].config.damage
            player1.projectiles.pop()
    if len(player2.projectiles) > 0:
        if player2.projectiles[-1].check_collision(player1.hitboxes):
            if not player1.is_blocking:
                player1.health -= player2.projectiles[-1].config.damage
            player2.projectiles.pop()

# 更新 draw_battle 函數
def draw_battle():
    global game_state, round, goal1, goal2, blood_bar_0, blood_bar_1, blood_bar_2
    field = bg[field_num].blit_ready()
    # 繪製玩家
    player1.draw(character_surface)
    player1.update(1/60)
    player2.draw(character_surface)
    player2.update(1/60)

    # 繪製血量條
    blood_bar_1 = pygame.transform.scale(blood_bar_1, (max(0, int(player1.health)*4), 30))
    blood_bar_2 = pygame.transform.scale(blood_bar_2, (max(0, int(player2.health)*4), 30))
    item_surface.blit(blood_bar_0, (50, 30))
    item_surface.blit(blood_bar_1, (50, 30))
    item_surface.blit(blood_bar_0, (750, 30))
    item_surface.blit(blood_bar_2, (750, 30))
    
    # 繪製回合數、分數
    if goal1 > 0:
        item_surface.blit(point_img, (460, 20))
        if goal1 > 1:
            item_surface.blit(point_img, (510, 20))
    if goal2 > 0:
        item_surface.blit(point_img, (690, 20))
        if goal2 > 1:
            item_surface.blit(point_img, (640, 20))
    if remaining_time == countdown:
        screen.blit(field, (0, 0))
        screen.blit(blur_surface, (0, 0))
        screen.blit(round_img[0], (SCREEN_WIDTH//2 - round_img[0].get_width()//5*3, SCREEN_HEIGHT//2 - round_img[0].get_height()//2))
        screen.blit(round_img[round], (SCREEN_WIDTH//2 + round_img[0].get_width()//5*2, SCREEN_HEIGHT//2 - round_img[round].get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(field, (0, 0))
        screen.blit(item_surface, (0, 0))
        screen.blit(blur_surface, (0, 0))
        fight = pygame.image.load("./resources/Fight Font/ft_063.png")
        fight = pygame.transform.scale2x(fight)
        screen.blit(fight, (SCREEN_WIDTH//2 - fight.get_width()//2, SCREEN_HEIGHT//2 - fight.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)

    # 繪製技能冷卻
    item_surface.blit(dash_img, (50, 530))
    item_surface.blit(dash_img, (1080, 530))
    item_surface.blit(skill_img, (125, 530))
    item_surface.blit(skill_img, (1015, 530))
    item_surface.blit(cd_img, (40, 520))
    item_surface.blit(cd_img, (1070, 520))
    item_surface.blit(cd_img, (110, 520))
    item_surface.blit(cd_img, (1000, 520))

    if player1.config.cooldowns["DASH"] > 0:
        pygame.draw.circle(character_surface, (255, 255, 255, 200), (75, 555), 25, 25)
        draw_text_centered(str(int(player1.config.cooldowns["DASH"])+1), font_path, 24, BLACK, character_surface, 75, 555)
    if player1.config.cooldowns["SHOOT"] > 0:
        pygame.draw.circle(character_surface, (255, 255, 255, 200), (148, 555), 25, 25)
        draw_text_centered(str(int(player1.config.cooldowns["SHOOT"])+1), font_path, 24, BLACK, character_surface, 148, 555)
    if player2.config.cooldowns["DASH"] > 0:
        pygame.draw.circle(character_surface, (255, 255, 255, 200), (1105, 555), 25, 25)
        draw_text_centered(str(int(player2.config.cooldowns["DASH"])+1), font_path, 24, BLACK, character_surface, 1105, 555)
    if player2.config.cooldowns["SHOOT"] > 0:
        pygame.draw.circle(character_surface, (255, 255, 255, 200), (1038, 555), 25, 25)
        draw_text_centered(str(int(player2.config.cooldowns["SHOOT"])+1), font_path, 24, BLACK, character_surface, 1038, 555)

    screen.blit(field, (0, 0))
    screen.blit(item_surface, (0, 0))
    screen.blit(character_surface, (0, 0))


def handle_battle_input(event):
    global game_state
    # 更新玩家移動與攻擊
    if event.key == pygame.K_ESCAPE:
        game_state = STATE_RESULT
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            player1.move(-20)
        elif event.key == pygame.K_d:
            player1.move(20)
        elif event.key == pygame.K_w:
            player1.jump()
        elif event.key == pygame.K_c:
            player1.attack()
        elif event.key == pygame.K_s:
            player1.block()
        elif event.key == pygame.K_v:
            player1.dash()
        elif event.key == pygame.K_b:
            if player1 == characters[2]:
                player1.shoot(player2)
            else:
                player1.shoot()
            
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_f:  # 松开攻击键
            player1.attack_key_held = False
            player1.velocity.x = 0
        if event.key in [pygame.K_a, pygame.K_d]:
            player1.velocity.x = 0
            player1.change_state(FighterState.IDLE)
        elif event.key == pygame.K_s:
            player1.is_blocking = False
            player1.change_state(FighterState.IDLE)
    
    # 更新玩家2移動與攻擊
    if num_players == 2 or (hasattr(event, "is_simulated") and event.is_simulated):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player2.move(-20)
            elif event.key == pygame.K_RIGHT:
                player2.move(20)
            elif event.key == pygame.K_UP:
                player2.jump()
            elif event.key == pygame.K_SEMICOLON:
                player2.attack()
            elif event.key == pygame.K_DOWN:
                player2.block()
            elif event.key == pygame.K_l:
                player2.dash()
            elif event.key == pygame.K_k:
                if player2 == characters2[2]:
                    player2.shoot(player1)
                else:
                    player2.shoot()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SEMICOLON:  # 松开攻击键
                player2.attack_key_held = False
                player2.velocity.x = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player2.velocity.x = 0
                player2.change_state(FighterState.IDLE)
            elif event.key == pygame.K_DOWN:
                player2.is_blocking = False
                player2.change_state(FighterState.IDLE)


#結算畫面
def draw_result():
    screen.blit(field, (0, 0))
    screen.blit(blur_surface, (0, 0))
    screen.blit(item_surface, (0, 0))
    screen.blit(character_surface, (0, 0))
    if goal1 > goal2:
        winner = pygame.image.load('./resources/Fight Font/ft_033.png')
    elif goal1 < goal2:
        winner = pygame.image.load('./resources/Fight Font/ft_034.png')
    elif player1.health > player2.health:
        winner = pygame.image.load('./resources/Fight Font/ft_033.png')
    else:
        winner = pygame.image.load('./resources/Fight Font/ft_034.png')
    winner = pygame.transform.scale2x(winner)
    screen.blit(winner, (SCREEN_WIDTH//2 - winner.get_width()//2, SCREEN_HEIGHT//2 - winner.get_height()//2))
    if current_time % 1000 < 500:
        draw_text_centered("Press R to Restart", font_path, 30, (235, 142, 85), screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)

def handle_result_input(event):
    global game_state
    if event.key == pygame.K_r:
        init_game()
        load_image()
        game_state = STATE_MENU


# main
if __name__ == "__main__":
    init_game()
    load_image()
    # 更新遊戲循環中的輸入處理
    while True:
        global current_time
        current_time = pygame.time.get_ticks()
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
            elif event.type == pygame.KEYUP:
                if game_state == STATE_BATTLE:
                    handle_battle_input(event)

        # 根據遊戲狀態更新畫面
        if game_state == STATE_MENU:
            draw_menu()
        elif game_state == STATE_PLAYER_SELECT:
            draw_player_select()
        elif game_state == STATE_CHARACTER_SELECT:
            character_surface.fill((0, 0, 0, 0))
            draw_character_select()
        elif game_state == STATE_FIELD_SELECT:
            draw_field_select()
        elif game_state == STATE_BATTLE:
            item_surface.fill((0, 0, 0, 0))
            character_surface.fill((0, 0, 0, 0))

            # 電腦模式
            if num_players == 1:
                ai_player_logic()
            
            # 計算剩餘時間
            current_time = pygame.time.get_ticks()
            remaining_time = max(0, countdown - (current_time - start_time)//1000)
            # 繪製剩餘時間
            unit_digit = num_img[remaining_time % 10]
            hundred_digit = num_img[remaining_time // 10]
            item_surface.blit(unit_digit, (SCREEN_WIDTH//2, 20))
            item_surface.blit(hundred_digit, (SCREEN_WIDTH//2 - hundred_digit.get_width(), 20))

            # 碰撞檢測
            detect_collision(player1, player2)
            
            if player1 == characters[2] and player1.state == FighterState.SHOOT and player1.config.cooldowns["SHOOT"] > 0:
                if abs(player1.position.x - player2.position.x) < 30:
                    player1.velocity.x = 0
                    player2.health -= 20
                    player1.change_state(FighterState.IDLE)
            if player2 == characters2[2] and player2.state == FighterState.SHOOT and player2.config.cooldowns["SHOOT"] > 0:
                if abs(player1.position.x - player2.position.x) < 30:
                    player2.velocity.x = 0
                    player1.health -= 20
                    player2.change_state(FighterState.IDLE)
            
            
            # 回合結束(時間到或有玩家血量歸零)
            if remaining_time == 0 or player1.health <= 0 or player2.health <= 0:
                round += 1
                start_time = current_time
                if player1.health > player2.health:
                    goal1 += 1
                elif player1.health < player2.health:
                    goal2 += 1
                if round > 3 or goal1 == 2 or goal2 == 2:
                    game_state = STATE_RESULT
                else:
                    ko = pygame.image.load("./resources/Fight Font/ft_030.png")
                    ko = pygame.transform.scale2x(ko)
                    if player1.health <= 0:
                        screen.blit(blood_bar_0, (50, 30))
                    else:
                        screen.blit(blood_bar_0, (750, 30))
                    screen.blit(ko, (SCREEN_WIDTH//2 - ko.get_width()//2, SCREEN_HEIGHT//2 - ko.get_height()//2))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    player1.health = 100
                    player2.health = 100
                    player1.position.x = SCREEN_WIDTH//4 - player1.scaled_w//2
                    player1.position.y = 400
                    player2.position.x = SCREEN_WIDTH//4 * 3 - player2.scaled_w//2
                    player2.position.y = 400
            draw_battle()
        elif game_state == STATE_RESULT:
            draw_result()
        
        # 更新畫面
        pygame.display.flip()
        clock.tick(FPS)
