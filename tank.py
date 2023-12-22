import pygame
import math

import config
import functions


class Tank:
    def __init__(self, image_path: str, start_position: tuple, angle: int, name: str):
        self.img = pygame.image.load(image_path)
        self.speed = config.TANKS_SPEED
        self.vel = 0
        self.rotation_vel = config.TANKS_ROTATION_SPEED
        self.angle = angle
        self.x, self.y = start_position
        self.name = name

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen, dark_mode):
        new_rect = functions.blit_rotate_center(
            screen, self.img, (self.x, self.y), self.angle
        )
        font = pygame.font.SysFont("Helvetica", 12)
        text_color = "gray92" if dark_mode else "gray14"
        tank_name_text = font.render(self.name, True, text_color)
        tank_name_x = self.img.get_rect().centerx + self.x
        tank_name_y = self.img.get_rect().centery + self.y
        screen.blit(
            tank_name_text,
            (
                tank_name_x - tank_name_text.get_width() // 2,
                tank_name_y - tank_name_text.get_height() // 2,
            ),
        )
        return new_rect

    def move_forward(self):
        self.vel = self.speed
        self.move()

    def move_backward(self):
        self.vel = -self.speed
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def hit_wall(self):
        self.vel = -3 * self.vel
        self.move()
