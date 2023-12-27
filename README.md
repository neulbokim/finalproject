# Infinite Loyola Stairs
수많은 계단을 올라가야 도착할 수 있는 서강대학교 로욜라도서관!
<엔플라이 스튜디오>의 <<무한의 계단>> 게임을 모티브로 하여서,
서강대학교 후문 쪽 J관에서부터 D관을 거쳐 로욜라 도서관까지 가는 길을 그려냈습니다.
과연 알로스는 로욜라 도서관까지 성공적으로 도착해 공부하게 될 수 있을까요?!

## 목차
- [개요] (#개요)


## 개요
- 프로젝트 이름: Infinite Loyola Stairs
- 프로젝트 지속 기간: 2023.11.17 ~ 2023.12.27
- 개발 언어: Python
- 제작자: 서강대학교 국어국문학과 20220042 김현서

## 게임 설명



# 1. class Alros
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
