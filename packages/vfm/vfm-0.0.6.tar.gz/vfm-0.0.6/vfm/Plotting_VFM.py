import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plotting_vfm_v2(data_vfm, data_bdo, time_bdo, qw_sc_est, qo_sc_est, qg_sc_est, pos_sim, flag_init, dir_save):
    # Function to reorganize and plot the simulation results for model validation
    
    # Convert Time columns to datetime
    data_vfm['Time'] = pd.to_datetime(data_vfm['Time'], errors='coerce')
    data_bdo['Time'] = pd.to_datetime(data_bdo['Time'], errors='coerce')
    time_bdo = pd.to_datetime(time_bdo, errors='coerce')
    
    # Ensure all necessary columns are present
    required_columns_vfm = ['Time', 'Qo_SC', 'Qg_SC']
    required_columns_bdo = ['Time', 'Qo_SC', 'Qg_SC', 'Qw_SC']
    for col in required_columns_vfm:
        if col not in data_vfm.columns:
            raise ValueError(f"Missing column {col} in data_vfm")
    for col in required_columns_bdo:
        if col not in data_bdo.columns:
            raise ValueError(f"Missing column {col} in data_bdo")
    
    # Convert relevant columns to numeric
    data_vfm[['Qo_SC', 'Qg_SC']] = data_vfm[['Qo_SC', 'Qg_SC']].apply(pd.to_numeric, errors='coerce')
    data_bdo[['Qo_SC', 'Qg_SC', 'Qw_SC']] = data_bdo[['Qo_SC', 'Qg_SC', 'Qw_SC']].apply(pd.to_numeric, errors='coerce')
    
    # Definition of the input sizes
    n_bdo = len(time_bdo)
    if len(data_vfm) > 1:
        ts = (data_vfm['Time'].iloc[1] - data_vfm['Time'].iloc[0]).total_seconds() / 3600  # in hours
    else:
        ts = 1  # or some default value if there's only one data point
    
    if ts == 0:
        raise ValueError("Time step (ts) calculated as zero, check the 'Time' column in data_vfm")

    n_row = len(data_vfm)
    
    # Ensure pos_sim values are within the valid range
    pos_sim = [pos for pos in pos_sim if pos < n_row and pos >= 0]
    
    # Debug statement to check pos_sim range
    # print(f"Filtered pos_sim (within valid range): {pos_sim}")
    
    # Initialize arrays for estimations
    qot_pi_est = np.full(n_row, np.nan)
    qgt_pi_est = np.full(n_row, np.nan)
    qot_pi_est[pos_sim] = 0
    qgt_pi_est[pos_sim] = 0
    
    # Check the structure of qo_sc_est, qw_sc_est, and qg_sc_est
    if len(qo_sc_est.shape) == 1:
        qo_sc_est = qo_sc_est[:, np.newaxis]
        qw_sc_est = qw_sc_est[:, np.newaxis]
        qg_sc_est = qg_sc_est[:, np.newaxis]
    
    # Calculate total flowrates for PI data
    for i in range(qo_sc_est.shape[1]):
        qot_pi_est[pos_sim] += qo_sc_est[pos_sim, i] / 24  # [N m^3/h]
        qgt_pi_est[pos_sim] += qg_sc_est[pos_sim, i] / 24  # [N m^3/h]
    
    # Initialize arrays for BDO data
    qot_bdo_est = np.full(n_bdo, np.nan)
    qwt_bdo_est = np.full(n_bdo, np.nan)
    qgt_bdo_est = np.full(n_bdo, np.nan)
    qot_bdo_hour = np.full(n_row, np.nan)
    qgt_bdo_hour = np.full(n_row, np.nan)
    
    # Calculate daily total flowrates for BDO data
    k = 0
    j = 0
    qot_bdo = np.zeros(n_bdo)
    qgt_bdo = np.zeros(n_bdo)
    qwt_bdo = np.zeros(n_bdo)
    
    for i in range(n_bdo):
        while k < n_row and (data_vfm['Time'].iloc[k] < time_bdo.iloc[i] or pd.isna(data_vfm['Time'].iloc[k])):
            k += 1
        while j < len(data_bdo) and data_bdo['Time'].iloc[j] < time_bdo.iloc[i]:
            j += 1
        if k > 7 / (ts * 24) and k + 16 / (ts * 24) <= n_row:
            qot_bdo_hour[int(k - 7 / (ts * 24)):int(k + 16 / (ts * 24))] = data_bdo['Qo_SC'].iloc[j] / 24  # [N m^3/h]
            qgt_bdo_hour[int(k - 7 / (ts * 24)):int(k + 16 / (ts * 24))] = data_bdo['Qg_SC'].iloc[j] / 24  # [N m^3/h]
            qot_bdo[i] = data_bdo['Qo_SC'].iloc[j]  # [N m^3/d]
            qgt_bdo[i] = data_bdo['Qg_SC'].iloc[j]  # [N m^3/d]
            qwt_bdo[i] = data_bdo['Qw_SC'].iloc[j]  # [N m^3/d]
            qot_bdo_est[i] = np.sum(qo_sc_est[int(k - 7 / (ts * 24)):int(k + 16 / (ts * 24))]) * ts  # [N m^3/d]
            qwt_bdo_est[i] = np.sum(qw_sc_est[int(k - 7 / (ts * 24)):int(k + 16 / (ts * 24))]) * ts  # [N m^3/d]
            qgt_bdo_est[i] = np.sum(qg_sc_est[int(k - 7 / (ts * 24)):int(k + 16 / (ts * 24))]) * ts  # [N m^3/d]
    
    # Calculate PREs for flowrate estimations
    pre_qo_pi = (qot_pi_est - data_vfm['Qo_SC']) / data_vfm['Qo_SC'] * 100
    pre_qg_pi = (qgt_pi_est - data_vfm['Qg_SC']) / data_vfm['Qg_SC'] * 100
    pre_qo_bdo = (qot_bdo_est - qot_bdo) / qot_bdo * 100
    pre_qg_bdo = (qgt_bdo_est - qgt_bdo) / qgt_bdo * 100
    pre_qw_bdo = (qwt_bdo_est - qwt_bdo) / qwt_bdo * 100
    
    # Define positions with consistent results
    pos_mape11 = ~np.isnan(pre_qo_pi) & (np.abs(pre_qo_pi) < 100)
    pos_mape12 = ~np.isnan(pre_qo_bdo) & (np.abs(pre_qo_bdo) < 100)
    pos_mape21 = ~np.isnan(pre_qg_pi) & (np.abs(pre_qg_pi) < 100)
    pos_mape22 = ~np.isnan(pre_qg_bdo) & (np.abs(pre_qg_bdo) < 100)
    pos_mape32 = ~np.isnan(pre_qw_bdo) & (np.abs(pre_qw_bdo) < 100)
    
    # Calculate MAPEs to evaluate flowrate estimations
    mape_q = np.array([
        [np.mean(np.abs(pre_qo_pi[pos_mape11])), np.mean(np.abs(pre_qo_bdo[pos_mape12]))],
        [np.mean(np.abs(pre_qg_pi[pos_mape21])), np.mean(np.abs(pre_qg_bdo[pos_mape22]))],
        [0, np.mean(np.abs(pre_qw_bdo[pos_mape32]))]
    ])
    
    # Ensure the results directory exists
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    
    # Plotting the simulation results
    tag = ["Goes2021", "Raw", "Preprocessed"]
    
    if flag_init >= len(tag):
        raise ValueError(f"flag_init value {flag_init} is out of range. Valid range is 0 to {len(tag) - 1}.")

    # print(f"data_vfm index length: {len(data_vfm.index)}")
    # print(f"pos_sim: {pos_sim}")
    
    # BDO measurement (qot_bdo) and estimation of the total oil flowrate at SC (qot_bdo_est)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(qot_bdo_est[pos_mape12], '-')
    plt.plot(qot_bdo[pos_mape12], 'o')
    plt.plot(-10 * qot_bdo[pos_mape12] / qot_bdo[pos_mape12], ':k')
    plt.xlabel("Daily period")
    plt.ylabel('Oil Flowrate [N m$^3$/d]')
    plt.legend(["Current model", "BDO", "10% deviation"], loc="best")
    plt.subplot(2, 1, 2)
    plt.plot(pre_qo_bdo[pos_mape12], '-k')
    plt.plot(-10 * pre_qo_bdo[pos_mape12] / pre_qo_bdo[pos_mape12], ':k')
    plt.plot(10 * pre_qo_bdo[pos_mape12] / pre_qo_bdo[pos_mape12], ':k')
    plt.xlabel("Daily period")
    plt.ylabel("PRE Oil Flowrate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, f"{tag[flag_init]}_Oil_BDO.jpeg"), dpi=300)
    
    # BDO measurements (qgt_bdo) and estimations of the total gas flowrate at SC (qgt_bdo_est)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(qgt_bdo_est[pos_mape22], '-')
    plt.plot(qgt_bdo[pos_mape22], 'o')
    plt.plot(-15 * pre_qg_bdo[pos_mape22] / pre_qg_bdo[pos_mape22], ':k')
    plt.xlabel("Daily period")
    plt.ylabel('Gas Flowrate [N m$^3$/d]')
    plt.legend(["Current model", "BDO", "15% deviation"], loc="best")
    plt.subplot(2, 1, 2)
    plt.plot(pre_qg_bdo[pos_mape22], '-k')
    plt.plot(-15 * pre_qg_bdo[pos_mape22] / pre_qg_bdo[pos_mape22], ':k')
    plt.plot(15 * pre_qg_bdo[pos_mape22] / pre_qg_bdo[pos_mape22], ':k')
    plt.xlabel("Daily period")
    plt.ylabel("PRE Gas Flowrate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, f"{tag[flag_init]}_Gas_BDO.jpeg"), dpi=300)
    
    # BDO measurements (qwt_bdo) and estimations of the total water flowrate at SC (qwt_bdo_est)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(qwt_bdo_est[pos_mape32], '-k')
    plt.plot(qwt_bdo[pos_mape32], 'o')
    plt.plot(-30 * pre_qw_bdo[pos_mape32] / pre_qw_bdo[pos_mape32], ':k')
    plt.xlabel("Daily period")
    plt.ylabel('Water Flowrate [N m$^3$/d]')
    plt.legend(["Current model", "BDO", "30% deviation"], loc="best")
    plt.subplot(2, 1, 2)
    plt.plot(pre_qw_bdo[pos_mape32], '-k')
    plt.plot(-30 * pre_qw_bdo[pos_mape32] / pre_qw_bdo[pos_mape32], ':k')
    plt.plot(30 * pre_qw_bdo[pos_mape32] / pre_qw_bdo[pos_mape32], ':k')
    plt.xlabel("Daily period")
    plt.ylabel("PRE Water Flowrate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, f"{tag[flag_init]}_Water_BDO.jpeg"), dpi=300)
    
    # PI measurements (data_vfm['Qo_SC']) and estimations of the total oil flowrate at SC (qot_pi_est)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(data_vfm['Time'][pos_sim], data_vfm['Qo_SC'][pos_sim], 'x',
             data_vfm['Time'][pos_sim], qot_pi_est[pos_sim], '-k',
             data_vfm['Time'][pos_sim], qot_bdo_hour[pos_sim], 'o')
    plt.plot(data_vfm['Time'], -15 * np.ones(n_row), ':k')
    plt.xlabel("Time")
    plt.ylabel('Oil Flowrate [N m$^3$/h]')
    plt.legend(["PI", "Current model", "BDO", "15% deviation"], loc="best", ncol=2)
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.plot(data_vfm['Time'][pos_mape11], pre_qo_pi[pos_mape11], '-k')
    plt.plot(data_vfm['Time'][pos_mape11], -15 * np.ones(sum(pos_mape11)), ':k')
    plt.plot(data_vfm['Time'][pos_mape11], 15 * np.ones(sum(pos_mape11)), ':k')
    plt.xlabel("Time")
    plt.ylabel("PRE Oil Flowrate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, f"{tag[flag_init]}_Oil_PI.jpeg"), dpi=300)
    
    # PI measurements (data_vfm['Qg_SC']) and estimations of the total gas flowrate at SC (qgt_pi_est)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(data_vfm['Time'][pos_sim], data_vfm['Qg_SC'][pos_sim], 'x',
             data_vfm['Time'][pos_sim], qgt_pi_est[pos_sim], '-k',
             data_vfm['Time'][pos_sim], qgt_bdo_hour[pos_sim], 'o')
    plt.plot(data_vfm['Time'], -15 * np.ones(n_row), ':k')
    plt.xlabel("Time")
    plt.ylabel('Gas Flowrate [N m$^3$/h]')
    plt.legend(["PI", "Current model", "BDO", "15% deviation"], loc="best", ncol=2)
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.plot(data_vfm['Time'][pos_mape21], pre_qg_pi[pos_mape21], '-k')
    plt.plot(data_vfm['Time'][pos_mape21], -15 * np.ones(sum(pos_mape21)), ':k')
    plt.plot(data_vfm['Time'][pos_mape21], 15 * np.ones(sum(pos_mape21)), ':k')
    plt.xlabel("Time")
    plt.ylabel("PRE Gas Flowrate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, f"{tag[flag_init]}_Gas_PI.jpeg"), dpi=300)
    
    return (qot_pi_est, qgt_pi_est, qot_bdo_est, qgt_bdo_est, qwt_bdo_est,
            pre_qo_pi, pre_qg_pi, pre_qo_bdo, pre_qg_bdo, pre_qw_bdo, mape_q)
