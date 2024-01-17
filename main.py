import pygame
import random
import math

MOVE_SPEED = 7
Y1_PLANE = 50
Y2_PLANE = 400


def distance(sprite1, sprite2):
    return math.sqrt((sprite1.rect.x - sprite2.rect.x)**2 + (sprite1.rect.y - sprite2.rect.y)**2)


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
        self.rect_gun = self.gun.get_rect(center=(self.rect_tank.x - 26, self.rect_tank.y + 40))

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
        self.rect_gun.x = self.rect_tank.x - 26

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


class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
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

    def update(self):
        self.rect.x += self.x_velocity


pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
background_image = pygame.image.load('images/level1/background.png')
ground = pygame.transform.scale(pygame.image.load('images/level1/ground.png'), (384, 114))
tank = Player(700, 625)
cursor_img = pygame.image.load('images/crosshair.png')
pygame.mouse.set_visible(False)
cursor_img_rect = cursor_img.get_rect()
planes = pygame.sprite.Group()
left = right = False
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

    cursor_img_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_img, cursor_img_rect)

    tank.update(left, right)
    tank.draw(screen)

    planes.update()
    planes.draw(screen)

    # Spawn a new plane randomly away from existing planes
    if random.randint(0, 100) < 3:  # Adjust the probability as needed
        new_plane = Plane(-50, random.randint(Y1_PLANE, Y2_PLANE))

        # Ensure new plane is not too close to existing planes
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
