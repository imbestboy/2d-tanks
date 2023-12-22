import customtkinter

# -- main menu screen config
MAIN_MENU_SCREEN_WIDTH: int = 1000
MAIN_MENU_SCREEN_HEIGHT: int = 400

# -- game screen config
CELL_X: int = 150
CELL_Y: int = 120
GAME_SCREEN_WIDTH: int = CELL_X * 8
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
TANK_WIDTH: int = 90
TANK_HEIGHT: int = 60
TANKS_SPEED: int = 10
