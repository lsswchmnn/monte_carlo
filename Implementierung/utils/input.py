from python.errors import show_error
from python.display import print_thin_separation
#=========================================================================

def input_int(min_value: int=0, max_value: int=10000, default: int=100, 
        forbidden: list = [], msg: str="value", loop: bool = True,
        error: bool=True) -> int | None:
    
    if forbidden is None:
        forbidden = []

    while True:
        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip()

        # Input leer?
        if raw == '':
            if error:
                raise ValueError("Input is empty.")
            return default

        # Ist Input ein integer?
        try:
            value = int(raw)
        except ValueError:
            if not loop:
                if error:
                    raise ValueError(f"'{raw}' is not a valid Integer.")
                return default
            else:
                if error:
                    raise ValueError(f"'{raw}' is not a valid Integer.")
                continue

        # Ist der Wert erlaubt?
        if value in forbidden:
            if not loop:
                if error:
                    raise ValueError(f"'{raw}' is not allowed.")
                return default
            else:
                if error:
                    raise ValueError(f"'{raw}' is not allowed.")
                continue

        # Wert klein genug?
        if value > max_value:
            if not loop:
                if error:
                    raise ValueError(f"{value} is to big, maximal value is {max_value}.")
                return max_value
            else:
                if error:
                    raise ValueError(f"{value} is to big, maximal value is {max_value}.")
                continue

        # Wert groß genug?
        elif value < min_value:
            if not loop:
                if error:
                    raise ValueError(f"{value} is to small, minimal value is {min_value}.")
                return min_value
            else:
                if error:
                    raise ValueError(f"{value} is to small, minimal value is {min_value}.")
                continue

        return value

def input_float(min_value: float=0, max_value: float=10000, default: float=100, 
                forbidden: list = [], msg: str="value", loop: bool=True,
                error: bool=True) -> float:
    if forbidden is None:
        forbidden = []

    while True:

        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip()

        # Input leer?
        if raw == '':
            if error:
                show_error("InputError", "Input is empty. Returning Default")
            return default

        # "," durch "." ersetzen
        raw = raw.replace(',', '.')
        
        # Ist Input ein float?
        try:
            value = float(raw)
        except ValueError:
            if not loop:
                if error:
                    show_error("Input Error", f"'{raw}' is not a valid Float. Returning Default")
                return default
            else:
                if error:
                    show_error("Input Error", f"'{raw}' is not a valid Float.")
                continue

        # Ist der Wert erlaubt?
        if value in forbidden:
            if not loop:
                if error:
                    show_error("InputError", f"'{raw} is not allowed. Returning Default")
                return default
            else:
                if error:
                    show_error("InputError", f"'{raw} is not allowed.")
                continue

        # Wert klein genug?
        if value > max_value:
            if not loop:
                if error:
                    show_error("Input Error", f"{value} is to big, maximal value is {max_value}. Returning {max_value}")
                return max_value
            else:
                if error:
                    show_error("Input Error", f"{value} is to big, maximal value is {max_value}.")
                continue

        # Wert groß genug?
        elif value < min_value:
            if not loop:
                if error:
                    show_error("Input Error", f"{value} is to small, minimal value is {min_value}. Retruning {min_value}")
                return min_value
            else:
                if error:
                    show_error("Input Error", f"{value} is to small, minimal value is {min_value}. Retruning {min_value}")
                continue

        return value

def input_str(msg: str="value") -> str:
    value = input(f"{msg}: ").strip()
    if value == '':
        return None    
    return value

def input_confirm(msg: str="Are you sure?", default_true: bool=True) -> bool:
    print()
    print_thin_separation(linebreak=False)
    print()
    choice = input(f"{msg} (y/n): ").strip().lower()

    if not default_true:
        if choice == '':
            choice = False
        if choice == "y" or choice == True or choice == "yes":
            return True
        else:
            return False
        
    elif default_true:
        if choice == '':
            choice = True
        if choice == "n" or choice == False or choice == "no":
            return False
        else:
            return True