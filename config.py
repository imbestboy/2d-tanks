import customtkinter

# -- main menu screen config
MAIN_MENU_SCREEN_WIDTH: int = 1000
MAIN_MENU_SCREEN_HEIGHT: int = 400

# -- winner score
DEFAULT_WINNER_SCORE: int = 5

# -- help screen config
HELP_SCREEN_WIDTH: int = 300
HELP_SCREEN_HEIGHT: int = 400

# -- game screen config
CELL_X: int = 150
CELL_Y: int = 120
GAME_SCREEN_WIDTH: int = CELL_X * (8 + 1)  # plus 1 for score section
GAME_SCREEN_HEIGHT: int = CELL_Y * 8

# -- map configs
WALL_THICKNESS: int = 10

# -- theme config
customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("system")

# -- creating temp window for config fonts this window will destroy
temp_window = customtkinter.CTk()

# -- font config
normal_font = customtkinter.CTkFont("Helvetica", 20)
bold_font = customtkinter.CTkFont("Helvetica", 20, "bold")

temp_window.destroy()

# -- vertical distance between components main menu
PADDING_Y = 30

# -- tanks config
TANKS_SPEED: int = 4
TANKS_ROTATION_SPEED: int = 4

# -- bullet config
BULLET_ALIVE_TIME: int = 3  # in second
TOTAL_BULLET_COUNT: int = 3
BULLET_SPEED: int = 6
