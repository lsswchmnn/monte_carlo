from ui.cli.utils.errors import show_error
from ui.cli.utils.display import print_thin_separation
#=========================================================================

def input_int(

        min_value: int=0, max_value: int=10000, default: int=100, 

        forbidden:     list = None,     msg:            str  = "value", 
        retry:         bool = True,     raise_error:    bool = True, 
        allow_cancel:  bool = True,     allow_float:    bool = True

        ) -> int | None:

    '''
    Prompt the user for an integer within a specified range.

    The function repeatedly asks for input until a valid value is entered,
    unless `retry` is False. Empty input returns `default` (or raises an
    exception if `raise_error` is True). If `allow_float` is True, floating-point
    numbers are accepted and rounded to the nearest integer before validation.
    The user may enter "c" or "cancel" to abort if `allow_cancel` is True.

    Parameters:
        min_value (int):
            Smallest allowed value (inclusive).

        max_value (int):
            Largest allowed value (inclusive).

        default (int):
            Value returned if the input is empty or invalid while `loop` is
            False and `error` is False.

        forbidden (list | None):
            List of values that are not accepted.

        msg (str):
            Prompt displayed to the user.

        retry (bool):
            If True, keeps asking until valid input is received.
            If False, returns a fallback value or raises an exception.

        raise_error (bool):
            If True, invalid input raises a ValueError immediately.
            If False, invalid input is handled according to `loop`.

        allow_cancel (bool):
            If True, entering "c" or "cancel" returns None.

        allow_float (bool):
            If True, floating-point numbers are accepted and rounded to the
            nearest integer before validation.

    Returns:
        int | None:
            The validated integer, or None if the input was cancelled.
    '''

    if forbidden is None:
        forbidden = []

    while True:

        # Input abfragen
        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip().lower()

        # Abbrechen (wenn erlaubt)
        if allow_cancel and raw in ("c", "cancel"):
            return None

        # Input leer?
        if raw == '':
            if raise_error:
                raise ValueError("Input is empty.")
            return default

        # Zahl einlesen
        try:
            if allow_float:     # float und int akzeptieren
                value = round(float(raw))
            else:
                value = int(raw)   # Nur int akzeptieren

        except ValueError:
            if raise_error:
                if allow_float:
                    raise ValueError(f"'{raw}' is not a valid number.")
                raise ValueError(f"'{raw}' is not a valid integer.")
            if retry:
                continue
            return default

        # Ist der Wert erlaubt?
        if value in forbidden:
            if raise_error:
                raise ValueError(f"{value} is not allowed.")
            if retry:
                continue
            return default

        # Wert klein genug?
        if value > max_value:
            if raise_error:
                raise ValueError(f"{value} is too big, maximal value is {max_value}.")
            if retry:
                continue
            return max_value

        # Wert groß genug?
        if value < min_value:
            if raise_error:
                raise ValueError(f"{value} is too small, minimal value is {min_value}.")
            if retry:
                continue
            return min_value

        return value

def input_float(

        min_value: float=0, max_value: float=10000, default: float=100,
                
        forbidden:      list = None,    msg:         str  = "value", 
        retry:          bool = True,    raise_error: bool = True, 
        allow_cancel:   bool = True

        ) -> float:

    if forbidden is None:
        forbidden = []

    while True:

        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip()
        
        if allow_cancel and raw in ("c", "cancel"):
            return None
        
        # Input leer?
        if raw == '':
            if raise_error:
                show_error("InputError", "Input is empty. Returning Default")
            return default

        # "," durch "." ersetzen
        raw = raw.replace(',', '.')
        
        # Ist Input ein float?
        try:
            value = float(raw)
        except ValueError:
            if not retry:
                if raise_error:
                    show_error("Input Error", f"'{raw}' is not a valid Float. Returning Default")
                return default
            else:
                if raise_error:
                    show_error("Input Error", f"'{raw}' is not a valid Float.")
                continue

        # Ist der Wert erlaubt?
        if value in forbidden:
            if not retry:
                if raise_error:
                    show_error("InputError", f"'{raw} is not allowed. Returning Default")
                return default
            else:
                if raise_error:
                    show_error("InputError", f"'{raw} is not allowed.")
                continue

        # Wert klein genug?
        if value > max_value:
            if not retry:
                if raise_error:
                    show_error("Input Error", f"{value} is to big, maximal value is {max_value}. Returning {max_value}")
                return max_value
            else:
                if raise_error:
                    show_error("Input Error", f"{value} is to big, maximal value is {max_value}.")
                continue

        # Wert groß genug?
        elif value < min_value:
            if not retry:
                if raise_error:
                    show_error("Input Error", f"{value} is to small, minimal value is {min_value}. Retruning {min_value}")
                return min_value
            else:
                if raise_error:
                    show_error("Input Error", f"{value} is to small, minimal value is {min_value}. Retruning {min_value}")
                continue

        return value

def input_str(msg: str="value", allow_cancel=False) -> str:
    value = input(f"{msg}: ").strip()
    
    if allow_cancel and value in ("c", "cancel"):
        return None
    
    if value == '':
        return None

    return value

def input_confirm(msg: str="Are you sure?", default_true: bool=True, warn_symbol: bool=False) -> bool:
    print()
    print_thin_separation(linebreak=False)
    print()
    if not warn_symbol:
        choice = input(f"{msg} (y/n): ").strip().lower()
    else:
        choice = input(f"⚠️ {msg} (y/n): ").strip().lower()

    if not default_true:
        if choice == '':
            choice = False
        if choice in ("y", "yes", "true", "ja", "j"):
            return True
        else:
            return False
        
    elif default_true:
        if choice == '':
            choice = True
        if choice in ("n", "no", "false", "c", "cancel", "nein"):
            return False
        else:
            return True