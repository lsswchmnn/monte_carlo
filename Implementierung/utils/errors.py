from python.display import print_heading, enter_continue
#=========================================================================

def show_error(title: str="Error", text: str="An unknown error occurred."):
    '''Einfache Fehlermeldung.'''
    print(f"\n ⚠️ {title}: {text}\n")

def cli_blocking_message(
        heading: str, error_type: str, msg_error: str, 
        msg_continue: str="Press enter to continue"
        ):
    '''
    Standardisierte Fehlermeldung mit Überschrift, Fehlertyp, Fehlertext und Aufforderung zum Weitermachen.
    '''
    print_heading(heading)
    show_error(f"{error_type}", f"{msg_error}")
    enter_continue(f"{msg_continue}", seperation=True)