from   pathlib      import Path
from   ui.web.state import get_controller, get_plotter
import streamlit    as     st
import sys
#=========================================================================
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
controller = get_controller()
plotter = get_plotter()

# Test: Config
st.header("Config")
col1, col2, col3 = st.columns(3)

with col1:
    paths = st.number_input("Input paths")
    controller.config.n_paths = paths

with col2:
    steps = st.number_input("Input steps")
    controller.config.n_steps = steps

with col3:
    seed = st.number_input("Input seed")
    controller.config.n_steps = steps


# Test: Plotting
st.header("Plotting")
if st.button("Start plotting"):
    paths = controller.run_simulation()

    # Figuren plotten
    plot_paths = plotter.plot_paths_1d(paths=paths, config=controller.config)
    plot_dist = plotter.plot_final_distribution(paths=paths, config=controller.config)
    plot_mean = plotter.plot_mean_and_std(paths=paths, config=controller.config)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Sample Paths:")
        st.pyplot(plot_paths)

    with col2:
        st.write("Final distribution:")
        st.pyplot(plot_dist)

    with col3:
        st.write("Mean and std:")
        st.pyplot(plot_mean)




# Test: Tabelle
# import pandas as pd

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [controller.config.seed, (controller.config.n_paths), (controller.config.n_steps), (controller.config.n_dimensions)],
#     'second column': ["Seed", "Paths", "Steps", "Dimensions"]
# }))