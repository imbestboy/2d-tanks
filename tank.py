import pygame
import math
import time

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
        self.bullets = []

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

    def shoot(self, screen: pygame.surface.Surface, is_dark_mode: bool):
        if len(self.bullets) < config.TOTAL_BULLET_COUNT:
            bullet_image_path = (
                "bullets_image/dark.png" if is_dark_mode else "bullets_image/light.png"
            )
            tank_rect = self.draw(screen, is_dark_mode)
            new_bullet = Bullet(
                bullet_image_path, (tank_rect.centerx, tank_rect.centery), self.angle
            )
            self.bullets.append(new_bullet)

    def bullet_die(self):
        self.bullets.pop(0)


class Bullet:
    def __init__(self, image_path: str, shoot_position: tuple, angle: int):
        self.img = pygame.image.load(image_path)
        self.speed = config.TANKS_SPEED
        self.vel = self.speed
        self.angle = angle
        self.x, self.y = shoot_position
        self.hit_count = 0
        self.alive_time = config.BULLET_ALIVE_TIME
        self.birth_time = time.time()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def move_forward(self):
        self.vel = self.speed
        self.move()

    def hit_wall(self):
        if self.hit_wall >= 3:
            pass
        self.vel = -3 * self.vel
        self.hit_count += 1
        self.move()

    def draw(self, screen):
        bullet_new_rect = functions.blit_rotate_center(
            screen, self.img, (self.x, self.y), self.angle
        )
        return bullet_new_rect

    def check_die(self):
        return time.time() - self.birth_time >= self.alive_time
