import customtkinter

import config
import functions
import game


def start_main_menu():
    # -- create main menu window
    main_menu_window = customtkinter.CTk()

    # -- main menu window config
    main_menu_window.geometry(
        f"{config.MAIN_MENU_SCREEN_WIDTH}x{config.MAIN_MENU_SCREEN_HEIGHT}"
    )
    main_menu_window.title("Main Menu")
    main_menu_window.resizable(False, False)

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
    winner_score = customtkinter.IntVar(value=config.DEFAULT_WINNER_SCORE)
    winner_score_slider = customtkinter.CTkSlider(
        winner_score_frame,
        from_=1,
        to=20,
        number_of_steps=19,
        variable=winner_score,
        command=lambda value: functions.show_winner_score(value, winner_score_label),
        width=150,
    )
    winner_score_slider.grid(column=1, row=1, padx=20)
    winner_score_label = customtkinter.CTkLabel(
        winner_score_frame, text=config.DEFAULT_WINNER_SCORE, font=config.bold_font
    )
    winner_score_label.grid(column=2, row=1)

    # -- start game section
    buttons_frame = customtkinter.CTkFrame(
        main_menu_window, width=config.MAIN_MENU_SCREEN_WIDTH, fg_color="transparent"
    )
    buttons_frame.pack(pady=config.PADDING_Y)

    customtkinter.CTkButton(
        buttons_frame,
        text="Start Game",
        command=lambda: game.start_game(
            main_menu_window=main_menu_window, winner_score=winner_score
        ),
        width=200,
        height=55,
        font=config.bold_font,
    ).grid(column=2, row=0, padx=55)

    customtkinter.CTkButton(
        buttons_frame,
        text="Help",
        command=lambda: 1,
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
