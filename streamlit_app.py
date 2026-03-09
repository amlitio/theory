import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

# --- 1. Page Configuration and Titles ---
st.set_page_config(page_title="Cosmic String App", layout="wide")
st.title("Exact Asymptotic GW Power Spectrum")
st.markdown("""
This interactive application evaluates the exact analytical solutions for the 
power spectrum of gravitational radiation emitted by cosmic strings, 
bypicking up where traditional numerical cutoffs fail.
""")

# --- 2. Interactive Sidebar (UI Controls) ---
st.sidebar.header("Configure Loop Parameters")
a_param = st.sidebar.slider("Asymmetry Parameter (a)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
c0_base = st.sidebar.number_input("Cusp Amplitude (c_0)", value=1.0, step=0.1)
c1_base = st.sidebar.number_input("Kink Amplitude (c_1)", value=0.8, step=0.1)
log_N_max = st.sidebar.slider("Max Harmonic Mode (log10 N)", min_value=2, max_value=6, value=4)

# --- 3. Mathematical Formula Display ---
st.subheader("The Analytical Solution")
st.markdown("The neuro-symbolic system derived the following exact meromorphic series:")
st.latex(r"""
P(N, a) \simeq \frac{\Gamma(5/6)^2}{\pi \Gamma(1/3)^2} \left[ |c_0|^2 N^{-4/3} + |c_1|^2 N^{-2} + |c_0 c_1 a|^2 N^{-8/3} \right]
""")

# --- 4. Physics Computation (Array for Plotting) ---
@st.cache_data
def compute_power_spectrum(N_array, a, c0, c1):
    prefactor = (gamma(5/6)**2) / (np.pi * gamma(1/3)**2)
    P_cusp = prefactor * (c0**2) * N_array**(-4/3)
    P_kink = prefactor * (c1**2) * N_array**(-2)
    P_interact = prefactor * ((c0 * c1 * a)**2) * N_array**(-8/3)
    return P_cusp + P_kink + P_interact, P_cusp, P_kink, P_interact

# Generate the X-axis (Harmonic Modes)
N_array = np.logspace(1, log_N_max, 500)
P_tot, P_c, P_k, P_i = compute_power_spectrum(N_array, a_param, c0_base, c1_base)

# --- 5. Dynamic Plotting ---
st.subheader("Interactive Spectral Plot")

fig, ax = plt.subplots(figsize=(10, 6))
ax.loglog(N_array, P_tot, 'k-', linewidth=3, label='Total Analytical Solution $P(N)$')
ax.loglog(N_array, P_c, 'r--', linewidth=2, label=r'Cusp Emission ($\propto N^{-4/3}$)')
ax.loglog(N_array, P_k, 'b--', linewidth=2, label=r'Kink Contribution ($\propto N^{-2}$)')
ax.loglog(N_array, P_i, 'g--', linewidth=2, label=r'Cusp-Kink Interaction ($\propto N^{-8/3}$)')

ax.set_xlabel('Harmonic Mode ($N$)', fontsize=12)
ax.set_ylabel('Power Spectrum $P(N)$', fontsize=12)
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(fontsize=11)

st.pyplot(fig)

# --- 6. Live Numerical Evaluation ---
st.divider()
st.subheader("Live Numerical Evaluation")
st.markdown("See the exact mathematical output recalculate in real-time as you adjust the sidebar parameters.")

eval_N = st.number_input("Enter a specific Harmonic Mode (N) to calculate:", min_value=1.0, value=1000.0, step=100.0)

# Calculate the exact values for this single N
prefactor_val = (gamma(5/6)**2) / (np.pi * gamma(1/3)**2)
val_P_cusp = prefactor_val * (c0_base**2) * eval_N**(-4/3)
val_P_kink = prefactor_val * (c1_base**2) * eval_N**(-2)
val_P_interact = prefactor_val * ((c0_base * c1_base * a_param)**2) * eval_N**(-8/3)
val_P_tot = val_P_cusp + val_P_kink + val_P_interact

# Display the plugged-in formula dynamically using LaTeX
st.markdown("**Plugged-in Formula Output:**")
st.latex(rf"""
P({eval_N}, {a_param}) \simeq {val_P_cusp:.4e} + {val_P_kink:.4e} + {val_P_interact:.4e} = \mathbf{{{val_P_tot:.4e}}}
""")

# Display metric cards
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Power P(N)", value=f"{val_P_tot:.4e}")
col2.metric(label="Cusp Power", value=f"{val_P_cusp:.4e}")
col3.metric(label="Kink Power", value=f"{val_P_kink:.4e}")
col4.metric(label="Interaction Power", value=f"{val_P_interact:.4e}")
