import numpy as np
from vfm.GammaDistribution import GammaDistribution
from vfm.GetParametersPseudo import GetParametersPseudo
from vfm.FlashCalculation import FlashCalculation
from vfm.PengRobinsonCalculation import PengRobinsonCalculation
from vfm.HeuristicBinaryInteractions import HeuristicBinaryInteractions

def DelumpingMethod(MWblackoil, eta, Lambda, M_b, PureProperties, y_CG, T_sep, P_sep, Qg_SC, Qo_SC, SGo_meas, API_meas, GOR_meas, SGg_meas, flag_code):
    # Constants at standard conditions (SC)
    P_SC = 101325  # Pressure in Pascal
    T_SC = 293.15  # Temperature in Kelvin
    rhow_SC = 1000  # Density of water in kg/m^3
    R = 8.314  # Ideal gas constant in m^3*bar/K/mol
    MWair = 28.97  # Molecular weight of air in kg/mol
    rhoair_SC = 0.001 * MWair * P_SC / (R * T_SC)  # Density of air at SC in kg/m^3

    N_pseudo = len(M_b)
    N_pure = PureProperties['N']
    kbin_temp = PureProperties['k_bin']
    # Splitting heavy hydrocarbons into pseudocomponents
    if flag_code < 2:
        MW_pseudo, z_pseudo = GammaDistribution(MWblackoil, eta, Lambda, N_pseudo, M_b)
    elif 2 <= flag_code < 4:
        MW_pseudo, z_pseudo = GammaDistribution(MWblackoil, PureProperties['MW'][9], Lambda, N_pseudo, M_b)
        for i in range(len(PureProperties['MW']) - 1, 10, -1):
            kbin_temp = PureProperties['k_bin']

            kbin_temp = np.delete(kbin_temp, i, axis=0)
            kbin_temp = np.delete(kbin_temp, i, axis=1)
        
        N_pure -= 4
    else:
        raise ValueError("Invalid flag_code value.")

    pos_pure = list(range(N_pure))

    # Calculate thermodynamic properties of pseudocomponents
    PseudoProperties = GetParametersPseudo(MWblackoil, MW_pseudo, z_pseudo, SGo_meas, flag_code)

    # Allocate thermodynamic properties of all components
    N_comp = N_pure + len(PseudoProperties['MW'])
    MW_comp = np.concatenate((PureProperties['MW'][:N_pure], PseudoProperties['MW']))
    Tc_comp = np.concatenate((PureProperties['Tc'][:N_pure], PseudoProperties['Tc']))
    Pc_comp = np.concatenate((PureProperties['Pc'][:N_pure], PseudoProperties['Pc']))
    Acentric_comp = np.concatenate((PureProperties['Acentric'][:N_pure], PseudoProperties['Acentric']))
    Vc_comp = np.concatenate((PureProperties['Vc'][:N_pure], PseudoProperties['Vc']))
    s_comp = np.concatenate((PureProperties['s'][:N_pure], PseudoProperties['s']))

    # Calculate binary interaction parameters
    k_bin = HeuristicBinaryInteractions(MW_comp, Vc_comp, PureProperties['k_bin'])

    # Optimal tolerance for flash calculation
    tolK = 0.0001
    maxIter = 1000

    K_posterior = 1e10*np.ones(N_comp)
    Vm = np.zeros(2)

    # Initial estimates for molar composition at each phase
    x_comp = np.zeros((2, N_comp))
    x_comp[0, :] = np.concatenate((1e-2 * np.ones(N_pure), z_pseudo))
    x_comp[0, :] /= np.sum(x_comp[0, :])  # Normalize oil phase
    x_comp[1, :] = np.concatenate((y_CG[:N_pure], 1e-4 * np.ones(N_comp - N_pure)))
    x_comp[1, :] /= np.sum(x_comp[1, :])  # Normalize gas phase

    if flag_code == 1:
        K_prior = x_comp[1, :] / x_comp[0, :]
        Beta_flash = 0.5

        cont = 0
        while np.sum((K_prior / K_posterior - 1) ** 2) > tolK and cont < maxIter:
            phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_sep, P_sep, Tc_comp, Pc_comp, Acentric_comp, k_bin)
            K_prior = phi[0, :] / phi[1, :]

            K_posterior = x_comp[1, :] / x_comp[0, :]

            z_comp = x_comp[0, :] * (1 + Beta_flash * (K_posterior - 1))

            Beta_flash = FlashCalculation(z_comp, K_posterior)

            x_comp[0, :] = z_comp / (1 + Beta_flash * (K_prior - 1))
            x_comp[1, :] = K_prior * x_comp[0, :]
            cont += 1

        K_prior = (Pc_comp / P_SC) * np.exp(5.37 * (1 + Acentric_comp) * (1 - Tc_comp / T_SC))

        cont = 0
        while np.sum((K_prior / K_posterior - 1) ** 2) > tolK and cont < maxIter:
            K_posterior = K_prior

            Beta_flash = FlashCalculation(z_comp, K_posterior)

            x_comp[0, :] = z_comp / (1 + Beta_flash * (K_posterior - 1))
            x_comp[1, :] = K_prior * x_comp[0, :]

            phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_SC, P_SC, Tc_comp, Pc_comp, Acentric_comp, k_bin)
            K_prior = phi[0, :] / phi[1, :]
            cont += 1

        Vm[0] = V_mist[0] - np.sum(x_comp[0, :] * b * s_comp)
        Vm[1] = V_mist[1] - np.sum(x_comp[1, :] * b * s_comp)

        Qom_SC = x_comp[0, :] * Qo_SC / Vm[0]
        Qgm_SC = x_comp[1, :] * Qg_SC / Vm[1]

        Qm_TOT = np.sum(Qom_SC + Qgm_SC)
        z_comp = (Qom_SC + Qgm_SC) / Qm_TOT

        K_prior = (Pc_comp / P_SC) * np.exp(5.37 * (1 + Acentric_comp) * (1 - Tc_comp / T_SC))

        cont = 0
        while np.sum((K_prior / K_posterior - 1) ** 2) > tolK and cont < maxIter:
            K_posterior = K_prior

            Beta_flash = FlashCalculation(z_comp, K_prior)

            x_comp[0, :] = z_comp / (1 + Beta_flash * (K_prior - 1))
            x_comp[1, :] = K_prior * x_comp[0, :]

            phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_SC, P_SC, Tc_comp, Pc_comp, Acentric_comp, k_bin)
            K_prior = phi[0, :] / phi[1, :]
            cont += 1

    else:
        K_prior = (Pc_comp / P_sep) * np.exp(5.37 * (1 + Acentric_comp) * (1 - Tc_comp / T_sep))

        cont = 0
        while np.sum((K_prior / K_posterior - 1) ** 2) > tolK and cont < maxIter:
            K_posterior = K_prior

            if flag_code == 3:
                x_comp[1, pos_pure] = np.sum(x_comp[1, pos_pure]) * y_CG[pos_pure]
                x_comp[1, :] /= np.sum(x_comp[1, :])
                x_comp[0, N_pure:] = np.sum(x_comp[0, N_pure:]) * z_pseudo
                x_comp[0, :] /= np.sum(x_comp[0, :])

            phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_sep, P_sep, Tc_comp, Pc_comp, Acentric_comp, k_bin)
            K_prior = phi[0, :] / phi[1, :]

            phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_SC, P_SC, Tc_comp, Pc_comp, Acentric_comp, k_bin)
            Vm[0] = V_mist[0] - np.sum(x_comp[0, :] * b * s_comp)
            Vm[1] = V_mist[1] - np.sum(x_comp[1, :] * b * s_comp)

            Qom_SC = x_comp[0, :] * Qo_SC / Vm[0]
            Qgm_SC = x_comp[1, :] * Qg_SC / Vm[1]

            Qm_TOT = np.sum(Qom_SC + Qgm_SC)
            z_comp = (Qom_SC + Qgm_SC) / Qm_TOT

            Beta_flash = FlashCalculation(z_comp, K_prior)

            x_comp[0, :] = z_comp / (1 + Beta_flash * (K_prior - 1))
            x_comp[1, :] = K_prior * x_comp[0, :]
            cont += 1

        phi, V_mist, b = PengRobinsonCalculation(x_comp[0, :], x_comp[1, :], T_SC, P_SC, Tc_comp, Pc_comp, Acentric_comp, k_bin)

    # Calculation of the molar volume of each phase at SC
    Vm[0] = V_mist[0] - np.sum(x_comp[0, :] * b * s_comp)
    Vm[1] = V_mist[1] - np.sum(x_comp[1, :] * b * s_comp)
    
    # Molar flowrate calculations
    Qom_SC = x_comp[0, :] * Qo_SC / Vm[0]
    Qgm_SC = x_comp[1, :] * Qg_SC / Vm[1]
    Qm_TOT = np.sum(Qom_SC + Qgm_SC)
    z_comp = (Qom_SC + Qgm_SC) / Qm_TOT

    # Phase fractions and densities
    alfa_o_SC = np.sum(Qom_SC) / Qm_TOT
    rho_o_SC = np.sum(x_comp[0, :] * MW_comp) / Vm[0] * 0.001  # Convert to kg/m^3
    rho_g_SC = np.sum(x_comp[1, :] * MW_comp) / Vm[1] * 0.001  # Convert to kg/m^3

    # Tracking variable calculations
    API_est = 141.5 / (rho_o_SC / rhow_SC) - 131.5
    GOR_est = Vm[1] * (1 - alfa_o_SC) / (Vm[0] * alfa_o_SC)
    SGg_est = rho_g_SC / rhoair_SC

    # Percentage relative errors
    PRE_API = 100 * (API_est - API_meas) / API_meas
    PRE_GOR = 100 * (GOR_est - GOR_meas) / GOR_meas
    PRE_SGg = 100 * (SGg_est - SGg_meas) / SGg_meas

    # Objective function
    FO = max(np.abs([PRE_API, PRE_GOR, PRE_SGg]))

    return FO, PRE_API, PRE_GOR, PRE_SGg, z_comp, x_comp, MW_comp, z_pseudo
