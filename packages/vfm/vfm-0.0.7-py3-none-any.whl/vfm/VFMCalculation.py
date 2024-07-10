import numpy as np
import math

def VFMCalculation(T_us, P_us, P_ds, Qgi, opening, Fc, SGo, SGg, SGw, GOR, BSW, Ql_SC, flag_code):
    # Defining properties at standard conditions (SC)
    MWair = 28.97  # Molecular weight of air [kg/kmol]
    P_SC = 1.01325  # Standard pressure [bar]
    T_SC = 293.15  # Standard temperature [K]
    rhow_SC = 984.252  # Water density at SC [kg/m^3]
    R = 0.08314462  # Universal gas constant [m^3*bar/K/kmol]

    # Air and gas densities at SC
    rhoair_SC = MWair * P_SC / (R * T_SC)
    rhog_SC = SGg * rhoair_SC

    # Oil and water flow rates at SC
    Qo_SC = Ql_SC * (1 - BSW)
    Qw_SC = Ql_SC * BSW

    # Convert upstream temperature to Fahrenheit
    T_us_F = 1.8 * T_us - 459.67

    # Define water density at 60°F (rhow_Cv) [kg/m^3]
    rhow_Cv = 984.252  # [kg/m^3]

    # Oil and water densities at SC
    rhoo_SC = SGo * rhow_Cv
    rhow_SC = SGw * rhow_Cv

    # Pressure drop across choke valve (deltaP) [bar]
    deltaP = P_us - P_ds

    # Gas formation volume factor assuming ideal gas
    Bg = P_SC * T_us / (T_SC * P_us)
    Qgi_SC = Qgi * 24 / Bg  # [m^3/d]

    # Standing correlation for gas solubility
    if abs(flag_code) == 1:
        API = 141.5 / SGo - 131.5
        Rs = min((SGg * ((0.7969 * P_us + 1.4) * 10 ** (0.0125 * API - 0.0016 * T_us + 0.4183)) ** 1.2048) / 5.6146, GOR)
    else:
        API = 141.5 / (SGo * rhow_SC / rhow_Cv) - 131.5
        Rs = min((SGg * ((0.7969 * P_us + 1.4) * 10 ** (0.0125 * API - 0.00091 * T_us_F)) ** 1.2048) / 5.6146, GOR)

    # Total gas flowrate at SC
    Qg_SC = Qgi_SC + Qo_SC * (GOR - Rs)

    # Lasater correlation for bubble point pressure
    Mo = 630 - 10 * API
    yg = (GOR * 5.6146 / 379.3) / ((GOR * 5.6146 / 379.3) + 350 * SGo / Mo)
    pf = 0.679 * np.exp(2.786 * yg) - 0.323
    Pb = pf * 1.8 * T_us / SGg / 14.5037744

    # Mass flowrates for each phase
    Wg = Qg_SC * rhog_SC
    Wo = Qo_SC * rhoo_SC
    Ww = Qw_SC * rhow_SC
    Wt = Wg + Wo + Ww  # Total mass flowrate [kg/d]

    # Gas upstream volumetric flowrate
    Xt = 0.75
    Y = 1 - (deltaP / P_us) / 3 / Xt
    Vg = R * T_us * Wg / (MWair * SGg * P_us * Y ** 2)

    # Water formation volume factor (Bw) and density corrections
    P_ref = min(P_us, Pb)
    if abs(flag_code) == 1:
        deltawT = -0.010001 + 0.00013391 * T_us_F + 5.50654e-7 * T_us_F ** 2
        deltawP = -5.0987e-8 * P_ref * T_us_F - 6.5443e-11 * P_ref ** 2 * T_us_F + 7.8153e-6 * P_ref - 3.0691e-8 * P_ref ** 2
    else:
        deltawT = -0.003514 + 0.0001863 * T_us_F + 2.923e-7 * T_us_F ** 2
        deltawP = -2.4762e-8 * P_ref * T_us_F - 3.3472e-11 * P_ref ** 2 * T_us_F - 5.6263e-6 * P_ref - 5.1037e-8 * P_ref ** 2

    Bw = (1 + deltawP) * (1 + deltawT)

    # Water isothermal compressibility (cw) [bar^(-1)]
    A_cw = 3.8546 - 0.000134 * 14.5037744 * P_us
    B_cw = -0.01052 + 0.000000477 * 14.5037744 * P_us
    C_cw = 3.9267e-5 - 8.8e-10 * 14.5037744 * P_us if abs(flag_code) == 1 else 3.9267e-14 - 0.00000000088 * 14.5037744 * P_us

    cw = 14.5037744e-6 * (A_cw + B_cw * T_us_F + C_cw * T_us_F ** 2)

    # Water density neglecting gas solubility
    rhow = rhow_SC / Bw

    # Oil compressibility (co) [bar^(-1)]
    X_co = (5.6146 * Rs) ** 0.1982 * T_us_F ** 0.6685 * SGg ** (-0.21435) * API ** 1.0116 * (14.5037744 * P_us) ** (-0.1616)
    co = 14.5037744 * (10 ** (-5.4531 + 5.03e-4 * X_co - 3.5e-8 * X_co ** 2))

    # Oil formation volume factor (Bo)
    if P_us >= Pb:
        Bob = 0.9759 + 0.00012 * (5.6146 * GOR * np.sqrt(SGg / SGo) + 2.25 * T_us - 574.5875) ** 1.2
        Bo = Bob * np.exp(co * (P_us - Pb))
    else:
        Bo = 0.9759 + 0.00012 * (5.6146 * Rs * np.sqrt(SGg / SGo) + 2.25 * T_us - 574.5875) ** 1.2

    # Oil density
    if P_us >= Pb:
        rhoob = ((62.4 * SGo + 0.0136 * 5.6146 * GOR * SGg) / Bo) / 0.0624
        rhoo = rhoob * np.exp(co * (P_us - Pb))
        Bw *= np.exp(cw * (P_us - Pb))
    else:
        rhoo = ((62.4 * SGo + 0.0136 * 5.6146 * Rs * SGg) / Bo) / 0.0624

    # Water cut (WC)
    Qw = Qw_SC * Bw
    Qo = Qo_SC * Bo
    WC = Qw / (Qw + Qo)

    # Liquid density (rhol)
    rhol = rhoo * (1 - WC) + rhow * WC

    # Total upstream volumetric flowrate (Vt) [m^3/d]
    Wl = Wo + Ww
    Vl = Wl / rhol
    Vt = Vg + Vl

    # Upstream mixture density (rhom) [kg/m^3]
    rhom = Wt / Vt

    # Valve sizing coefficient [m^3/(s.Pa^0.5)]
    if flag_code == 1:
        fc = opening ** 2 / (2 - opening ** 4) ** 0.5
    else:
        fc = opening

    den = np.sqrt((deltaP * 1e5) * rhom * rhow_Cv * Fc) * fc
    eps = 0
    #Cv = (Wt / (24 * 3600)) / (den + eps ** (1e6 * den))
    try:
        Cv = (Wt / (24 * 3600)) / (den)
    except:
        Cv = math.inf
        
    Cv_gpm = Cv * 264.172 * 60 / np.sqrt(0.00014504)

    return Cv, Cv_gpm, Wt, rhom, Vt, Qw_SC, Qo_SC, Qg_SC

# Example usage
# Cv, Cv_gpm, Wt, rhom, Vt, Qw_SC, Qo_SC, Qg_SC = VFMCalculation(
    # T_us=350, P_us=100, P_ds=50, Qgi=100, opening=0.8, Fc=1.1, SGo=0.85, SGg=0.65, SGw=1.05,
    # GOR=150, BSW=0.1, Ql_SC=5000, flag_code=1
# )
# print(f"Cv: {Cv}, Cv_gpm: {Cv_gpm}, Wt: {Wt}, rhom: {rhom}, Vt: {Vt}, Qw_SC: {Qw_SC}, Qo_SC: {Qo_SC}, Qg_SC: {Qg_SC}")
