import pygame

MOVE_SPEED = 7


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x_velocity = 0
        self.startX = x
        self.startY = y
        self.last_left = False
        self.last_right = False
        self.image = pygame.transform.scale(pygame.image.load('images/tank.png'), (418, 108))
        self.image_left = pygame.transform.flip(self.image, False, False)
        self.image_right = pygame.transform.flip(self.image, True, False)
        self.rect = pygame.Rect(x, y, self.image.get_size()[0], self.image.get_size()[1])

    def update(self, left, right):
        if left:
            self.x_velocity = -MOVE_SPEED
            self.image = self.image_left

        if right:
            self.x_velocity = MOVE_SPEED
            self.image = self.image_right

        if not (left or right):
            self.x_velocity = 0

        self.rect.x += self.x_velocity
        if self.rect.x < -100:
            self.rect.x = -100
        if self.rect.x > 1100:
            self.rect.x = 1100

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
background_image = pygame.image.load('images/level1/background.png')
ground = pygame.transform.scale(pygame.image.load('images/level1/ground.png'), (384, 114))
tank = Player(700, 605)
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

    screen.blit(background_image, (0, 0))
    for _ in range(5):
        screen.blit(ground, (0 + _ * 383, 700))

    tank.update(left, right)
    tank.draw(screen)

    pygame.display.update()
    clock.tick(60)
