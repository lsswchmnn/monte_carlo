from ui.cli.utils.display   import print_heading, enter_continue
from ui.help                import HELP_REGISTRY
#=========================================================================
def print_help(key: str) -> None:
    text = HELP_REGISTRY.get(key)
    if text is None:
        raise KeyError(f"No help text registered for key: '{key}'")
    print_heading("HELP MENU")
    print(text)
    enter_continue()