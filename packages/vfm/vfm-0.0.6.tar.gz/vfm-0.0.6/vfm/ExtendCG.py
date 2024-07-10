import numpy as np
import pandas as pd
from PengRobinsonCalculation import PengRobinsonCalculation

def ExtendCG(Data, PP, pos_row, pos_col):
    # Constants
    T_SC = 293.15  # [K]
    P_SC = 101325  # [Pa]
    R = 8.314  # [m^3*bar/K/mol]
    MWair = 28.97  # [g/mol]
    rhoair_SC = 0.001 * MWair * P_SC / (R * T_SC)  # [kg/m^3]

    # Searches the closest consistent data in time
    Tempo = Data['Time']
    pos_aux = pos_row

    # Ensure that N2 column is numeric
    Data['N2'] = pd.to_numeric(Data['N2'], errors='coerce')

    if np.isnan(Data['N2'].iloc[pos_row]):
        # Searches for consistent data entry at previous sampling times
        pos_p = 0
        while pos_row - pos_p >= 0 and np.isnan(Data['N2'].iloc[pos_row - pos_p]):
            pos_p += 1
            if pos_row - pos_p < 0:
                break

        # Searches for consistent data entry at later sampling times
        pos_f = 0
        while pos_row + pos_f < len(Data['Time']) and np.isnan(Data['N2'].iloc[pos_row + pos_f]):
            pos_f += 1
            if pos_row + pos_f >= len(Data['Time']):
                break

        # Checks the lack of consistent data at previous sampling times
        if pos_row - pos_p < 0:
            pos_aux = pos_row + pos_f

        # Checks the lack of consistent data at later sampling times
        elif pos_row + pos_f >= len(Data['Time']):
            pos_aux = pos_row - pos_p

        # Definition of the closest consistent data entry in time
        else:
            if (Tempo.iloc[pos_row] - Tempo.iloc[pos_row - pos_p]).days < (Tempo.iloc[pos_row + pos_f] - Tempo.iloc[pos_row]).days:
                pos_aux = pos_row - pos_p
            else:
                pos_aux = pos_row + pos_f

    # Definition of the molar composition of the gas phase based on the results
    # from the gas chromatography
    y = 0.01 * np.array([
        Data['N2'].iloc[pos_aux], Data['CO2'].iloc[pos_aux], Data['C1'].iloc[pos_aux], 
        Data['C2'].iloc[pos_aux], Data['C3'].iloc[pos_aux], Data['iC4'].iloc[pos_aux], 
        Data['nC4'].iloc[pos_aux], Data['iC5'].iloc[pos_aux], Data['nC5'].iloc[pos_aux], 
        Data['nC6'].iloc[pos_aux], Data['nC7'].iloc[pos_aux], Data['nC8'].iloc[pos_aux], 
        Data['nC9'].iloc[pos_aux], Data['nC10'].iloc[pos_aux]
    ])

    # Correction of incomplete n-decane entries
    y[-1] = max(y[-1], 1e-6)

    # Calculation of the specific gravity of the gas phase if not available
    if np.isnan(Data['SGg'].iloc[pos_row]):
        _, V_mist, b = PengRobinsonCalculation(np.zeros(PP['N']), y, T_SC, P_SC, PP['Tc'], PP['Pc'], PP['Acentric'], PP['k_bin'])
        Vm_gas = V_mist[1] - np.sum(y * b * PP['s'])  # [m^3/mol]
        MW_gas = np.sum(y * PP['MW'])  # [kg/mol]
        rhog = MW_gas / Vm_gas * 0.001  # [kg/m^3]
        SGg = rhog / rhoair_SC
    else:
        SGg = Data['SGg'].iloc[pos_aux]

    return y, SGg
