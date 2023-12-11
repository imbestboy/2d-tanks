import customtkinter


def change_theme(theme: str) -> None:
    """change_theme change application theme

    Arguments:
        theme {str} -- only "dark" , "light" and "system"
    """
    if theme in ("dark", "light", "system"):
        customtkinter.set_appearance_mode(theme)
    else:
        raise ValueError("theme should be in 'dark' , 'light' and 'system'")
