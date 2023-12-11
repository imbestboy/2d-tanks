import customtkinter

import config
import functions


def start_main_menu():
    # -- create main menu window
    main_menu_window = customtkinter.CTk()

    # -- main menu window config
    main_menu_window.geometry(
        f"{config.MAIN_MENU_SCREEN_WIDTH}x{config.MAIN_MENU_SCREEN_HEIGHT}"
    )
    main_menu_window.title("Main Menu")
    main_menu_window.resizable(False, False)

    # -- add theme section to main menu window
    customtkinter.CTkLabel(
        main_menu_window,
        text="Choose game theme (default : system) : ",
        font=config.normal_font,
    ).grid(column=0, row=0, padx=10, pady=30)
    customtkinter.CTkButton(
        main_menu_window, text="Dark", command=lambda: functions.change_theme("dark")
    ).grid(column=1, row=0, pady=30)
    customtkinter.CTkButton(
        main_menu_window, text="Light", command=lambda: functions.change_theme("light")
    ).grid(column=2, row=0, padx=10, pady=30)

    return main_menu_window
