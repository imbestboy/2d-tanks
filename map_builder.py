import customtkinter
import pygame
import random
import json
import tkinter
import os

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
    button_font = pygame.font.SysFont("Helvetica", 25)
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
        mouse_position = pygame.mouse.get_pos()

        # -- restart button
        restart_text = button_font.render("Restart", True, restart_color)
        restart_x = config.CELL_X * 8 + (
            config.CELL_X // 2 - restart_text.get_width() // 2
        )
        restart_y = config.CELL_Y // 3
        screen.blit(restart_text, (restart_x, restart_y))
        restart_button = pygame.Rect(
            restart_x - 10,
            restart_y - 10,
            restart_text.get_width() + 20,
            restart_text.get_height() + 20,
        )
        pygame.draw.rect(screen, restart_color, restart_button, 2)
        restart_color = (
            config.BUTTON_HOVER_COLORS["restart"]
            if restart_button.collidepoint(*mouse_position)
            else wall_color
        )

        # -- save button
        save_y = restart_y + (config.PADDING_Y * 2)
        save_text = button_font.render("Save", True, save_color)
        save_x = config.CELL_X * 8 + (config.CELL_X // 2 - save_text.get_width() // 2)
        screen.blit(save_text, (save_x, save_y))
        save_button = pygame.Rect(
            save_x - 10,
            save_y - 10,
            save_text.get_width() + 20,
            save_text.get_height() + 20,
        )
        save_color = (
            config.BUTTON_HOVER_COLORS["save"]
            if save_button.collidepoint(*mouse_position)
            else wall_color
        )
        pygame.draw.rect(screen, save_color, save_button, 2)

        # -- quit button
        quit_text = button_font.render("Cancel", True, quit_color)
        quit_y = save_y + (config.PADDING_Y * 2)
        quit_x = config.CELL_X * 8 + (config.CELL_X // 2 - quit_text.get_width() // 2)
        screen.blit(quit_text, (quit_x, quit_y))
        quit_button = pygame.Rect(
            quit_x - 10,
            quit_y - 10,
            quit_text.get_width() + 20,
            quit_text.get_height() + 20,
        )
        quit_color = (
            config.BUTTON_HOVER_COLORS["quit"]
            if quit_button.collidepoint(*mouse_position)
            else wall_color
        )
        pygame.draw.rect(screen, quit_color, quit_button, 2)

        for event in pygame.event.get():
            # -- pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                is_running = False
                main_menu.start_main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for wall in walls_rect:
                    if wall.collidepoint(*mouse_position):
                        wall_type = (
                            "h" if wall.topright[0] - wall.topleft[0] != 10 else "v"
                        )
                        wall_x, wall_y = wall.topleft
                        x = wall_x // config.CELL_X
                        y = wall_y // config.CELL_Y
                        try:
                            walls.remove({"type": wall_type, "x": x, "y": y, "d": 1})
                        except ValueError:
                            pass
                if restart_button.collidepoint(*mouse_position):
                    walls = [
                        {"type": "h", "x": 0, "y": 0, "d": 8},
                        {"type": "h", "x": 0, "y": 8, "d": 8},
                        {"type": "v", "x": 0, "y": 0, "d": 8},
                        {"type": "v", "x": 8, "y": 0, "d": 8},
                    ]
                    # for wall_type in ("h", "v"):
                    #     for y in range(8):
                    #         for x in range(8):
                    #             walls.append({"type": wall_type, "x": x, "y": y, "d": 1})
                    walls += [
                        {"type": wall_type, "x": x, "y": y, "d": 1}
                        for wall_type in ("h", "v")
                        for y in range(8)
                        for x in range(8)
                    ]
                    tanks = []
                    tanks_name = ["A", "B"]
                    try:
                        del map_information_dict["tanks"]
                    except KeyError:
                        pass
                elif save_button.collidepoint(*mouse_position):
                    if len(tanks) == 2:
                        main_menu.start_main_menu()
                        save_map_dialog = customtkinter.CTkInputDialog(
                            text="Enter map name...", title="Save Map"
                        )
                        is_running = False
                    else:
                        if not is_save_error_open:
                            is_save_error_open = True
                            tkinter.messagebox.showinfo(
                                title="tanks error",
                                message="please put tanks in game, right click to put tank (if mouse freezed please press enter to close)",
                            )
                elif quit_button.collidepoint(*mouse_position):
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

    # -- check user wants save map
    if save_map_dialog:
        map_name = save_map_dialog.get_input()
        if map_name:
            if map_name not in ("map_1", "map_2", "map_3"):
                map_information_dict.update({"walls": walls})
                with open(os.path.join("maps", f"{map_name}.json"), "w+") as map_file:
                    map_file.write(json.dumps(map_information_dict))
                tkinter.messagebox.showinfo(
                    title="Map Saved",
                    message="Map successfully saved, restart game to see",
                )
            else:
                tkinter.messagebox.showerror(
                    title="Map name error",
                    message="map name cant be map_1 or map_2 or map_3",
                )
        else:
            tkinter.messagebox.showwarning(
                title="Map name empty or cancelled",
                message="Map name empty or save was cancelled",
            )
