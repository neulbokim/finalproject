import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 400
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

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

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



# alors 클래스
class Alros(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walk_frames_l = {}
        self.walk_frames_r = {}

        self.load_images()
        self.image_orig = alros_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH-self.rect.width)//2 + self.rect.width
        self.rect.y = 400

        self.direction = 'left'
        self.direction_prev = self.direction
        self.foot = 'left_left'
        self.foot_prev = self.foot
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

    
    def load_images(self):
        # 왼쪽 방향 이미지들
        self.walk_frames_l['left_left'] = []
        self.walk_frames_l['left_right'] = []
        for i in range(1, 4):
            filename = 'alros_left_left_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.walk_frames_l['left_left'].append(img)

            filename = 'alros_left_right_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.walk_frames_l['left_right'].append(img)

        # 오른쪽 방향 이미지들
        self.walk_frames_r['right_left'] = []
        self.walk_frames_r['right_right'] = []
        for i in range(1, 4):
            filename = 'alros_right_left_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.walk_frames_r['right_left'].append(img)

            filename = 'alros_right_right_{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.walk_frames_r['right_right'].append(img)


    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:  # 애니메이션 속도 조절 (150 밀리초마다 업데이트)
            self.last_update = now
            keys = list(self.walk_frames_l.keys())
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames_l[keys[0]])
            # 애니메이션 방향에 따라 이미지 설정
            if self.direction == 'left':
                self.image = self.walk_frames_l['left_left'][self.frame_index]
            else:
                self.image = self.walk_frames_r['right_left'][self.frame_index]
    def move(self, x, y):
        if self.direction == 'left':
            if self.direction_prev == 'left':
                self.rect.x += x
                self.rect.y -= y
            elif self.direction_prev == 'right':
                self.rect.x -= x
                self.rect.y -= y
        if self.direction == 'right':
            if self.direction_prev == 'left':
                self.rect.x -= x
                self.rect.y -= y
            elif self.direction_prev == 'right':
                self.rect.x += x
                self.rect.y -= y
            
    

# 계단 클래스
class Stair(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = stair_level_1
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def move(self, x, y):
        if self.direction == 'left':
            if self.direction_prev == 'left':
                self.rect.x += x
                self.rect.y -= y
            elif self.direction_prev == 'right':
                self.rect.x -= x
                self.rect.y -= y
        if self.direction == 'right':
            if self.direction_prev == 'left':
                self.rect.x -= x
                self.rect.y -= y
            elif self.direction_prev == 'right':
                self.rect.x += x
                self.rect.y -= y
    
    




def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "INFINITE", 48, WIDTH / 2, HEIGHT / 4 - 48)
    draw_text(screen, "LOYOLA", 48, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "STAIRS", 48, WIDTH / 2, HEIGHT / 4 + 48)
    draw_text(screen, "Slash to chance direction and go up,",16, WIDTH / 2, HEIGHT / 2 - 8)
    draw_text(screen, "Space to just go up",16, WIDTH / 2, HEIGHT / 2 + 8)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False




# Load all game graphics

# 배경 그래픽
background = pygame.image.load(path.join(img_dir, "Manresa.webp")).convert()
background_rect = background.get_rect()

# 계단 그래픽
stair_level_1 = pygame.image.load(path.join(img_dir, "stair_level_1.png")).convert()
stair_level_1.set_colorkey(BLACK)
stair_width = stair_level_1.get_rect().width
stair_height = stair_level_1.get_rect().height

# 알로스 그래픽
alros_img = pygame.image.load(path.join(img_dir, "alros_start.png")).convert()
alros_anim = {}
alros_anim['left_left'] = []
alros_anim['left_right'] = []
alros_anim['right_left'] = []
alros_anim['right_right'] = []
dire = ['left', 'right']
for i in range(1,4):
    for d in dire:
        for foot in dire:
            filename = 'alros_{}_{}_{}.png'.format(d, foot, i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            alros_anim['{}_{}'.format(d, foot)].append(img)



# 계단 그룹 생성
stairs = pygame.sprite.Group()
# 첫 번째 계단 생성
first_stair = Stair(WIDTH/2 - stair_width/2, 491)
stairs.add(first_stair)
# 나머지 계단 생성
for i in range(2,30):
    prev_stair = stairs.sprites()[-1]
    new_stair = Stair(random.choice([-stair_width, stair_width])+prev_stair.rect.x, 
                      prev_stair.rect.y - stair_height)
    stairs.add(new_stair)


# Load all game sounds....



# Game loop
game_over = True
running = True
while running :
    if game_over:
        show_go_screen()
        game_over = False

        # ...
        all_sprites = pygame.sprite.Group()

        alros = Alros()

        all_sprites.add(stairs)
        all_sprites.add(alros)
        score = 0
    
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                alros.direction_prev = alros.direction
                # 스페이스 키를 눌렀을 때 계단과 배경 이동
                if alros.direction == 'left':
                    if alros.direction_prev == 'left':
                        for stair in stairs:
                            stair.rect.x += stair_width
                            stair.rect.y += stair_height
                        background_rect.x += stair_width
                        background_rect.y += stair_height
                        alros.move(-stair_width//2, 0)
                        alros.update_animation()
                    
                elif alros.direction == 'right':
                    if alros.direction_prev == 'right':
                        for stair in stairs:
                            stair.rect.x -= stair_width
                            stair.rect.y += stair_height
                        background_rect.x -= stair_width
                        background_rect.y += stair_height
                        alros.move(stair_width//2, 0)
                        alros.update_animation()
                
            elif event.key == pygame.K_SLASH:
                # 슬래시 키를 눌렀을 때 방향 전환하고 올라감
                alros.direction_prev = alros.direction
                alros.direction = 'left' if alros.direction == 'right' else 'right'
                if alros.direction == 'left':
                    if alros.direction_prev == 'right':
                        for stair in stairs:
                            stair.rect.x += stair_width
                            stair.rect.y += stair_height
                        background_rect.x += stair_width
                        background_rect.y += stair_height
                        alros.move(-stair_width//2, 0)
                        alros.update_animation()
                    
                elif alros.direction == 'right':
                    if alros.direction_prev == 'left':
                        for stair in stairs:
                            stair.rect.x -= stair_width
                            stair.rect.y += stair_height
                        background_rect.x -= stair_width
                        background_rect.y += stair_height
                        alros.move(stair_width//2, 0)
                        alros.update_animation()


    
    # Update...

    # player가 계단 올라가는지 체크하기 ...

    # if the player died ... game_over = True

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    # all sprites draw
    all_sprites.draw(screen)
    # draw text
    # draw shield bar
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
