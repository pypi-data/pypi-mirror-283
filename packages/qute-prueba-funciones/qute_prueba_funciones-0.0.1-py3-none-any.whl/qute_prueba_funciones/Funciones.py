import numpy as np
from scipy.special import gamma
from scipy.linalg import expm

# Estado coherente del vacío
def coherent_state(nf, alfa):
    vacio = np.zeros((nf + 1, 1))
    for i in range(nf + 1):
        cav = np.zeros((nf + 1, 1))
        cav[i, 0] = alfa ** i / (np.sqrt(gamma(i + 1)))
        vacio += cav
    vacio *= np.exp(-np.abs(alfa) ** 2 / 2)
    return vacio

# Método de Runge-Kutta de orden 4
def solver_rk4(psi0, H, tlist, desv,media ,wp):
    dt = tlist[1] - tlist[0]
    psi_t = np.zeros((len(tlist), len(psi0)), dtype=complex)
    psi_t[0] = psi0.ravel()

    psit_int = np.zeros((len(tlist), len(psi0)), dtype=complex)  #Interacción
    psit_int[0] = expm(1j*H0*0)@psi0.ravel()

    for i in range(1, len(tlist)):
        t = tlist[i - 1]
        k1 = -1j * H(t, desv, media, wp) @ psi_t[i - 1]
        k2 = -1j * H(t + dt / 2, desv, media, wp) @ (psi_t[i - 1] + dt / 2 * k1)
        k3 = -1j * H(t + dt / 2, desv, media, wp) @ (psi_t[i - 1] + dt / 2 * k2)
        k4 = -1j * H(t + dt, desv, media, wp) @ (psi_t[i - 1] + dt * k3)
        
        psi_t[i] = psi_t[i - 1] + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        psi_t[i] /= np.linalg.norm(psi_t[i])

        psit_int[i] = expm(1j*H0*t)@psi_t[i]  #Interacción
        psit_int[i] /= np.linalg.norm(psit_int[i])
    
    return psi_t, psit_int