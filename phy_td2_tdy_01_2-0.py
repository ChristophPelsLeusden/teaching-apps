
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.optimize import brentq

# ==========================================
# Antoine-Koeffizienten
# Druck in mbar, Temperatur in °C
# ==========================================

A_B, B_B, C_B = 7.03055, 1211.033, 220.790
A_T, B_T, C_T = 7.07954, 1344.800, 219.480


# ==========================================
# Sättigungsdampfdruck
# ==========================================

def psat_benzol(T):
    return 10**(A_B - B_B/(T + C_B))

def psat_toluol(T):
    return 10**(A_T - B_T/(T + C_T))


# ==========================================
# Siedetemperatur
# ==========================================

def siedetemperatur(x_B, P):

    def gleichung(T):
        return (
            x_B * psat_benzol(T)
            + (1-x_B) * psat_toluol(T) - P
        )

    return brentq(gleichung, -50, 180)


# ==========================================
# Taupunkttemperatur
# ==========================================

def taupunkt(y_B, P):

    def gleichung(T):
        return (
            y_B / psat_benzol(T)
            + (1-y_B) / psat_toluol(T)
            - 1/P
        )

    return brentq(gleichung, -50, 180)


# ==========================================
# Streamlit Oberfläche
# ==========================================

st.set_page_config(
    page_title="Phasendiagramme Benzol / Toluol",
    layout="wide"
)

st.title("Phasendiagramme Benzol / Toluol")

# ==========================================
# Regler
# ==========================================

col1, col2 = st.columns(2)

with col1:
    P = st.slider(
        "Druck T-X Diagramm [mbar]",
        min_value=100,
        max_value=1500,
        value=500,
        step=10
    )

with col2:
    T = st.slider(
        "Temperatur p-X Diagramm [°C]",
        min_value=40,
        max_value=140,
        value=90,
        step=1
    )


# ==========================================
# Zusammensetzung
# ==========================================

x_B = np.linspace(0, 1, 101)
y_B = np.linspace(0, 1, 101)


# ==========================================
# T-x-y-Diagramm
# ==========================================

T_sied = np.array([
    siedetemperatur(x, P) for x in x_B
])

T_tau = np.array([
    taupunkt(y, P) for y in y_B
])

fig1, ax1 = plt.subplots(figsize=(7, 5))

ax1.plot(
    x_B, T_sied,
    color="blue",
    linewidth=2,
    label="Siedelinie"
)

ax1.plot(
    y_B, T_tau,
    color="red",
    linewidth=2,
    label="Taulinie"
)

ax1.set_xlabel("Molenbruch Benzol [-]")
ax1.set_ylabel("Temperatur [°C]")
ax1.set_title(f"T-X Diagramm bei {P} mbar")

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 200)
ax1.grid(True)
ax1.legend()
fig1.tight_layout()


# ==========================================
# p-x-y-Diagramm
# ==========================================

p_B = psat_benzol(T)
p_T = psat_toluol(T)

# Siededruckkurve
p_sied = (
    x_B * p_B
    + (1-x_B) * p_T
)

# Taudruckkurve
p_tau = 1 / (
    y_B / p_B
    + (1-y_B) / p_T
)

fig2, ax2 = plt.subplots(figsize=(7, 5))

ax2.plot(
    x_B, p_sied,
    color="blue",
    linewidth=2,
    label="Siedelinie"
)

ax2.plot(
    y_B, p_tau,
    color="red",
    linewidth=2,
    label="Tauline"
)

ax2.set_xlabel("Molenbruch Benzol [-]")
ax2.set_ylabel("Druck [mbar]")

ax2.set_title(f"p-X Diagramm bei {T} °C")

ax2.set_xlim(0, 1)
#ax2.set_ylim(0, max(p_B, p_T) * 1.15)
ax2.set_ylim(0, 5000)

ax2.grid(True)
ax2.legend()
fig2.tight_layout()


# ==========================================
# Diagramme nebeneinander anzeigen
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1, use_container_width=True)

with col2:
    st.pyplot(fig2, use_container_width=True)


# ==========================================
# Zusätzliche Informationen
# ==========================================

st.subheader("Reinstoffdaten")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Siedepunkt Benzol",
        f"{siedetemperatur(1, P):.2f} °C"
    )

with col2:
    st.metric(
        "Siedepunkt Toluol",
        f"{siedetemperatur(0, P):.2f} °C"
    )

with col3:
    st.metric(
        "Dampfdruck Benzol",
        f"{p_B:.1f} mbar"
    )

with col4:
    st.metric(
        "Dampfdruck Toluol",
        f"{p_T:.1f} mbar"
    )
