colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "orange": "\033[33m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "lightgrey": "\033[37m",
    "darkgrey": "\033[90m",
    "lightred": "\033[91m",
    "lightgreen": "\033[92m",
    "yellow": "\033[93m",
    "lightblue": "\033[94m",
    "pink": "\033[95m",
    "lightcyan": "\033[96m",
    "reset": "\033[0m",
    "bold": "\033[01m",
    "disable": "\033[02m",
    "underline": "\033[04m",
    "reverse": "\033[07m",
    "strikethrough": "\033[09m",
    "invisible": "\033[08m",
}


def log(message: str, color: str = colors["yellow"], nln: bool = True):
    """Log a message

    Args:
        message (str): Message to log
        color (str, optional): Color to use. Defaults to colors['yellow'].
        nln (bool, optional): Whether or not to make a new line. Defaults to True.
    """

    n = "\n"
    if color is None:
        print(
            f'{n if nln else ""}'
            + colors["bold"]
            + "[*] "
            + colors["reset"]
            + f"{message}"
            + colors["reset"]
        )
    else:
        print(
            f'{n if nln else ""}'
            + color
            + colors["bold"]
            + "[*] "
            + colors["reset"]
            + color
            + f"{message}"
            + colors["reset"]
        )


def debug(message: str, dbg: bool):
    """Log a debug message

    Args:
        message (str): Debug message to log
        dbg (bool): Whether or not we are in debug mode
    """

    if dbg:
        print(
            colors["lightcyan"]
            + colors["bold"]
            + "[DEBUG] "
            + colors["reset"]
            + colors["lightcyan"]
            + f"{message}"
            + colors["reset"]
        )


def error(message: str):
    """Log an error

    Args:
        message (str): Error to log
    """

    print(
        colors["lightred"]
        + colors["bold"]
        + "[!] "
        + colors["reset"]
        + colors["lightred"]
        + f"{message}"
        + colors["reset"]
    )


def ask(message: str) -> str:
    """Ask a question

    Args:
        message (str): Question to ask

    Returns:
        str: Output from the input function
    """

    return input(
        colors["orange"]
        + colors["bold"]
        + "[?] "
        + colors["reset"]
        + colors["orange"]
        + f"{message}"
        + colors["reset"]
    )
