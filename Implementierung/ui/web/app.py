from   pathlib          import Path
from   ui.web.state     import get_controller, get_plotter
from   ui.common.text   import *
import streamlit        as     st
import sys
#=========================================================================
# Setup

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

st.set_page_config(
    page_title="Monte Carlo Simulation",
    layout="wide"
)

controller  = get_controller()
plotter     = get_plotter()
config      = controller.config
settings    = plotter.settings
#-------------------------------------------------------------------------
# Abschnitt: Simulationseinstellungen

st.header("Configuration", divider="gray")

col_fields, col_section, col_system = st.columns(3)

with col_fields:

    # Eingabefelder
    n_dim     = st.number_input("Dimensions", min_value=1,    max_value=100,       value=config.n_dimensions, step=1,   key="cfg_n_dim")
    n_paths   = st.number_input("Paths",      min_value=1,    max_value=1_000_000, value=config.n_paths,      step=10,  key="cfg_n_paths")
    n_steps   = st.number_input("Steps",      min_value=10,   max_value=100_000,   value=config.n_steps,      step=100, key="cfg_n_steps")
    step_size = st.number_input("Step Size",  min_value=0.01, max_value=100.0,     value=config.step_size,    step=0.1, key="cfg_step_size")
    seed      = st.number_input("Seed",       min_value=1,    max_value=99_999,    value=config.seed,         step=1,   key="cfg_seed")

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
    process_type = st.selectbox("Process Type", process_types, index=process_types.index(config.process_type), format_func=str.capitalize, key="cfg_process_type")

    # Startstate
    start_options = controller.get_start_state_options()
    start_keys  = list(start_options.keys())
    start_names = [start_options[k]["name"] for k in start_keys]
    current_start_key = next(
        (k for k in start_keys if start_options[k]["name"] == config.start_state_name),
        start_keys[0]
    )
    selected_start_name = st.selectbox("Start State", start_names, index=start_keys.index(current_start_key), key="cfg_start_state")
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

    selected_name = st.selectbox("Transition", transition_names, index=transition_keys.index(current_key), key="cfg_transition")
    selected_key = transition_keys[transition_names.index(selected_name)]

    if process_type != config.process_type or selected_key != current_key:
        controller.set_transition(process_type, selected_key)

    st.caption(transition_options[selected_key]["desc"])    # Beschreibung anzeigen

with col_system:
    smooth        = st.checkbox("Smooth paths", value=settings.smooth, key="sys_smooth")
    smooth_window = st.slider("Smoothing window", min_value=2, max_value=100, value=settings.smooth_window, disabled=not smooth, key="sys_smooth_window")
    grid          = st.checkbox("Grid", value=settings.grid, key="sys_grid")
    alpha         = st.slider("Plot alpha", min_value=0.0, max_value=1.0, value=settings.alpha, step=0.05, key="sys_alpha")

    if smooth != settings.smooth:
        plotter.toggle_smooth()
    if smooth_window != settings.smooth_window:
        plotter.set_smooth_window(smooth_window)
    if grid != settings.grid:
        plotter.toggle_grid()
    if alpha != settings.alpha:
        plotter.set_alpha(alpha)

st.space(size="xsmall")
if st.button("Reset", width="content", type="tertiary"):
    controller.reset_config()
    plotter.reset_settings()

#-------------------------------------------------------------------------
# Abschnitt: Simulation

st.space(size="small")
st.header("Simulation", divider="gray")

if st.button("Run simulation", width="stretch", type="primary"):
    controller.run_simulation()
    st.session_state.last_result_index = len(controller.get_history_entries()) - 1

if "last_result_index" in st.session_state:
    entry   = controller.get_history_entry(st.session_state.last_result_index)
    result  = entry.result
    config  = entry.config

    # Pfad: >1d
    if config.dimensionality == "nd":
        if config.n_dimensions in (2, 3):
            fig = plotter.plot(result, "sample_paths", config)
            with st.container(horizontal=True):
                st.space("stretch")
                st.pyplot(fig, width="content")
                st.space("stretch")
            plotter.close(fig)
        else:
            st.info(f"Plotting is not available for {config.n_dimensions} dimensions.")
            # Zusammenfassung statt Plotting
            st.write("Summary:")
            st.text(format_result_summary(entry))   

    # Pfad: 1d
    else:
        col1, col2, col3 = st.columns(3)
        fig_paths = plotter.plot_paths_1d(result, config)
        with col1:
            st.write("Sample Paths")
            st.pyplot(fig_paths)
        plotter.close(fig_paths)
        fig_dist = plotter.plot_final_distribution(result, config)
        with col2:
            st.write("Final distribution")
            st.pyplot(fig_dist)
        plotter.close(fig_dist)
        fig_mean = plotter.plot_mean_and_std(result, config)
        with col3:
            st.write("Mean and std")
            st.pyplot(fig_mean)
        plotter.close(fig_mean)

else:
    st.info("Click 'Run simulation' to simulate a stochastic process.")

#-------------------------------------------------------------------------
# Abschnitt: Analyse

st.space(size="medium")
st.header("Analysis", divider="gray")

if "last_result_index" not in st.session_state:
    st.info("Run a simulation first to enable analysis.")

else:
    entry = controller.get_history_entry(st.session_state.last_result_index)

    if entry.config.dimensionality != "1d":
        st.info("Analysis is only available for 1D processes.")

    else:
        if st.button("Analyze", width="stretch"):
            with st.spinner("Running analysis..."):
                idx = st.session_state.last_result_index
                controller.calculate_ergodicity(idx)
                controller.calculate_autocorrelation(idx)
                controller.calculate_hurst_exponent(idx)
                controller.calculate_variance_growth(idx)

        if entry.erg_result is not None:
            col_erg, col_acf, col_hurst, col_var = st.columns(4)

            with col_erg:
                st.write("Ergodicity")
                fig = plotter.plot_ergodicity(entry.erg_result, entry.config)
                st.pyplot(fig)
                plotter.close(fig)

            with col_acf:
                st.write("Autocorrelation")
                fig = plotter.plot_autocorrelation(entry.acf_result, entry.config)
                st.pyplot(fig)
                plotter.close(fig)

            with col_hurst:
                st.write("Hurst Exponent")
                fig = plotter.plot_hurst(entry.hurst_result, entry.config)
                st.pyplot(fig)
                plotter.close(fig)

            with col_var:
                st.write("Variance Growth")
                fig = plotter.plot_variance_growth(entry.variance_result, entry.config)
                st.pyplot(fig)
                plotter.close(fig)