import pygame
from settings import *


class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 15
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - self.width // 2, SCREEN_HEIGHT - 40, self.width, self.height)
        self.speed = 8

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect, border_radius=5)


class Ball:
    def __init__(self):
        self.radius = 10
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.dx = 5
        self.dy = -5
        self.active = False

    def move(self, paddle):
        if not self.active:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.active = True
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.dx *= -1

            if self.rect.top <= 0:
                self.dy *= -1

    def draw(self, surface, color):
        pygame.draw.ellipse(surface, color, self.rect)

class Block:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (30, 30, 30), self.rect, 1, border_radius=4)


def create_blocks(rows, cols):
    blocks = []
    gap = 5

    block_width = (SCREEN_WIDTH - (cols + 1) * gap) // cols
    block_height = 30

    for row in range(rows):
        color = RAINBOW_COLORS[row % len(RAINBOW_COLORS)]

        for col in range(cols):
            x = gap + col * (block_width + gap)
            y = gap + row * (block_height + gap) + 60
            blocks.append(Block(x, y, block_width, block_height, color))

    return blocks