import customtkinter

import config
import functions
import game


def start_main_menu(
    theme: str = config.DEFAULT_THEME,
    winner_score: int = config.DEFAULT_WINNER_SCORE,
    bullet_speed: int = config.DEFAULT_BULLET_SPEED,
    map_name: str = config.DEFAULT_MAP,
):
    # -- create main menu window
    main_menu_window = customtkinter.CTk()

    # -- main menu window config
    main_menu_window.geometry(
        f"{config.MAIN_MENU_SCREEN_WIDTH}x{config.MAIN_MENU_SCREEN_HEIGHT}"
    )
    main_menu_window.title("Main Menu")
    main_menu_window.resizable(False, False)
    customtkinter.set_appearance_mode(theme)

    # -- change theme section
    change_theme_frame = customtkinter.CTkFrame(
        main_menu_window, width=config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    change_theme_frame.pack(pady=config.PADDING_Y)

    customtkinter.CTkLabel(
        change_theme_frame,
        text="Choose game theme (default : system) : ",
        font=config.normal_font,
    ).grid(column=0, row=0, padx=10)
    customtkinter.CTkButton(
        change_theme_frame, text="Dark", command=lambda: functions.change_theme("dark")
    ).grid(column=1, row=0)
    customtkinter.CTkButton(
        change_theme_frame,
        text="Light",
        command=lambda: functions.change_theme("light"),
    ).grid(column=2, row=0, padx=10)

    # -- winner score section
    winner_score_frame = customtkinter.CTkFrame(
        main_menu_window, width=config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    winner_score_frame.pack()
    customtkinter.CTkLabel(
        winner_score_frame,
        text=f"Winner score (default : {config.DEFAULT_WINNER_SCORE}) : ",
        font=config.normal_font,
    ).grid(column=0, row=1)
    winner_score = customtkinter.IntVar(value=winner_score)
    winner_score_slider = customtkinter.CTkSlider(
        winner_score_frame,
        from_=1,
        to=20,
        number_of_steps=19,
        variable=winner_score,
        command=lambda value: functions.show_slider_value_to_label(
            value, winner_score_label
        ),
        width=150,
    )
    winner_score_slider.grid(column=1, row=1, padx=20)
    winner_score_label = customtkinter.CTkLabel(
        winner_score_frame, text=winner_score.get(), font=config.bold_font
    )
    winner_score_label.grid(column=2, row=1)

    # -- bullet speed section
    bullet_speed_frame = customtkinter.CTkFrame(
        main_menu_window, width=config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    bullet_speed_frame.pack(pady=config.PADDING_Y)
    customtkinter.CTkLabel(
        bullet_speed_frame,
        text=f"Bullet speed (default : {config.DEFAULT_BULLET_SPEED}) : ",
        font=config.normal_font,
    ).grid(column=0, row=1)
    bullet_speed = customtkinter.IntVar(value=bullet_speed)
    bullet_speed_slider = customtkinter.CTkSlider(
        bullet_speed_frame,
        from_=5,
        to=8,
        number_of_steps=3,
        variable=bullet_speed,
        command=lambda value: functions.show_slider_value_to_label(
            value, bullet_speed_label
        ),
        width=150,
    )
    bullet_speed_slider.grid(column=1, row=1, padx=20)
    bullet_speed_label = customtkinter.CTkLabel(
        bullet_speed_frame, text=bullet_speed.get(), font=config.bold_font
    )
    bullet_speed_label.grid(column=2, row=1)

    # -- change map category
    change_map_frame = customtkinter.CTkFrame(
        main_menu_window, config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    customtkinter.CTkLabel(
        change_map_frame,
        text="Maps : ",
        font=config.normal_font,
    ).grid(column=0, row=0, padx=10)

    map_names = functions.get_maps_name()
    map_name = customtkinter.StringVar(value=map_name)
    optionmenu = customtkinter.CTkOptionMenu(
        change_map_frame,
        values=map_names,
        variable=map_name,
        font=config.small_bold_font,
    ).grid(column=1, row=0, padx=10)

    change_map_frame.pack()

    # -- start game section
    buttons_frame = customtkinter.CTkFrame(
        main_menu_window, width=config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    buttons_frame.pack(pady=config.PADDING_Y)

    customtkinter.CTkButton(
        buttons_frame,
        text="Start Game",
        command=lambda: game.start_game(
            main_menu_window=main_menu_window,
            winner_score=winner_score,
            bullet_speed=bullet_speed,
            map_name=map_name,
        ),
        width=200,
        height=55,
        font=config.bold_font,
    ).grid(column=2, row=0, padx=55)

    customtkinter.CTkButton(
        buttons_frame,
        text="Help",
        command=lambda: functions.help(main_menu_window=main_menu_window),
        width=200,
        height=55,
        font=config.normal_font,
    ).grid(column=1, row=0, padx=55)

    customtkinter.CTkButton(
        buttons_frame,
        text="Quit",
        command=main_menu_window.destroy,
        width=200,
        height=55,
        font=config.normal_font,
    ).grid(column=0, row=0, padx=55)

    return main_menu_window
