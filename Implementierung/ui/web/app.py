from   pathlib          import Path
from   ui.web.state     import get_controller, get_plotter
from   ui.common.text   import *
import streamlit        as     st
import sys
#=========================================================================
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

st.set_page_config(
    page_title="Monte Carlo Simulation",
    layout="wide"
)

controller  = get_controller()
plotter     = get_plotter()
config      = controller.config
#-------------------------------------------------------------------------
# Abschnitt: Simulationseinstellungen

st.header("Configuration", divider="gray")

col_fields, col_section = st.columns(2)

with col_fields:

    # Eingabefelder
    n_dim     = st.number_input("Dimensions", min_value=1,      max_value=100,       value=config.n_dimensions, step=1)
    n_paths   = st.number_input("Paths",      min_value=1,      max_value=1_000_000, value=config.n_paths,      step=10)
    n_steps   = st.number_input("Steps",      min_value=10,     max_value=100_000,   value=config.n_steps,      step=100)
    step_size = st.number_input("Step Size",  min_value=0.01,   max_value=100.0,     value=config.step_size,    step=0.1)
    seed      = st.number_input("Seed",       min_value=1,      max_value=99_999,    value=config.seed,         step=1)

    # Änderungen anwenden
    if n_dim != config.n_dimensions:
        controller.set_dimensionality("nd" if n_dim > 1 else "1d", n_dimensions=n_dim)
    if (n_paths, n_steps, step_size) != (config.n_paths, config.n_steps, config.step_size):
        controller.set_parameters(n_steps, n_paths, step_size)
    if seed != config.seed:
        controller.set_seed(seed)

with col_section:

    # Prozesstyp
    process_types = ["markov", "variational", "adaptive"]
    process_type = st.selectbox("Process Type", process_types, index=process_types.index(config.process_type), format_func=str.capitalize)

    # Startstate
    start_options = controller.get_start_state_options()
    start_keys  = list(start_options.keys())
    start_names = [start_options[k]["name"] for k in start_keys]
    current_start_key = next(
        (k for k in start_keys if start_options[k]["name"] == config.start_state_name),
        start_keys[0]
    )
    selected_start_name = st.selectbox("Start State", start_names, index=start_keys.index(current_start_key))
    selected_start_key = start_keys[start_names.index(selected_start_name)]

    if selected_start_key != current_start_key:
        controller.set_start_state(selected_start_key)

    # Transition
    transition_options = controller.get_transition_options(process_type)
    transition_keys = list(transition_options.keys())
    transition_names = [transition_options[k]["name"] for k in transition_keys]

    current_key = next(
        (k for k in transition_keys if transition_options[k]["name"] == config.transition_name),
        transition_keys[0]  # Fallback: aktuelle Transition gehört nicht zum gewählten Prozesstyp
    )

    selected_name = st.selectbox("Transition", transition_names, index=transition_keys.index(current_key))
    selected_key = transition_keys[transition_names.index(selected_name)]

    if process_type != config.process_type or selected_key != current_key:
        controller.set_transition(process_type, selected_key)

    st.caption(transition_options[selected_key]["desc"])    # Beschreibung anzeigen

#-------------------------------------------------------------------------
# Abschnitt: Simulation

st.space(size="xxsmall")
st.header("Simulation", divider="gray")

if st.button("Calculate data", width="stretch"):
    controller.run_simulation()
    st.session_state.last_result_index = len(controller.get_history_entries()) - 1

if "last_result_index" in st.session_state:
    entry = controller.get_history_entry(st.session_state.last_result_index)
    st.write(str(format_result_summary(entry)))

    if st.button("Start plotting", width="stretch"):
        result = entry.result
        config = entry.config

        if config.dimensionality == "nd":
            if config.n_dimensions in (2, 3):
                fig = plotter.plot(result, "sample_paths", config)
                st.pyplot(fig)
                plotter.close(fig)
            else:
                st.info(f"Plotting is not available for {config.n_dimensions} dimensions.")
        else:
            col1, col2, col3 = st.columns(3)
            fig_paths = plotter.plot_paths_1d(result, config)
            with col1:
                st.write("Sample Paths:")
                st.pyplot(fig_paths)
            plotter.close(fig_paths)
            fig_dist = plotter.plot_final_distribution(result, config)
            with col2:
                st.write("Final distribution:")
                st.pyplot(fig_dist)
            plotter.close(fig_dist)
            fig_mean = plotter.plot_mean_and_std(result, config)
            with col3:
                st.write("Mean and std:")
                st.pyplot(fig_mean)
            plotter.close(fig_mean)

else:
    st.info("Click 'Calculate data' to run a simulation first.")
