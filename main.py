import time
import pygame
import math

MOVE_SPEED = 7


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x_velocity = 0
        self.startX = x
        self.startY = y
        self.last_left = False
        self.last_right = False
        self.tank = pygame.transform.scale(pygame.image.load('images/tank.png'), (172.5, 90))
        self.gun = pygame.transform.scale(pygame.image.load('images/gun.png'), (225, 27))
        self.tank_left = pygame.transform.flip(self.tank, False, False)
        self.tank_right = pygame.transform.flip(self.tank, True, False)
        self.rect_tank = pygame.Rect(x, y, self.tank.get_size()[0], self.tank.get_size()[1])
        self.rect_gun = self.gun.get_rect(center=(self.rect_tank.x-26, self.rect_tank.y+40))

    def update(self, left, right):
        if left:
            self.x_velocity = -MOVE_SPEED
            self.tank = self.tank_left

        if right:
            self.x_velocity = MOVE_SPEED
            self.tank = self.tank_right

        if not (left or right):
            self.x_velocity = 0

        self.rect_tank.x += self.x_velocity
        if self.rect_tank.x < 0:
            self.rect_tank.x = 0
        if self.rect_tank.x > 1400-172.5:
            self.rect_tank.x = 1400-172.5

        self.rotate()

        self.rect_gun.x = self.rect_tank.x-26

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect_gun.x - 113, mouse_y - self.rect_gun.y - 14
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.surf, self.r = self.rot_center(self.gun, self.rect_gun, angle)

    def rot_center(self, image, rect_gun, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect_gun.center)
        return rot_image, rot_rect

    def draw(self, screen):
        screen.blit(self.tank, (self.rect_tank.x, self.rect_tank.y))
        screen.blit(self.surf, self.r)


pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
background_image = pygame.image.load('images/level1/background.png')
ground = pygame.transform.scale(pygame.image.load('images/level1/ground.png'), (384, 114))
cursor_img = pygame.image.load('images/crosshair.png')
tank = Player(700, 625)
left = right = False
pygame.mouse.set_visible(False)
cursor_img_rect = cursor_img.get_rect()

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

    # draw all
    screen.blit(background_image, (0, 0))
    for _ in range(5):
        screen.blit(ground, (0 + _ * 383, 700))

    tank.update(left, right)
    tank.draw(screen)

    cursor_img_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_img, cursor_img_rect)

    pygame.display.update()
    clock.tick(60)
