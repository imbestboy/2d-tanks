import pygame
import random
import customtkinter

import config
import main_menu
import functions


def start_game(main_menu_window: customtkinter.CTk) -> None:
    """start_game close main menu and start the game

    Arguments:
        main_menu_window {customtkinter.CTk} -- tkinter main menu window
    """
    # -- loading settings
    dark_mode = True if main_menu_window["bg"] == "gray92" else False
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
    wall_color = "gray14" if dark_mode else "gray92"
    map_name = "map_1"
    walls, tanks = functions.map_reader(map_name)

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

        screen.fill(game_background_color)

        # x = pygame.Rect(20, 30, 60, 100)
        # pygame.draw.rect(screen, "red", x)
        functions.draw_map(
            screen=screen,
            wall_color=wall_color,
            walls=walls,
            background_color=game_background_color,
            font=font,
            tank_a=tanks[0],
            tank_b=tanks[1],
        )

        # -- update() the display to put your work on screen
        pygame.display.update()

        # -- limits FPS to 60
        clock.tick(60)

    pygame.quit()
