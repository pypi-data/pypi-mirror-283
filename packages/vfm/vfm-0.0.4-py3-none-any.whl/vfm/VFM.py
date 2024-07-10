import numpy as np
from scipy.optimize import fsolve, minimize
from DelumpingMethod import DelumpingMethod
from VFMCalculation import VFMCalculation
from BisectionMethod import BisectionMethod

def VFM(T_us_PI, T_us_RWT, P_us_PI, P_us_RWT, P_ds_PI, P_ds_RWT, Qgi_PI, Qgi_RWT,
        opening_PI, opening_RWT, Fc, Rhoo_SC, SGg, SGw, GOR, BSW, Ql_SC, PureProperties,
        y_CG, T_sep, P_sep, flag_code):

    # Constants and initial setup
    rhow_SC = 984.252  # Water density at 60 oF in kg/m^3
    SGo = Rhoo_SC / rhow_SC
    API = 141.5 / SGo - 131.5

    # Definitions concerning the Gamma-Distribution model used to split the heavy hydrocarbons
    Lambda = 0.5  # Simplified value

    if flag_code == 1:
        MWblackoil = 197
        eta = PureProperties['MW'][PureProperties['N'] - 1]
        M_b = np.array([156.31, 170.34, 184.37, 198.39, 212.42, 226.45, 240.47, 1100])
        lb_var, ub_var = 144, 250
    else:
        MWblackoil = np.exp(-(API - 202.99) / 29.95)
        eta = PureProperties['MW'][9]
        M_b = np.append(PureProperties['MW'][10:], [170.34, 198.39, 226.45, 1100])
        lb_var, ub_var = M_b[0], M_b[-1]

    N_pseudo = len(M_b)
    OptTol = 1e-3

    # Calculation of Cv_est based on reference well test data
    Cv_est, Cv_gpm_est, Wt, Rhom, Vt, Qw_SC_est, Qo_SC_est, Qg_SC_est = VFMCalculation(T_us_RWT, P_us_RWT, P_ds_RWT, Qgi_RWT,
                                        opening_RWT, 1, SGo, SGg, SGw, GOR, BSW, Ql_SC, -flag_code)

    # Use fsolve to find Ql_SC_est
    def equations(Ql_var):
        Cv_est_temp, _, _, _, _, _, _, _ = VFMCalculation(T_us_PI, P_us_PI, P_ds_PI, Qgi_PI,
                                        opening_PI, Fc, SGo, SGg, SGw, GOR, BSW, Ql_var, -flag_code)
        return Cv_est_temp - Cv_est
            
    Ql_SC_est = fsolve(equations, Ql_SC, xtol=OptTol)[0]

    # Additional calculations for volumetric flows and other estimates
    Cv_est, Cv_gpm_est, Wt, Rhom, Vt, Qw_SC_est, Qo_SC_est, Qg_SC_est = VFMCalculation(
        T_us_PI, P_us_PI, P_ds_PI, Qgi_PI, opening_PI, Fc, SGo, SGg, SGw, GOR, BSW, Ql_SC_est, -flag_code)

    def objective_function(Ql_var):
        FO, _, _, _, _, _, _, _ = DelumpingMethod(Ql_var, eta, Lambda, M_b, PureProperties, y_CG, T_sep, P_sep, Qg_SC_est, Qo_SC_est, SGo, API, Qg_SC_est/Qo_SC_est, SGg, flag_code)
        return FO
                
    if flag_code == 1:
        FO, aux, _, PRE_API, PRE_GOR, PRE_SGg, z_est, x_comp, _, pseudo_est = BisectionMethod(
            objective_function, MWblackoil, lb_var, ub_var, OptTol)
    else:
        opt_result = minimize(objective_function, x0=MWblackoil, bounds=[(lb_var, ub_var)],
                              method='trust-constr', options={'xtol': OptTol, 'gtol': OptTol})
        aux = opt_result.x[0]
        FO = opt_result.fun
        FO, PRE_API, PRE_GOR, PRE_SGg, z_est, x_comp, MW_comp, pseudo_est = DelumpingMethod(aux, eta, Lambda, M_b, PureProperties, y_CG, T_sep, P_sep, Qg_SC_est, Qo_SC_est, SGo, API, Qg_SC_est/Qo_SC_est, SGg, flag_code)

    # Storage of output variables
    MWblackoil = aux
    API_est = API + PRE_API * API / 100
    GOR_est = Qg_SC_est / Qo_SC_est + PRE_GOR * Qg_SC_est / Qo_SC_est / 100
    SGg_est = SGg + PRE_SGg * SGg / 100
    x_est = x_comp[0, :]
    y_est = x_comp[1, :]

    return Cv_est, Cv_gpm_est, Qw_SC_est, Qo_SC_est, Qg_SC_est, API_est, GOR_est, \
           SGg_est, z_est, x_est, y_est, MWblackoil, FO, pseudo_est

# Example usage:
# PureProperties = {'MW': np.array([...]), 'N': 10}
# results = VFM(T_us_PI=300, T_us_RWT=305, P_us_PI=1.5, P_us_RWT=1.6,
#               P_ds_PI=1.1, P_ds_RWT=1.2, Qgi_PI=100, Qgi_RWT=95,
#               opening_PI=0.9, opening_RWT=0.85, Fc=1.05, Rhoo_SC=850, SGg=0.7,
#               SGw=1.02, GOR=200, BSW=0.1, Ql_SC=500, PureProperties=PureProperties,
#               y_CG=np.array([...]), T_sep=310, P_sep=1300, flag_code=1)

