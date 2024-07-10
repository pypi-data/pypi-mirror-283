import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from vfm.VFM import VFM
from vfm.GetDataPure import GetDataPure
from vfm.ExtendCG import ExtendCG
from vfm.Plotting_VFM import plotting_vfm_v2
from vfm.Plotting_Delumping import plotting_delumping


def simulation_vfm(data_directory, flag_code=3):
    # Definition of the results directory
    results_dir = os.path.join("..", "..", "..", "Results", f"VFM_case{flag_code}")
    os.makedirs(results_dir, exist_ok=True)

    # Load the data stored in .mat extension (assuming you have converted them to .npz)
    data_vfm = np.load(os.path.join(data_directory, "Data_VFM.npz"))
    data_delumping = np.load(os.path.join(data_directory, "Data_Delumping_updated.npz"))

    DataVFM = data_vfm['Data']
    DataDelumping = data_delumping['Data']

    # Storage of input variables from the PI
    T_us_PI = DataVFM['T_us_PI']  # [oC]
    P_us_PI = DataVFM['P_us_PI']  # [kPa]
    P_ds_SDV_PI = DataVFM['P_ds_SDV_PI']  # [kPa]
    DeltaPManifold_PI = DataVFM['DeltaPManifold_PI']  # [kPa]
    Qgi_PI = DataVFM['Qgi_PI']  # [m^3/h]
    u_PI = DataVFM['u_PI']
    u_RWT = DataVFM['u_RWT']
    Fc = DataVFM['Fc']
    T_us_RWT = DataVFM['T_us_RWT']  # [oC]
    P_us_RWT = DataVFM['P_us_RWT']  # [kPa]
    P_ds_SDV_RWT = DataVFM['P_ds_SDV_RWT']  # [kPa]
    DeltaPManifold_RWT = DataVFM['DeltaPManifold_RWT']  # [kPa]
    Qgi_RWT = DataVFM['Qgi_RWT']  # [m^3/h]

    # Adjusting the units of input variables to those of the model
    P_us_SDV = P_ds_SDV_PI  # Assumption
    P_ds_PI = P_us_SDV + DeltaPManifold_PI
    P_us_SDV = P_ds_SDV_RWT  # Assumption
    P_ds_RWT = P_us_SDV + DeltaPManifold_RWT
    T_us_PI = T_us_PI + 273.15  # [K]
    T_us_RWT = T_us_RWT + 273.15  # [K]
    P_us_PI = P_us_PI * 0.01  # [bar]
    P_us_RWT = P_us_RWT * 0.01  # [bar]
    P_ds_PI = P_ds_PI * 0.01  # [bar]
    P_ds_RWT = P_ds_RWT * 0.01  # [bar]
    opening_PI = u_PI / 100
    opening_RWT = u_RWT / 100

    # Definition of the pure components considered in the numerical calculations
    Tag = ["N2", "CO2", "C1", "C2", "C3", "iC4", "nC4", "iC5", "nC5", "nC6", "nC7", "nC8", "nC9", "nC10"]

    # Gather the properties from pure components and store them in a structure
    PureProperties = GetDataPure(Tag)

    # Memory allocation for output variables
    n_row, n_col = P_us_PI.shape
    Cv_est = np.zeros((n_row, n_col))
    Cv_gpm_est = np.zeros((n_row, n_col))
    Qw_SC_est = np.zeros((n_row, n_col))
    Qo_SC_est = np.zeros((n_row, n_col))
    Qg_SC_est = np.zeros((n_row, n_col))
    API_est = np.zeros((n_row, n_col))
    GOR_est = np.zeros((n_row, n_col))
    SGg_est = np.zeros((n_row, n_col))
    z_est = np.empty((n_row, n_col), dtype=object)
    x_est = np.empty((n_row, n_col), dtype=object)
    y_est = np.empty((n_row, n_col), dtype=object)
    pseudo_est = np.empty((n_row, n_col), dtype=object)
    MW_vector = np.zeros((n_row, n_col))
    FO_del = np.zeros((n_row, n_col))

    # Storage of input variables from the RWT
    rhoo_SC = DataVFM['rhoo_SC']  # [m^3/d]
    SGw = 1.040  # Assumed value based on Carbone et al. (2007)

    # Memory allocation of remaining input variables from the RWT
    Qg_SC = np.zeros((n_row, n_col))
    Qo_SC = np.zeros((n_row, n_col))
    Qw_SC = np.zeros((n_row, n_col))
    Ql_SC = np.zeros((n_row, n_col))
    BSW = np.zeros((n_row, n_col))
    GOR = np.zeros((n_row, n_col))
    T_sep = np.zeros((n_row, n_col))
    P_sep = np.zeros((n_row, n_col))
    y = np.empty((n_row, n_col), dtype=object)
    SGg = np.zeros((n_row, n_col))

    # Searches and stores the RWT data from the DataDelumping struct
    N_data_max = max(DataDelumping['N_data'])
    for i in range(n_row):
        for j in range(n_col):
            k = 1
            while (DataDelumping['Time'][k, j] - DataVFM['TimeBTP'][i, j]).days < 0:
                k += 1
                if k > N_data_max:
                    break

            # Storage of the input variables from the RWT
            Qg_SC[i, j] = DataDelumping['Qg_SC'][k, j]
            Qo_SC[i, j] = DataDelumping['Qo_SC'][k, j]
            Qw_SC[i, j] = DataDelumping['Qw_SC'][k, j]
            Ql_SC[i, j] = Qw_SC[i, j] + Qo_SC[i, j]
            BSW[i, j] = Qw_SC[i, j] / Ql_SC[i, j]
            GOR[i, j] = Qg_SC[i, j] / Qo_SC[i, j]

            # Adjustment of sampling times between DataVFM and DataDelumping
            if flag_code == 1:
                MWair = 28.97  # [kg/kmol]
                SGg[i, j] = DataVFM['MWg'][i, j] / MWair
                y[i, j] = ExtendCG(DataDelumping, PureProperties, k, j)
            else:
                k = max(k - 1, 1)
                y[i, j], SGg[i, j] = ExtendCG(DataDelumping, PureProperties, k, j)

            T_sep[i, j] = DataDelumping['T_sep'][k, j]
            P_sep[i, j] = DataDelumping['P_sep'][k, j]

    # Calculation of the VFM algorithm on the defined samples
    for i in range(n_row):
        for j in range(n_col):
            if not np.isnan(P_us_PI[i, j]) and not np.isnan(opening_PI[i, j]) and P_us_PI[i, j] > P_ds_PI[i, j] and Qgi_PI[i, j] < 1000:
                if np.isnan(Qgi_PI[i, j]):
                    Qgi_PI[i, j] = 0
                results = VFM(
                    T_us_PI[i, j], T_us_RWT[i, j], P_us_PI[i, j], P_us_RWT[i, j],
                    P_ds_PI[i, j], P_ds_RWT[i, j], Qgi_PI[i, j], Qgi_RWT[i, j],
                    opening_PI[i, j], opening_RWT[i, j], Fc[i, j], rhoo_SC[i, j],
                    SGg[i, j], SGw, GOR[i, j], BSW[i, j], Ql_SC[i, j], PureProperties,
                    y[i, j], T_sep[i, j], P_sep[i, j], flag_code
                )
                (Cv_est[i, j], Cv_gpm_est[i, j], Qw_SC_est[i, j], Qo_SC_est[i, j],
                 Qg_SC_est[i, j], API_est[i, j], GOR_est[i, j], SGg_est[i, j],
                 z_est[i, j], x_est[i, j], y_est[i, j], MW_vector[i, j], FO_del[i, j],
                 pseudo_est[i, j]) = results

    # Transcription of reported measures in the BDO document
    Qot_BDO = np.array([22767.86, 21923.49, 23589.62, 23479.47, 23289.80, 22065.64,
                        22950.96, 23945.14, 21324.51, 22178.44, 22994.90, 22421.97])

    Qgt_BDO = np.array([5717383, 5308589, 5361545, 5751253, 5733734, 5487994,
                        5805212, 5814666, 5665925, 5800781, 6006580, 5884175])

    Qwt_BDO = np.array([43.25, 41.06, 42.50, 42.33, 40.86, 21.55,
                        22.12, 68.80, 54.94, 84.58, 85.97, 98.11])

    Qt_BDO = Qot_BDO + Qgt_BDO + Qwt_BDO

    # Memory allocation of output variables for model validation
    Qwt_goes = np.zeros(n_row)
    Qot_goes = np.zeros(n_row)
    Qgt_goes = np.zeros(n_row)
    Qwt_est = np.zeros(n_row)
    Qot_est = np.zeros(n_row)
    Qgt_est = np.zeros(n_row)

    # Calculation of total flowrates in each phase for comparison between estimations
    for i in range(n_row):
        Qwt_goes[i] = np.sum(DataVFM['Qw_SC_est'][i, :])
        Qot_goes[i] = np.sum(DataVFM['Qo_SC_est'][i, :])
        Qgt_goes[i] = np.sum(DataVFM['Qg_SC_est'][i, :])

        Qwt_est[i] = np.sum(Qw_SC_est[i, :])
        Qot_est[i] = np.sum(Qo_SC_est[i, :])
        Qgt_est[i] = np.sum(Qg_SC_est[i, :])

    Qt_est = Qwt_est + Qot_est + Qgt_est

    # Definition of the samples plotted
    pos_plot = np.arange(n_row)
    n_plot = len(pos_plot)
    pos_cons = np.zeros(n_plot * n_col, dtype=int)

    pos_cont = 0
    for i in pos_plot:
        for j in range(n_col):
            pos_cons[pos_cont] = i + j * n_row
            pos_cont += 1

    # Plotting the results
    PRE_Qw, PRE_Qo, PRE_Qg, PRE_Qt, R2 = Plotting_VFM(
        Qwt_BDO, Qot_BDO, Qgt_BDO, Qwt_goes, Qot_goes, Qgt_goes, Qwt_est, Qot_est, Qgt_est,
        pos_plot, n_plot, flag_code, results_dir
    )

    rhow_SC = 1000  # [kg/m^3]
    API = 141.5 / (rhoo_SC / rhow_SC) - 131.5
    MAPE_x, MAPE_y = Plotting_Delumping(
        API, API_est, GOR, GOR_est, SGg, SGg_est, y, z_est, y_est, pseudo_est, x_est, pos_cons, pos_cont, flag_code, results_dir
    )

    # Save the simulation results
    np.savez_compressed(os.path.join(results_dir, "Results.npz"),
                        Cv_est=Cv_est, Qwt_BDO=Qwt_BDO, Qot_BDO=Qot_BDO, Qgt_BDO=Qgt_BDO,
                        Qwt_goes=Qwt_goes, Qot_goes=Qot_goes, Qgt_goes=Qgt_goes, Qwt_est=Qwt_est,
                        Qot_est=Qot_est, Qgt_est=Qgt_est, flag_code=flag_code, PRE_Qw=PRE_Qw,
                        PRE_Qo=PRE_Qo, PRE_Qg=PRE_Qg, PRE_Qt=PRE_Qt, R2=R2, MAPE_x=MAPE_x,
                        MAPE_y=MAPE_y)

# Example usage:
# simulation_vfm(data_directory="path_to_data_directory", flag_code=3)
