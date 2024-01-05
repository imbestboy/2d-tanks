import pygame
import random
import customtkinter

import config
import main_menu
import functions
from tank import Tank


def start_game(
    main_menu_window: customtkinter.CTk,
    winner_score: customtkinter.IntVar,
    bullet_speed: customtkinter.IntVar,
    map_name: customtkinter.StringVar,
) -> None:
    """start_game close main menu and start the game

    Arguments:
        main_menu_window {customtkinter.CTk} -- tkinter main menu window
        winner_score {customtkinter.IntVar} -- tkinter integer variable
        bullet_speed {customtkinter.IntVar} -- tkinter integer variable
        map_name {customtkinter.StringVar} -- tkinter string variable
    """
    # -- loading settings
    dark_mode = True if main_menu_window["bg"] == "gray14" else False
    game_background_color = main_menu_window["bg"]
    winner_score = winner_score.get()
    bullet_speed = bullet_speed.get()
    map_name = map_name.get()

    # -- close main menu window
    main_menu_window.destroy()

    # -- pygame setup
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    is_game_over = False
    is_pause = False
    winner_font = pygame.font.SysFont("Helvetica", 50)
    winner_name = None
    score_font = pygame.font.SysFont("Helvetica", 30)
    pygame.display.set_caption("2D tanks")

    # -- game components setup
    wall_color = "gray92" if dark_mode else "gray14"
    walls, tanks, respawn_locations = functions.map_reader(map_name)
    for location in tanks + respawn_locations:
        location["x"], location["y"] = functions.convert_location_to_pixel(**location)
    tank_a, tank_b = tanks
    tank_image_path = "tank_images/dark.png" if dark_mode else "tank_images/light.png"
    tank_a = Tank(
        tank_image_path, (tank_a["x"], tank_a["y"]), 0, "A", config.CELL_Y // 3
    )
    tank_b = Tank(tank_image_path, (tank_b["x"], tank_b["y"]), 270, "B", config.CELL_Y)
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
                theme = "dark" if dark_mode else "light"
                main_menu.start_main_menu(theme, winner_score, bullet_speed, map_name)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SLASH:
                    tank_a.shoot(screen, dark_mode, bullet_speed)
                if event.key == pygame.K_c:
                    tank_b.shoot(screen, dark_mode, bullet_speed)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    is_pause = not is_pause
                if event.key == pygame.K_e and is_pause:
                    is_running = False
                    theme = "dark" if dark_mode else "light"
                    main_menu.start_main_menu(
                        theme, winner_score, bullet_speed, map_name
                    )

        screen.fill(game_background_color)

        # -- get which key pressed by user (pygame.K_LEFT => left arrow and pygame.K_RIGHT => right arrow)
        tank_a, tank_b = tanks
        keys = pygame.key.get_pressed()
        walls_rect = [
            functions.draw_wall(**wall, screen=screen, color=wall_color)
            for wall in walls
        ]
        for tank in tanks:
            tank_score = score_font.render(
                f"{tank.name} : {tank.score}", True, wall_color
            )
            screen.blit(
                tank_score,
                (
                    config.CELL_X * 8
                    + (config.CELL_X // 2 - tank_score.get_width() // 2),
                    tank.score_height,
                ),
            )
            for bullet in tank.bullets:
                if bullet.check_die():
                    tank.bullet_die()
                else:
                    if not is_pause:
                        bullet.move_forward()
                    bullet.draw_and_check_hit_wall(
                        screen, walls_rect, game_background_color
                    )
                    if hit_tank := bullet.check_hit_tank(screen, tanks, dark_mode):
                        tank.bullets.remove(bullet)
                        random_respawn = random.choice(respawn_locations)
                        hit_tank.x, hit_tank.y = (
                            random_respawn["x"],
                            random_respawn["y"],
                        )
                        tanks_copy = tanks[:]
                        tanks_copy.remove(hit_tank)
                        tanks_copy[0].score += 1
                        if tanks_copy[0].score >= winner_score:
                            winner_name = "A" if hit_tank.name == "B" else "B"
                            is_game_over = True

            tank_rect = tank.draw(screen, dark_mode)
            if tank_rect.collidelistall(walls_rect):
                tank.hit_wall()
        if is_pause:
            screen.fill(game_background_color)
            pause_text = winner_font.render("GAME PAUSED", True, wall_color)
            pause_detail_text = score_font.render(
                "Press E to exit game", True, wall_color
            )
            pause_x = (config.GAME_SCREEN_WIDTH // 2) - (pause_text.get_width() // 2)
            pause_y = (config.GAME_SCREEN_HEIGHT // 2) - (pause_text.get_height() // 2)
            screen.blit(
                pause_detail_text,
                (
                    pause_x + (pause_text.get_width() // 7),
                    (pause_y + (pause_text.get_height() * 1.7)),
                ),
            )
            screen.blit(pause_text, (pause_x, pause_y))
            pause_rect = pygame.Rect(
                pause_x - 20,
                pause_y - 20,
                pause_text.get_width() + 40,
                pause_text.get_height() + 40,
            )
            pygame.draw.rect(screen, wall_color, pause_rect, 3)
        else:
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

        if is_game_over:
            screen.fill(game_background_color)
            winner_name_text = winner_font.render(
                winner_name + " WIN", True, wall_color
            )
            winner_name_x = (config.GAME_SCREEN_WIDTH // 2) - (
                winner_name_text.get_width() // 2
            )
            winner_name_y = (config.GAME_SCREEN_HEIGHT // 2) - (
                winner_name_text.get_height() // 2
            )
            screen.blit(winner_name_text, (winner_name_x, winner_name_y))
            winner_rect = pygame.Rect(
                winner_name_x - 20,
                winner_name_y - 20,
                winner_name_text.get_width() + 40,
                winner_name_text.get_height() + 40,
            )
            pygame.draw.rect(screen, wall_color, winner_rect, 3)
            pygame.display.update()
            pygame.time.delay(3000)
            is_running = False
            theme = "dark" if dark_mode else "light"
            main_menu.start_main_menu(theme, winner_score, bullet_speed, map_name)

        # -- update() the display to put your work on screen
        pygame.display.update()

        # -- limits FPS to 60
        clock.tick(60)

    pygame.quit()
