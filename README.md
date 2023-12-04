# final project

# class Alros
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
        self.foot = 'left_left'
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
        self.rect.x += x
        self.rect.y -= y
# Stair class
