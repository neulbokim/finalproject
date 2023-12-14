import pygame
import random
from os import path
import numpy as np
from pygame.locals import *


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 400
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
STAIR_WIDTH = 40
STAIR_HEIGHT = 20
ALROS_SPEED = 5

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20220042 김현서")
clock = pygame.time.Clock()



font_title = pygame.font.match_font('arialblack')
def draw_title(surf, text, size, x, y):
    font = pygame.font.Font(font_title, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    
def draw_title_outline(surf, text, size, x, y):
    font = pygame.font.Font(font_title, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

font_name = pygame.font.match_font('cafe24ssurround')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# HP bar dimensions
hp_bar_width = 282
hp_bar_height = 16

##### HP 클래스
class HP(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load HP bar image
        self.image = pygame.image.load(path.join(img_dir, "HPbar.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.max_width = hp_bar_width
        self.current_width = self.max_width
        self.hp_ratio = self.max_width / hp_bar_height
        self.decay_factor = 0.05
        self.health_width = self.max_width

    def update_width(self, score):
        decrease_rate = score*self.decay_factor
        # Gradual decrease of the health bar width
        if self.current_width > 0:
            self.current_width -= decrease_rate
        else:
            self.current_width = 0
        
        # Check if Alros is not doing anything
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_SPACE] or keys[pygame.K_SLASH]):
            self.decrease_width(score)  # Adjust the decrease rate as needed
        
    
    def decrease_width(self, score):
        global up_well
        
        if up_well:
            self.current_width -= score * self.decay_factor
        
        self.health_width = int(self.current_width / self.hp_ratio)
        health_bar = pygame.Rect(60, 62, self.health_width, 16)
        
        #pygame.draw.rect(screen, RED, health_bar)
        
    
    def reset_width(self):
        self.current_width = self.max_width
        
            
            
   

##### alors 클래스
class Alros(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ### 스타트 이미지 불러오기
        self.start = pygame.image.load(path.join(img_dir, 'alros_start.png'))
        self.start = self.start.convert()
        self.start.set_colorkey(BLACK)
        ### 계단 올라가는 이미지 불러오기 (왼쪽, 오른쪽)
        self.walk_frames_l = []
        self.walk_frames_r = []
        for i in range(1, 4):
            # 왼쪽
            filename = 'alros_left_left_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename))
            img = img.convert()
            img.set_colorkey(BLACK)
            self.walk_frames_l.append(img)
            # 오른쪽
            filename = 'alros_right_left_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename))
            img = img.convert()
            img.set_colorkey(BLACK)
            self.walk_frames_r.append(img)
        ### 떨어질 때 이미지 불러오기
        # 왼쪽
        self.down_l = pygame.image.load(path.join(img_dir, 'alros_left_down.png'))
        self.down_l = self.down_l.convert()
        self.down_l.set_colorkey(BLACK)
        # 오른쪽
        self.down_r = pygame.image.load(path.join(img_dir, 'alros_right_down.png'))
        self.down_r = self.down_r.convert()
        self.down_r.set_colorkey(BLACK)
      
        ### 현재 이미지를 스타트 이미지로 설정
        self.image = self.start
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2 + STAIR_WIDTH/2
        self.rect.y = 400
        
        ### 알로스의 health 값 설정
        self.health = 100 # Initial health value
        self.max_health = 100 # Maximum health value
        
        ### 프레임 번호 설정
        self.frame_index = 0
        
        ### last_update
        self.last_update = pygame.time.get_ticks()
        
        ### down_time
        self.down_time = 0


    def update(self):
        # Update animation and health bar
        self.update_animation()
        
        # Check if Alros is in the falling state
        if self.rect.y > HEIGHT:
            self.rect.y = 400  # Reset the position
            self.down_time = 0
            
    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:  # Animation speed control (update every 150 milliseconds)
            self.last_update = now
            # Use len() directly on the list
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames_l)

        # Check for consecutive space key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Increase the animation speed for consecutive space key presses
            now = pygame.time.get_ticks()
            if now - self.last_update < 150:  # Change animation every 150 milliseconds
                self.last_update = now

                # Update frame index for consecutive key presses
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_l)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y -= y
        



# 계단 클래스
class Stair(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = stair_level_1
        self.image_2 = stair_level_2
        self.image_3 = stair_level_3
        
        self.image = self.image_1.copy()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        if self.rect.y < -3200:
            self.image = stair_level_3.copy()
        elif self.rect.y < -1500:
            self.image = stair_level_2.copy()
        
        
        
        
        
def draw_score(score):
    text = str(score)
    score_size = 54
    score_outline = 2
    
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 5  - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 5  + score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 5  - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 5  + score_outline )
    draw_title(screen, text, score_size, WIDTH / 2 , HEIGHT / 5)
    

def show_go_screen():
    screen.blit(background, background_rect)
    title_size = 60
    outline = 3
    draw_title_outline(screen, "INFINITE", title_size, WIDTH / 2 + outline, HEIGHT / 4 - title_size -outline)
    draw_title_outline(screen, "INFINITE", title_size, WIDTH / 2 + outline, HEIGHT / 4 - title_size +outline)
    draw_title_outline(screen, "INFINITE", title_size, WIDTH / 2 - outline, HEIGHT / 4 - title_size -outline)
    draw_title_outline(screen, "INFINITE", title_size, WIDTH / 2 - outline, HEIGHT / 4 - title_size +outline)
    
    draw_title_outline(screen, "LOYOLA", title_size, WIDTH / 2 + outline, HEIGHT / 4 - outline)
    draw_title_outline(screen, "LOYOLA", title_size, WIDTH / 2 + outline, HEIGHT / 4 + outline)
    draw_title_outline(screen, "LOYOLA", title_size, WIDTH / 2 - outline, HEIGHT / 4 + outline)
    draw_title_outline(screen, "LOYOLA", title_size, WIDTH / 2 - outline, HEIGHT / 4 - outline)
    
    
    draw_title_outline(screen, "STAIRS", title_size, WIDTH / 2 + outline, HEIGHT / 4 + title_size - outline)
    draw_title_outline(screen, "STAIRS", title_size, WIDTH / 2 + outline, HEIGHT / 4 + title_size + outline)
    draw_title_outline(screen, "STAIRS", title_size, WIDTH / 2 - outline, HEIGHT / 4 + title_size - outline)
    draw_title_outline(screen, "STAIRS", title_size, WIDTH / 2 - outline, HEIGHT / 4 + title_size + outline)
    
                       
    draw_title(screen, "INFINITE", title_size, WIDTH / 2, HEIGHT / 4 - title_size)
    draw_title(screen, "LOYOLA", title_size, WIDTH / 2, HEIGHT / 4)
    draw_title(screen, "STAIRS", title_size, WIDTH / 2, HEIGHT / 4 + title_size)
    
    text_size = 20
    press_size = 24
    draw_text(screen, "Slash to chance direction and go up,",text_size, WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "Space to just go up",text_size, WIDTH / 2, HEIGHT / 2 + 48)
    draw_text(screen, "Press a key to begin", press_size, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting_a = True
    while waiting_a:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting_a = False
 



def show_over_screen():
    screen.blit(background, background_rect)
    
    title_size = 60
    outline = 3
    draw_title_outline(screen, "GAME", title_size, WIDTH / 2 + outline, HEIGHT / 4  -outline)
    draw_title_outline(screen, "GAME", title_size, WIDTH / 2 + outline, HEIGHT / 4  +outline)
    draw_title_outline(screen, "GAME", title_size, WIDTH / 2 - outline, HEIGHT / 4  -outline)
    draw_title_outline(screen, "GAME", title_size, WIDTH / 2 - outline, HEIGHT / 4  +outline)
    
    draw_title_outline(screen, "OVER", title_size, WIDTH / 2 + outline, HEIGHT / 4 + title_size- outline)
    draw_title_outline(screen, "OVER", title_size, WIDTH / 2 + outline, HEIGHT / 4 + title_size+ outline)
    draw_title_outline(screen, "OVER", title_size, WIDTH / 2 - outline, HEIGHT / 4 + title_size+ outline)
    draw_title_outline(screen, "OVER", title_size, WIDTH / 2 - outline, HEIGHT / 4 + title_size- outline)
    
              
    draw_title(screen, "GAME", title_size, WIDTH / 2, HEIGHT / 4)
    draw_title(screen, "OVER", title_size, WIDTH / 2, HEIGHT / 4 + title_size)
    
    
    text = "SCORE: "+str(score)
    score_size = 48
    score_outline = 2
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 4 + 3*title_size  - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 4 + 3*title_size  + score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 4 + 3*title_size  - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 4 + 3*title_size  + score_outline )
    draw_title(screen, text, score_size, WIDTH / 2 , HEIGHT / 4 + 3*title_size )
    
    
    pygame.mixer.music.stop()
    fail.stop()
    
    pygame.display.flip()
    waiting_a = True
    while waiting_a:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            

def show_success_screen():
    screen.blit(background, background_rect)
    
    text = "SUCCESS!"
    score_size = 48
    score_outline = 2
    
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 3 - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 + score_outline, HEIGHT / 3 + score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 3 - score_outline )
    draw_title_outline(screen, text, score_size, WIDTH / 2 - score_outline, HEIGHT / 3 + score_outline )
    draw_title(screen, text, score_size, WIDTH / 2 , HEIGHT / 3 )
    
    text_size = 30
    draw_text(screen, "You can study in LOYOLA!",text_size, WIDTH / 2, HEIGHT / 2 + text_size)
    
    pygame.display.flip()
    waiting_a = True
    while waiting_a:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    

### Load all game graphics
# 배경 그래픽
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
background_rect.y = -2400

# 계단 그래픽
stair_level_1 = pygame.image.load(path.join(img_dir, "stair_level_1.png")).convert()
stair_level_1.set_colorkey(BLACK)
stair_width = stair_level_1.get_rect().width
stair_height = stair_level_1.get_rect().height

stair_level_2 = pygame.image.load(path.join(img_dir, "stair_level_2.png")).convert()
stair_level_2.set_colorkey(BLACK)

stair_level_3= pygame.image.load(path.join(img_dir, "stair_level_3.png")).convert()
stair_level_3.set_colorkey(BLACK)

# 알로스 그래픽
alros_img = pygame.image.load(path.join(img_dir, "alros_start.png")).convert().set_colorkey(BLACK)

### Load all game sounds
# 배경음악
bgm = pygame.mixer.Sound(path.join(snd_dir, "bgm.mp3"))
bgm.play(-1)
walk = pygame.mixer.Sound(path.join(snd_dir, "jump_03.wav"))
fail = pygame.mixer.Sound(path.join(snd_dir, "fail.mp3"))


# 계단 그룹 생성
stairs = pygame.sprite.Group()
# 계단 위치 저장하는 리스트 생성
stairs_list = []
# 첫 번째 계단 생성
first_stair = Stair(WIDTH/2 - stair_width/2, 491)
stairs.add(first_stair)
stairs_list.append([WIDTH/2 - stair_width/2, 491])
# 나머지 계단 생성
for i in range(2,185):
    prev_stair = stairs.sprites()[-1]
    new_stair_x = prev_stair.rect.x + random.choice([-stair_width, stair_width])
    new_stair_y = prev_stair.rect.y - stair_height
    new_stair = Stair(new_stair_x, new_stair_y)
    stairs.add(new_stair)
    stairs_list.append([new_stair_x, new_stair_y])
stairs_list = np.array(stairs_list)
 
# Load all game sounds....



# Game loop
game_over_time = 0
game_start = True
game_over = False
running = True
img_order = 0
SPACE_n = 0
SLASH_n = 0
SPACE_pressed = False
SLASH_pressed = False
START = True
SLASH = False
Down = False
up_well = True
previous_score = 0

all_sprites = pygame.sprite.Group()


all_sprites.add(stairs)
hp = HP()
all_sprites.add(hp)
alros = Alros()
all_sprites.add(alros) 
        
score = 0
    
     
while running :
    if game_start:
        show_go_screen()
        game_start = False
        

        # ...
    
    # keep loop running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if not Down:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SPACE_n += 1
                    SPACE_pressed = True
                if event.key == pygame.K_SLASH:
                    SLASH_n += 1
                    SLASH_pressed = True
                    

    # 처음 시작에서 올라가는 경우
    if SPACE_n == 1:
        # 스페이스 키를 누르면
        if SPACE_pressed:
            if img_order == 0:
                alros.move(-stair_width//2, 0)
                alros.image = alros.walk_frames_l[0]
                img_order += 1
            elif img_order == 1:
                alros.move(0, -stair_height)
                alros.image = alros.walk_frames_l[1]
                img_order += 1
            elif img_order == 2:
                alros.move(-stair_width // 2, stair_height)
                alros.image = alros.walk_frames_l[2]
                background_rect.y += stair_height
                for stair in stairs:
                    stair.rect.y += stair_height
                stairs_list += (0, stair_height)
                img_order = 0
                SPACE_pressed = False
    # 게임 진행 중에 올라가는 경우
    elif SPACE_n > 1:
        # 왼쪽으로 올라가는 경우
        if SLASH_n%2==0:  
            # 스페이스 키를 누르면      
            if SPACE_pressed:
                if img_order == 0:
                    alros.move(stair_width//2,0)
                    for stair in stairs:
                        stair.rect.x += stair_width//2
                    stairs_list += (stair_width//2, 0)
                    alros.move(-stair_width//2,0)
                    alros.image = alros.walk_frames_l[0]
                    img_order +=1
                elif img_order == 1:
                    alros.move(0,-stair_height)
                    alros.image = alros.walk_frames_l[1]
                    img_order +=1
                elif img_order == 2:
                    alros.move(0,stair_height)
                    alros.image = alros.walk_frames_l[2]
                    background_rect.y += stair_height//2
                    for stair in stairs:
                        stair.rect.x += stair_width//2
                        stair.rect.y += stair_height
                    stairs_list += (stair_width//2,0)
                    stairs_list += (0,stair_height)
                    img_order = 0
                    SPACE_pressed = False
        # 오른쪽으로 올라가는 경우
        elif SLASH_n%2!=0: 
            # 스페이스 키를 누르면
            if SPACE_pressed: 
                if img_order == 0:
                    alros.move(-stair_width//2,0)
                    for stair in stairs:
                        stair.rect.x -= stair_width//2
                    stairs_list -= (stair_width//2,0)
                    alros.move(stair_width//2,0)
                    alros.image = alros.walk_frames_r[0]
                    img_order +=1
                elif img_order == 1:
                    alros.move(0,-stair_height)
                    alros.image = alros.walk_frames_r[1]
                    img_order +=1
                elif img_order == 2:
                    alros.move(0,stair_height)
                    alros.image = alros.walk_frames_r[2]
                    background_rect.y += stair_height//2
                    for stair in stairs:
                        stair.rect.x -= stair_width//2
                        stair.rect.y += stair_height
                    stairs_list -= (stair_width//2,0)
                    stairs_list += (0,stair_height)
                    img_order = 0
                    SPACE_pressed = False
    # 왼쪽으로 방향을 바꾸는 경우
    if SLASH_n%2==0:
        if SLASH_pressed:
            if img_order == 0:
                alros.move(stair_width//2,0)
                for stair in stairs:
                    stair.rect.x += stair_width//2
                stairs_list += (stair_width//2,0)
                alros.move(-stair_width//2,0)
                alros.image = alros.walk_frames_l[0]
                img_order +=1
            elif img_order == 1:
                alros.move(0,-stair_height)
                alros.image = alros.walk_frames_l[1]
                img_order +=1
            elif img_order == 2:
                alros.move(0,stair_height)
                alros.image = alros.walk_frames_l[2]
                background_rect.y += stair_height//2
                for stair in stairs:
                    stair.rect.x += stair_width//2
                    stair.rect.y += stair_height
                stairs_list += (stair_width//2,0)
                stairs_list += (0,stair_height)
                img_order = 0
                SLASH_pressed = False
    # 오른쪽으로 방향을 바꾸는 경우            
    elif SLASH_n%2!=0:
        if SLASH_pressed:
            if img_order == 0:
                alros.move(-stair_width//2,0)
                for stair in stairs:
                    stair.rect.x -= stair_width//2
                stairs_list -= (stair_width//2,0)
                alros.move(stair_width//2,0)
                alros.image = alros.walk_frames_r[0]
                img_order +=1
            elif img_order == 1:
                alros.move(0,-stair_height)
                alros.image = alros.walk_frames_r[1]
                img_order +=1
            elif img_order == 2:
                alros.move(0, stair_height)
                alros.image = alros.walk_frames_r[2]
                background_rect.y += stair_height//2
                for stair in stairs:
                    stair.rect.x -= stair_width//2
                    stair.rect.y += stair_height
                stairs_list -= (stair_width//2,0)
                stairs_list += (0,stair_height)
                img_order = 0
                SLASH_pressed = False    
            
    # 계단 위에 잘 올라가는지 체크
    i = SPACE_n+SLASH_n-1
    if (i>=0 and (stairs_list[i][0] > alros.rect.x+alros.rect.width or stairs_list[i][0]+stair_width < alros.rect.x)) or (hp.health_width <= 0):
        up_well = False
        if alros.image == alros.walk_frames_l[2]:
            alros.image = alros.down_l
            alros.down_time = pygame.time.get_ticks()
            
        elif alros.image == alros.walk_frames_r[2]:
            alros.image = alros.down_r 
            alros.down_time = pygame.time.get_ticks()
            
        Down = True   
        
    else: # 잘 올라가면
        up_well = True
        score = i + 1

        
    # 알로스가 계단애 잘 올라가는지 체크 
    for alros in all_sprites:
        if isinstance(alros, Alros):
            alros.update()
            
            # Check if Alros is not doing anything
            if not (SPACE_pressed or SLASH_pressed):
                decrease_rate = score * 0.1
                if decrease_rate != 0:
                    hp.decrease_width(decrease_rate)  # Decrease health gradually
            
    # 떨어지는 경우
    if Down:
        nowTime = pygame.time.get_ticks()
        fail.play(loops = 1, maxtime = 2600)
        # Wait for 1000 milliseconds (1 second) after changing to down image
        if nowTime - alros.down_time > 3000:
            alros.move(0, -10)# Move Alros down
            if alros.rect.y > HEIGHT: 
                Down = False
                game_over_time = pygame.time.get_ticks()
                game_over = True
        
    # If Alros is directly above a stair, perform the necessary actions
    if up_well:
        # Gradual decrease of the health bar width
        hp.update_width(score)
        
        if score > previous_score:
            hp.reset_width()
            walk.play()
            previous_score = score
        
        
        

    
    if game_over:
        show_over_screen()
        bgm.stop()
        game_over= False
        Down = False
        
    if score >= 184:
        show_success_screen()
        

   
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    # all sprites draw
    all_sprites.draw(screen)
    
    # Draw the health bar at a fixed position
    hp.hp_ratio = max(0, hp.current_width / hp.max_width)
    hp.health_width = int(hp_bar_width * hp.hp_ratio)
    health_bar_surface = pygame.Surface((hp.health_width, hp_bar_height))
    health_bar_surface.fill(YELLOW)

    screen.blit(health_bar_surface, (60, 62))
    
    draw_score(score)

    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
