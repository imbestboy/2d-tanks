import pygame
import random
import customtkinter

import config
import main_menu
import functions
from tank import Tank


def start_game(main_menu_window: customtkinter.CTk) -> None:
    """start_game close main menu and start the game

    Arguments:
        main_menu_window {customtkinter.CTk} -- tkinter main menu window
    """
    # -- loading settings
    dark_mode = True if main_menu_window["bg"] == "gray14" else False
    game_background_color = main_menu_window["bg"]

    # -- close main menu window
    main_menu_window.destroy()

    # -- pygame setup
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    is_game_over = False
    font = pygame.font.SysFont("Helvetica", 20)

    # -- game components setup
    wall_color = "gray92" if dark_mode else "gray14"
    map_name = "map_1"
    walls, tanks = functions.map_reader(map_name)
    tank_a, tank_b = tanks
    tank_a["x"] = (tank_a["x"] * config.CELL_X) - config.CELL_X
    tank_a["x"] += config.CELL_X // 3
    tank_a["y"] = (tank_a["y"] * config.CELL_Y) - config.CELL_Y
    tank_a["y"] += config.CELL_Y // 3
    tank_b["x"] = (tank_b["x"] * config.CELL_X) - config.CELL_X
    tank_b["x"] += config.CELL_X // 3
    tank_b["y"] = (tank_b["y"] * config.CELL_Y) - config.CELL_Y
    tank_b["y"] += config.CELL_Y // 3
    tank_image_path = "tank_images/dark.png" if dark_mode else "tank_images/light.png"
    tank_a = Tank(tank_image_path, (tank_a["x"], tank_a["y"]), 0, "A")
    tank_b = Tank(tank_image_path, (tank_b["x"], tank_b["y"]), 270, "B")
    tanks = [tank_a, tank_b]

    # -- game window size
    screen = pygame.display.set_mode(
        (config.GAME_SCREEN_WIDTH, config.GAME_SCREEN_HEIGHT)
    )

    # -- game loop
    while is_running:
        for event in pygame.event.get():
            # -- pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                is_running = False
                # -- run main menu window again
                main_menu.start_main_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SLASH:
                    tank_a.shoot(screen, dark_mode)
                if event.key == pygame.K_c:
                    tank_b.shoot(screen, dark_mode)

        screen.fill(game_background_color)

        # -- get which key pressed by user (pygame.K_LEFT => left arrow and pygame.K_RIGHT => right arrow)
        tank_a, tank_b = tanks
        keys = pygame.key.get_pressed()
        walls_rect = [
            functions.draw_wall(**wall, screen=screen, color=wall_color)
            for wall in walls
        ]
        for tank in tanks:
            for bullet in tank.bullets:
                if bullet.check_die():
                    tank.bullet_die()
                else:
                    bullet.move_forward()
                    bullet.draw_and_check_hit_wall(screen, walls_rect)
                    if bullet.check_hit_tank(screen, tanks, dark_mode):
                        tank.bullets.remove(bullet)

            tank_rect = tank.draw(screen, dark_mode)
            if tank_rect.collidelistall(walls_rect):
                tank.hit_wall()

        if keys[pygame.K_LEFT]:
            tank_a.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            tank_a.rotate(right=True)
        if keys[pygame.K_UP]:
            tank_a.move_forward()
        if keys[pygame.K_DOWN]:
            tank_a.move_backward()

        if keys[pygame.K_w]:
            tank_b.move_forward()
        if keys[pygame.K_s]:
            tank_b.move_backward()
        if keys[pygame.K_a]:
            tank_b.rotate(left=True)
        if keys[pygame.K_d]:
            tank_b.rotate(right=True)

        # -- update() the display to put your work on screen
        pygame.display.update()

        # -- limits FPS to 60
        clock.tick(60)

    pygame.quit()
