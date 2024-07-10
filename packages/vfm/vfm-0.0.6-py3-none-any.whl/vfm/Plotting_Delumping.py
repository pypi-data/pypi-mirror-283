import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plotting_delumping(api_meas, api_est, gor_meas, gor_est, sgg_meas, sgg_est, cg_vector, z_est, y_est, pseudo_est, x_est, pos_cons, pos_cont, flag_code, dir_save):
    # Function to reorganize and plot the simulation results for model validation

    # Inputs:
    # api_meas - API degree measured
    # api_est - API degree estimation
    # gor_meas - Gas-oil ratio measured
    # gor_est - Gas-oil ratio estimation
    # sgg_meas - Gas specific gravity measured
    # sgg_est - Gas specific gravity estimation
    # cg_vector - Molar composition measurements of the pure components in the gas phase
    # z_est - Molar composition of the wellstream
    # y_est - Molar composition of the gas phase
    # pseudo_est - Optimal molar composition of pseudocomponents in black oil
    # x_est - Molar composition of the oil phase
    # pos_cons - Position of the consistent samples
    # pos_cont - Degree API of the oil at standard conditions (SC)
    # gor_meas - Gas–oil ratio at SC
    # sgg_meas - Gas specific gravity at SC
    # flag_code - Indicator of the procedure followed in the numerical calculation
    # dir_save - Directory to save the results

    # Outputs:
    # MAPE_x - Mean absolute percentage error (MAPE) of the mole fractions in the oil phase with respect to its expected values from the Gamma-distribution model
    # MAPE_y - Mean absolute percentage error (MAPE) of the mole fractions in the gas phase with respect to its expected values from the gas chromatography

    # Detecting the sizes of input variables
    print(f"Debug: pos_cons = {pos_cons}")
    print(f"Debug: pseudo_est shape = {np.array(pseudo_est).shape}")
    print(f"Debug: cg_vector shape = {np.array(cg_vector).shape}")
    print(f"Debug: y_est shape = {np.array(y_est).shape}")
    
    # Ensure pos_cons contains valid integer indices
    pos_cons = pos_cons.astype(int)

    n_pseudo = len(pseudo_est[pos_cons[0]])
    n_cg = len(cg_vector[pos_cons[0]])
    n_comp = len(y_est[pos_cons[0]])
    n_data_max, n_wells, n_code = np.array(y_est).shape

    # Reorganization of output results and calculation of MAPE_x and MAPE_y
    # Memory allocation
    api_vector = np.full((pos_cont * n_code, 1), np.nan)
    gor_vector = np.full((pos_cont * n_code, 1), np.nan)
    sgg_vector = np.full((pos_cont * n_code, 1), np.nan)
    x_vector = np.full((pos_cont * n_code, n_comp), np.nan)
    y_vector = np.full((pos_cont * n_code, n_comp), np.nan)
    y_ref = np.full((pos_cont * n_code, n_cg), np.nan)
    pseudo_vector = np.full((pos_cont * n_code, n_pseudo), np.nan)
    mape_x = np.full((pos_cont * n_code, n_pseudo), np.nan)
    mape_y = np.full((pos_cont * n_code, n_cg), np.nan)

    # Reading the data
    for j in range(n_code):
        for i in range(pos_cont):
            pos_col = (pos_cons[i] // n_data_max) + 1
            pos_row = (pos_cons[i] % n_data_max) - 1
            if x_est[pos_row, pos_col, j] is not None:
                n_comp = len(y_est[pos_row, pos_col, j])
                n_pure = n_comp - n_pseudo

                api_vector[(j * pos_cont) + i] = api_est[pos_row, pos_col, j]
                gor_vector[(j * pos_cont) + i] = gor_est[pos_row, pos_col, j]
                sgg_vector[(j * pos_cont) + i] = sgg_est[pos_row, pos_col, j]
                x_vector[(j * pos_cont) + i, :n_comp] = x_est[pos_row, pos_col, j]
                y_vector[(j * pos_cont) + i, :n_comp] = y_est[pos_row, pos_col, j]
                y_ref[(j * pos_cont) + i, :n_cg] = cg_vector[pos_row, pos_col]
                pseudo_vector[(j * pos_cont) + i, :] = pseudo_est[pos_row, pos_col, j]

                # MAPE calculations
                mape_x[(j * pos_cont) + i, :] = (np.abs(x_vector[(j * pos_cont) + i, n_pure:] - pseudo_vector[(j * pos_cont) + i, :]) / pseudo_vector[(j * pos_cont) + i, :]) * 100
                mape_y[(j * pos_cont) + i, :] = (np.abs(y_vector[(j * pos_cont) + i, :n_cg] - y_ref[(j * pos_cont) + i, :n_cg]) / y_ref[(j * pos_cont) + i, :n_cg]) * 100

    # Definition of graphical properties affected by flag_code
    code_color = ["xc", "ok", "*r"]
    code_display = ["flag_code = 1", "Góes et al. (2022)", "This work"]

    # Plotting the API degree results
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(api_meas[pos_cons], api_meas[pos_cons], '-k', label="Measured API")
    plt.plot(api_meas[pos_cons], 0.95 * api_meas[pos_cons], ':k', label="5% deviation")
    plt.plot(api_meas[pos_cons], 1.05 * api_meas[pos_cons], ':k')
    plt.xlabel("Measured API")
    plt.ylabel("Calculated API")
    plt.legend(loc="best")
    plt.grid(True)
    for j in range(n_code):
        plt.plot(api_meas[pos_cons], api_vector[(j * pos_cont):(j + 1) * pos_cont], code_color[flag_code[j]], label=code_display[flag_code[j]])
    plt.tight_layout()

    # Plotting the gas specific gravity (SGg) results
    plt.subplot(2, 1, 2)
    plt.plot(sgg_meas[pos_cons], sgg_meas[pos_cons], '-k', label="Measured SGg")
    plt.plot(sgg_meas[pos_cons], 0.95 * sgg_meas[pos_cons], ':k', label="5% deviation")
    plt.plot(sgg_meas[pos_cons], 1.05 * sgg_meas[pos_cons], ':k')
    plt.xlabel("Measured SGg")
    plt.ylabel("Calculated SGg")
    plt.legend(loc="best")
    plt.grid(True)
    for j in range(n_code):
        plt.plot(sgg_meas[pos_cons], sgg_vector[(j * pos_cont):(j + 1) * pos_cont], code_color[flag_code[j]], label=code_display[flag_code[j]])
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, "API_SGg.jpeg"), dpi=300)

    # Plotting the gas-oil ratio (GOR) results
    plt.figure()
    plt.plot(gor_meas[pos_cons], gor_meas[pos_cons], '-k', label="Measured GOR")
    plt.plot(gor_meas[pos_cons], 0.95 * gor_meas[pos_cons], ':k', label="5% deviation")
    plt.plot(gor_meas[pos_cons], 1.05 * gor_meas[pos_cons], ':k')
    plt.xlabel("Measured GOR")
    plt.ylabel("Calculated GOR")
    plt.legend(loc="best")
    plt.grid(True)
    for j in range(n_code):
        plt.plot(gor_meas[pos_cons], gor_vector[(j * pos_cont):(j + 1) * pos_cont], code_color[flag_code[j]], label=code_display[flag_code[j]])
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, "GOR.jpeg"), dpi=300)

    # Plotting the mean absolute percentage errors (MAPE) of the molar compositions
    plt.figure()
    plt.subplot(2, 1, 1)
    for j in range(n_code):
        if flag_code[j] == 1:
            for i in range(n_cg):
                plt.plot(y_ref[(j * pos_cont):(j + 1) * pos_cont, i], mape_y[(j * pos_cont):(j + 1) * pos_cont, i], code_color[flag_code[j]])
        else:
            for i in range(n_pure):
                plt.plot(y_ref[(j * pos_cont):(j + 1) * pos_cont, i], mape_y[(j * pos_cont):(j + 1) * pos_cont, i], code_color[flag_code[j]])
    plt.xlabel("Measured $y_i$", fontsize=12)
    plt.ylabel("MAPE (%)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.tight_layout()

    plt.subplot(2, 1, 2)
    for j in range(n_code):
        for i in range(n_pseudo):
            plt.plot(pseudo_vector[(j * pos_cont):(j + 1) * pos_cont, i], mape_x[(j * pos_cont):(j + 1) * pos_cont, i], code_color[flag_code[j]])
    plt.xlabel("Calculated $x_i$", fontsize=12)
    plt.ylabel("MAPE (%)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dir_save, "X_Y.jpeg"), dpi=300)

    return mape_x, mape_y
