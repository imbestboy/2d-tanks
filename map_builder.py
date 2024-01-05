import customtkinter
import pygame

import config
import main_menu
import functions


def map_builder(main_menu_window: customtkinter.CTk):
    """map_builder close main menu and start building map

    Arguments:
        main_menu_window {customtkinter.CTk} -- tkinter main menu window
    """
    # -- loading settings
    dark_mode = True if main_menu_window["bg"] == "gray14" else False
    map_builder_background_color = main_menu_window["bg"]

    # -- close main menu window
    main_menu_window.destroy()

    # -- setup building components
    save_map_dialog = None
    wall_color = "gray92" if dark_mode else "gray14"
    map_information_dict = {}
    tanks_name = ["A", "B"]
    tanks = []
    is_save_error_open = False

    default_walls = [
        {"type": "h", "x": 0, "y": 0, "d": 8},
        {"type": "h", "x": 0, "y": 8, "d": 8},
        {"type": "v", "x": 0, "y": 0, "d": 8},
        {"type": "v", "x": 8, "y": 0, "d": 8},
    ]
    # for wall_type in ("h", "v"):
    #     for y in range(8):
    #         for x in range(8):
    #             walls.append({"type": wall_type, "x": x, "y": y, "d": 1})
    walls = default_walls + [
        {"type": wall_type, "x": x, "y": y, "d": 1}
        for wall_type in ("h", "v")
        for y in range(8)
        for x in range(8)
    ]

    # -- game screen setup
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True
    screen = pygame.display.set_mode(
        (config.GAME_SCREEN_WIDTH, config.GAME_SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Map Builder")

    # -- colors
    restart_color = wall_color
    save_color = wall_color
    quit_color = wall_color

    # -- map builder loop
    while is_running:
        screen.fill(map_builder_background_color)

        for event in pygame.event.get():
            # -- pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                is_running = False
                main_menu.start_main_menu()

        # -- draw walls
        walls_rect = [
            functions.draw_wall(**wall, screen=screen, color=wall_color)
            for wall in walls
        ]

        # -- update() the display to put your work on screen
        pygame.display.update()

        # -- limits FPS to 60
        clock.tick(60)
    pygame.quit()
