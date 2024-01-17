import pygame
import random
import math
from pygame import mixer

MOVE_SPEED = 7
Y1_PLANE = 50
Y2_PLANE = 400


def distance(sprite1, sprite2):
    return math.sqrt((sprite1.rect.x - sprite2.rect.x)**2 + (sprite1.rect.y - sprite2.rect.y)**2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.angle = angle
        self.x = x
        self.y = y
        self.speed_x = self.speed * math.cos(angle * 0.01745)
        self.speed_y = self.speed * math.sin(angle * 0.01745)
        self.bullet = pygame.image.load('images/bullet.png')
        self.rect = self.bullet.get_rect(center=(x, y))
        self.rotate()
        self.r.x += self.speed_x * 11
        self.r.y -= self.speed_y * 11

        self.F = False
        self.frames = []
        self.cut_sheet(pygame.image.load('images/Textures/Level/Animation/effect_sprite.png'), 3, 1)
        self.cur_frame = 0
        self.effect = self.frames[self.cur_frame]
        self.rect_effect = self.effect.get_rect(center=(x, y))

        self.mask = pygame.mask.from_surface(self.bullet)

    def cut_sheet(self, sheet, columns, rows):
        self.rect_effect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect_effect.w * i, self.rect_effect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect_effect.size)))

    def rotate(self):
        self.surf, self.r = self.rot_center(self.bullet, self.rect, self.angle)

    def rotate1(self):
        self.surf1, self.r1 = self.rot_center(self.effect, self.rect_effect, self.angle)

    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def update(self, screen, planes):

        try:
            self.cur_frame = self.cur_frame + 1
            self.effect = self.frames[self.cur_frame]
            self.rotate1()
            self.r1.x += self.speed_x * 4
            self.r1.y -= self.speed_y * 4
            screen.blit(self.surf1, self.r1)
        except:
            if not self.F:
                self.F = True
                del self.effect

        self.r.x += self.speed_x
        self.r.y -= self.speed_y
        screen.blit(self.surf, self.r)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_r, sheet_l, columns):
        pygame.sprite.Sprite.__init__(self)
        self.start_reload = None
        self.bullets_count = 30
        self.CoolDown = 400
        self.reload_time = 4000
        self.is_reloaded = True
        self.last_shot = None

        self.x_velocity = 0
        self.startX = x
        self.startY = y
        self.angle = None
        self.bullets = []
        self.last_left = False
        self.last_right = False

        self.frames_r = []
        self.frames_l = []
        self.rect_tank = pygame.Rect(0, 0, sheet_r.get_width() // columns,
                                sheet_r.get_height())
        self.cut_sheet_r(sheet_r, columns, 1)
        self.cut_sheet_l(sheet_l, columns, 1)
        self.cur_frame = 0
        self.tank_right = self.frames_r[self.cur_frame]
        self.tank = self.frames_r[self.cur_frame]
        self.tank_left = self.frames_l[self.cur_frame]
        self.rect_tank = self.rect_tank.move(x, y)

        self.gun = pygame.transform.scale(pygame.image.load('images/gun.png'), (225, 27))
        self.rect_gun = self.gun.get_rect(center=(self.rect_tank.x - 26, self.rect_tank.y + 40))

        self.shoot = mixer.Sound('images/Music/tank/shoot.mp3')
        self.reloading = mixer.Sound('images/Music/tank/reloading2.wav')
        self.popal = mixer.Sound('images/Music/tank/est-probitie.mp3')
        self.ubit = mixer.Sound('images/Music/tank/minecraft-death-sound.mp3')
        self.shoot.set_volume(0.2)
        self.popal.set_volume(0.4)
        self.ubit.set_volume(0.4)

    def cut_sheet_r(self, sheet, columns, rows):
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect_tank.w * i, self.rect_tank.h * j)
                self.frames_r.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect_tank.size)))

    def cut_sheet_l(self, sheet, columns, rows):
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect_tank.w * i, self.rect_tank.h * j)
                self.frames_l.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect_tank.size)))

    def update(self, left, right, is_fire, planes):

        self.cur_frame = (self.cur_frame + 1) % len(self.frames_r)

        if left:
            self.x_velocity = -MOVE_SPEED
            self.tank = self.frames_l[self.cur_frame]

        if right:
            self.x_velocity = MOVE_SPEED
            self.tank = self.frames_r[self.cur_frame]

        if not (left or right):
            self.x_velocity = 0

        self.rect_tank.x += self.x_velocity
        if self.rect_tank.x < 0:
            self.rect_tank.x = 0
        if self.rect_tank.x > 1400-172.5:
            self.rect_tank.x = 1400-172.5

        self.rotate()
        self.rect_gun.x = self.rect_tank.x - 26

        if self.start_reload:
            if pygame.time.get_ticks() - self.start_reload > self.reload_time and not self.is_reloaded:
                self.is_reloaded = True
                self.bullets_count = 30

        if is_fire:
            if not self.last_shot:
                self.shoot.play()
                self.last_shot = pygame.time.get_ticks()
                new_bullet = Bullet(self.rect_gun.x + self.gun.get_size()[0] // 2,
                                    self.rect_gun.y - self.gun.get_size()[1] // 2 + 24, self.angle)
                self.bullets.append(new_bullet)
                self.bullets_count -= 1
            else:
                if pygame.time.get_ticks() - self.last_shot > self.CoolDown and self.is_reloaded:
                    self.shoot.play()
                    self.last_shot = pygame.time.get_ticks()
                    new_bullet = Bullet(self.rect_gun.x + self.gun.get_size()[0] // 2,
                                        self.rect_gun.y - self.gun.get_size()[1] // 2 + 24, self.angle)
                    self.bullets.append(new_bullet)
                    self.bullets_count -= 1
                    if self.bullets_count <= 0:
                        print('play')
                        self.reloading.play()
                        print('dfgjkh')
                        self.is_reloaded = False
                        self.start_reload = pygame.time.get_ticks()
        to_del = []
        to_del_1 = []
        if self.bullets:
            for bullet in self.bullets:
                bullet.update(screen, planes)
                for plane in planes:
                    if bullet.r.colliderect(plane.rect):

                        plane.get_damage(1)
                        if plane.get_HP() <= 0:
                            self.ubit.play()
                            to_del_1.append(plane)
                        else:
                            self.popal.play()
                        to_del.append(bullet)
                if bullet.x > 1450 or bullet.x < -50 or bullet.y < -50 or bullet.y > 850:
                    to_del.append(bullet)
        for bullet in to_del:
            self.bullets.remove(bullet)
            del bullet
        for plane in to_del_1:
            planes.remove(plane)
            del plane

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect_gun.x + self.gun.get_size()[0] // 2), mouse_y - (self.rect_gun.y + self.gun.get_size()[1] // 2)
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if -90 < self.angle < 0:
            self.angle = 0
        if -179 < self.angle <= -90:
            self.angle = 180
        self.surf, self.r = self.rot_center(self.gun, self.rect_gun, self.angle)

    def rot_center(self, image, rect_gun, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect_gun.center)
        return rot_image, rot_rect

    def draw(self, screen):
        screen.blit(self.tank, (self.rect_tank.x, self.rect_tank.y))
        screen.blit(self.surf, self.r)


class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.HP = 3
        self.planes = [
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/a7.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/a7_2.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/drone.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/f16.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/j20.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/j20_2.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/mig21.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/su25.png'), (120, 53)),
            pygame.transform.scale(pygame.image.load('images/Textures/Planes/su25_2.png'), (120, 53)),
        ]
        self.image = random.choice(self.planes)
        self.rect = pygame.Rect(x, y, self.image.get_size()[0], self.image.get_size()[1])
        self.x_velocity = 5

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.x_velocity

    def get_damage(self, HP):
        self.HP -= HP

    def get_HP(self):
        return self.HP

pygame.init()
mixer.music.load("images/Music/background/1.MainTheme-320bitchosic.com.mp3")
mixer.music.set_volume(0.05)
mixer.music.play(-1)
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
background_image = pygame.image.load('images/level1/background.png')
ground = pygame.transform.scale(pygame.image.load('images/level1/ground.png'), (384, 114))
tank = Player(700, 625, pygame.transform.scale(pygame.image.load('images/tank.png'), (708, 90)), pygame.transform.scale(pygame.image.load('images/tank_left.png'), (708, 90)), 4)
cursor_img = pygame.image.load('images/crosshair.png')
pygame.mouse.set_visible(False)
cursor_img_rect = cursor_img.get_rect()
planes = pygame.sprite.Group()
left = right = False
is_fire = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            right = True
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            left = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_fire = True
        if event.type == pygame.MOUSEBUTTONUP:
            is_fire = False

    # draw all
    screen.blit(background_image, (0, 0))
    for _ in range(5):
        screen.blit(ground, (0 + _ * 383, 700))

    cursor_img_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_img, cursor_img_rect)

    tank.update(left, right, is_fire, planes)
    tank.draw(screen)

    planes.update()
    planes.draw(screen)

    if random.randint(0, 100) < 3:
        new_plane = Plane(-50, random.randint(Y1_PLANE, Y2_PLANE))

        too_close = any(distance(new_plane, existing_plane) < 200 for existing_plane in planes)
        if not too_close:
            planes.add(new_plane)
    to_del = []
    for i in planes:
        if i.rect.x > 1400:
            to_del.append(i)
    for i in range(len(to_del)):
        planes.remove(to_del[i])
        del to_del[i]

    pygame.display.update()
    clock.tick(60)
