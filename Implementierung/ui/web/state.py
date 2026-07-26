from   core.controller import Controller
from   ui.common.plots import Plotter
import streamlit       as     st
#=========================================================================
# Zugriff auf die App-weiten Kernobjekte über st.session_state.
# Streamlit führt das gesamte Skript bei jeder Interaktion neu aus --
# ohne session_state würden Controller (und damit die History) und
# Plotter (und damit die Einstellungen) bei jedem Klick verloren gehen.
#=========================================================================

def get_controller() -> Controller:
    if "controller" not in st.session_state:
        st.session_state.controller = Controller()
    return st.session_state.controller

def get_plotter() -> Plotter:
    if "plotter" not in st.session_state:
        st.session_state.plotter = Plotter()
    return st.session_state.plotter