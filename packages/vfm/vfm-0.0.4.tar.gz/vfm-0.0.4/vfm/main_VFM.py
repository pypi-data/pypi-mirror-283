import os
import numpy as np
import pandas as pd
from datetime import datetime
from VFM import VFM
from GetDataPure import GetDataPure
from ExtendCG import ExtendCG
from Plotting_VFM import plotting_vfm_v2
from Plotting_Delumping import plotting_delumping

class VFMProcessor:
    def __init__(self, data_directory, results_directory, flag_init, flag_code):
        self.data_directory = data_directory
        self.results_directory = results_directory
        self.flag_init = flag_init
        self.flag_code = flag_code
        self.wells = ['RJS-680', 'LL-60', 'LL-69', 'LL-90', 'LL-97', 'LL-100', 'LL-102']

        self.SGw = 1.040  # Define SGw globally

        self.load_data()
        self.process_data()

    def preprocess_data(self, df):
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        df.dropna(subset=['Time'], inplace=True)
        df.sort_values(by='Time', inplace=True)
        df.drop_duplicates(subset=['Time'], inplace=True)
        return df

    def load_data(self):
        btp_file_path = os.path.join(self.data_directory, 'Data_BTP.xlsx')
        pi_file_path = os.path.join(self.data_directory, 'Data_PI.xlsx')
        bdo_file_path = os.path.join(self.data_directory, 'Data_BDO.csv')

        self.btp_data = {}
        self.pi_data = {}

        for well in self.wells:
            # Preprocess the data before loading
            btp_df = pd.read_excel(btp_file_path, sheet_name=well)
            pi_df = pd.read_excel(pi_file_path, sheet_name=well)

            self.btp_data[well] = self.preprocess_data(btp_df)
            self.pi_data[well] = self.preprocess_data(pi_df)

            self.btp_data[well]['Time'] = pd.to_datetime(self.btp_data[well]['Time'], format='%Y-%m-%d %H:%M:%S', dayfirst=False, errors='coerce')
            self.pi_data[well]['Time'] = pd.to_datetime(self.pi_data[well]['Time'], format='%Y-%m-%d %H:%M:%S', dayfirst=False, errors='coerce')

            pi_time_diff = self.pi_data[well]['Time'].diff().dt.total_seconds().dropna()
            print(f"PI data time intervals for well {well}: {pi_time_diff.unique()}")

        # Preprocess BDO data
        bdo_df = pd.read_csv(bdo_file_path, delimiter=';', decimal=',')
        self.bdo_data = self.preprocess_data(bdo_df)
        self.bdo_data['Time'] = pd.to_datetime(self.bdo_data['Time'], format='%Y-%m-%d', dayfirst=False, errors='coerce')

        # Ensure the relevant columns are numeric
        self.bdo_data[['Ql_SC', 'Qo_SC', 'Qg_SC', 'Qw_SC']] = self.bdo_data[['Ql_SC', 'Qo_SC', 'Qg_SC', 'Qw_SC']].apply(pd.to_numeric, errors='coerce')

    def process_data(self):
        required_columns = [
            'Rhoo_SC', 'Qo_SC', 'Qg_SC', 'Qw_SC', 'SGg', 'T_sep', 'P_sep'
        ]

        for well in self.wells:
            missing_columns = [col for col in required_columns if col not in self.btp_data[well].columns]
            if missing_columns:
                raise KeyError(f"Missing columns in btp_data for well {well}: {missing_columns}")

            time_diff = self.pi_data[well]['Time'].diff().dt.total_seconds().dropna()
            if time_diff.min() <= 0:
                print(f"Error: Non-positive time interval found in 'Time' column of PI data for well {well}.")
            else:
                print(f"Minimum time interval for well {well}: {time_diff.min()} seconds")

        for well in self.wells:
            if 'TimeBTP' in self.pi_data[well]:
                self.pi_data[well]['TimeBTP'] = pd.to_datetime(self.pi_data[well]['TimeBTP'], errors='coerce')
            else:
                print(f"Error: 'TimeBTP' column not found in pi_data for well {well}")
                continue

            T_us_PI = self.pi_data[well]['T_us_PI']
            P_us_PI = self.pi_data[well]['P_us_PI']
            P_ds_SDV_PI = self.pi_data[well]['P_ds_SDV_PI']
            DeltaPManifold_PI = self.pi_data[well]['DeltaPManifold_PI']
            Qgi_PI = self.pi_data[well]['Qgi_PI']
            u_PI = self.pi_data[well]['u_PI']
            u_RWT = self.pi_data[well]['u_RWT']
            Fc = self.pi_data[well]['P_us_RWT']/self.pi_data[well]['P_us_PI']
            T_us_RWT = self.pi_data[well]['T_us_RWT']
            P_us_RWT = self.pi_data[well]['P_us_RWT']
            P_ds_SDV_RWT = self.pi_data[well]['P_ds_SDV_RWT']
            DeltaPManifold_RWT = self.pi_data[well]['DeltaPManifold_RWT']
            Qgi_RWT = self.pi_data[well]['Qgi_RWT']

            P_us_SDV = self.pi_data[well]['P_ds_SDV_PI']
            P_ds_PI = P_us_SDV + self.pi_data[well]['DeltaPManifold_PI']
            P_us_SDV = self.pi_data[well]['P_ds_SDV_RWT']
            P_ds_RWT = P_us_SDV + self.pi_data[well]['DeltaPManifold_RWT']
            T_us_PI = (T_us_PI + 273.15)
            T_us_RWT = (T_us_RWT + 273.15)
            P_us_PI = P_us_PI*0.01
            P_us_RWT = P_us_RWT*0.01
            P_ds_PI = P_ds_PI*0.01
            P_ds_RWT = P_ds_RWT*0.01
            opening_PI = u_PI/100
            opening_RWT = u_RWT/100

            n_pi = len(self.pi_data[well]['Time'])
            Tag = ["N2", "CO2", "C1", "C2", "C3", "iC4", "nC4", "iC5", "nC5", "nC6", "nC7", "nC8", "nC9", "nC10"]
            PureProperties = GetDataPure(Tag)

            Qg_SC = np.full(n_pi, np.nan)
            Qo_SC = np.full(n_pi, np.nan)
            Qw_SC = np.full(n_pi, np.nan)
            Ql_SC = np.full(n_pi, np.nan)
            BSW = np.full(n_pi, np.nan)
            GOR = np.full(n_pi, np.nan)
            SGg = np.full(n_pi, np.nan)
            T_sep = np.full(n_pi, np.nan)
            P_sep = np.full(n_pi, np.nan)
            y = np.empty(n_pi, dtype=object)

            T_us_est = np.full(n_pi, np.nan)
            P_us_est = np.full(n_pi, np.nan)
            P_ds_est = np.full(n_pi, np.nan)
            Qgi_est = np.full(n_pi, np.nan)
            opening_est = np.full(n_pi, np.nan)
            Fc_est = np.full(n_pi, np.nan)

            P_ds_est = P_ds_PI
            P_us_est = P_us_PI
            T_us_est = T_us_PI
            Fc_est = Fc
            opening_est = opening_PI
            Qgi_est = Qgi_PI

            self.Cv_est = np.full(n_pi, np.nan)
            self.Cv_gpm_est = np.full(n_pi, np.nan)
            self.Qw_SC_est = np.full(n_pi, np.nan)
            self.Qo_SC_est = np.full(n_pi, np.nan)
            self.Qg_SC_est = np.full(n_pi, np.nan)
            self.API_est = np.full(n_pi, np.nan)
            self.GOR_est = np.full(n_pi, np.nan)
            self.SGg_est = np.full(n_pi, np.nan)
            self.z_est = np.empty(n_pi, dtype=object)
            self.x_est = np.empty(n_pi, dtype=object)
            self.y_est = np.empty(n_pi, dtype=object)
            self.pseudo_est = np.empty(n_pi, dtype=object)
            self.MW_vector = np.full(n_pi, np.nan)
            self.FO_del = np.full(n_pi, np.nan)

            btp_time_series = self.btp_data[well]['Time']
            pi_time_series = self.pi_data[well]['Time']
            btp_indices = []
            for pi_time in pi_time_series:
                closest_btp_time = btp_time_series[btp_time_series <= pi_time].max()
                if pd.isna(closest_btp_time):
                    btp_indices.append(None)
                else:
                    btp_index = btp_time_series[btp_time_series == closest_btp_time].index[0]
                    btp_indices.append(btp_index)

            for i, pi_time in enumerate(pi_time_series):
                k = btp_indices[i]
                if k is None:
                    print(f"Skipping i = {i}, no valid btp_time found for PI Time = {pi_time}")
                    continue

                if k < len(self.btp_data[well]):
                    Qg_SC[i] = self.btp_data[well]['Qg_SC'].iloc[k]
                    Qo_SC[i] = self.btp_data[well]['Qo_SC'].iloc[k]
                    Qw_SC[i] = self.btp_data[well]['Qw_SC'].iloc[k]
                    Ql_SC[i] = Qw_SC[i] + Qo_SC[i]
                    BSW[i] = Qw_SC[i] / Ql_SC[i]
                    GOR[i] = Qg_SC[i] / Qo_SC[i]

                    if self.flag_code == 1:
                        MWair = 28.97  # [kg/kmol]
                        SGg[i] = self.btp_data[well]['SGg'].iloc[k] / MWair
                        y[i] = ExtendCG(self.btp_data[well], PureProperties, k, 0)
                    else:
                        k = max(k - 1, 1)
                        y[i], SGg[i] = ExtendCG(self.btp_data[well], PureProperties, k, 0)

                    T_sep[i] = self.btp_data[well]['T_sep'].iloc[k]
                    P_sep[i] = self.btp_data[well]['P_sep'].iloc[k]

            ts = (pi_time_series.iloc[1] - pi_time_series.iloc[0]).total_seconds() / (24 * 3600)  # in days
            inv_ts = int(1 / ts)

            if ts == 0:
                raise ValueError("Time step (ts) calculated as zero, check the 'Time' column in data_vfm")

            pos_sim = list(range(n_pi))
            pos_cont = 0
            pos_error = np.zeros(n_pi)
            pos_cons = np.zeros(n_pi)
            Time_BDO = self.bdo_data['Time']

            if self.flag_init == 1:
                Time_BDO = pd.date_range(start="2019-01-02", end="2019-12-02", freq='MS')
                Time_BDO = pd.Series(Time_BDO)
                n_BDO = len(Time_BDO)

                k = 1
                j = 1
                pos_sim = n_BDO * inv_ts * [0]
                for i in range(n_BDO):
                    while k < len(pi_time_series) and pi_time_series.iloc[k] <= Time_BDO[i]:
                        if k == n_pi - 1:
                            break
                        k += 1
                    for m in range(inv_ts):
                        pos_sim[(j - 1) * inv_ts + m] = k + int((m - 7) * inv_ts / 24)
                    j += 1

                for i in pos_sim[::inv_ts]:
                    for j in range(1):
                        idx = int(i)
                        if idx < n_pi and idx + inv_ts < n_pi:
                            T_us_est[idx] = np.mean(T_us_RWT[idx:idx + inv_ts])
                            P_us_est[idx] = np.mean(P_us_RWT[idx:idx + inv_ts])
                            P_ds_est[idx] = np.mean(P_ds_SDV_RWT[idx:idx + inv_ts])
                            Qgi_est[idx] = np.mean(Qgi_RWT[idx:idx + inv_ts])
                            opening_est[idx] = np.mean(u_RWT[idx:idx + inv_ts])
                            if P_us_est[idx] != 0:
                                Fc_est[idx] = P_us_RWT[idx] / P_us_est[idx]
                            else:
                                Fc_est[idx] = np.nan

                            if idx < len(self.btp_data[well]):
                                results = VFM(
                                    T_us_est[idx], T_us_RWT[idx], P_us_est[idx], P_us_RWT[idx],
                                    P_ds_est[idx], P_ds_RWT[idx], Qgi_est[idx], Qgi_RWT[idx],
                                    opening_est[idx], opening_RWT[idx], Fc_est[idx], self.pi_data[well]['rhoo_SC'].iloc[idx],
                                    SGg[idx], self.SGw, GOR[idx], BSW[idx], Ql_SC[idx], PureProperties,
                                    y[idx], T_sep[idx], P_sep[idx], self.flag_code
                                )
                                (self.Cv_est[idx], self.Cv_gpm_est[idx], self.Qw_SC_est[idx], self.Qo_SC_est[idx],
                                 self.Qg_SC_est[idx], self.API_est[idx], self.GOR_est[idx], self.SGg_est[idx],
                                 self.z_est[idx], self.x_est[idx], self.y_est[idx], self.MW_vector[idx], self.FO_del[idx],
                                 self.pseudo_est[idx]) = results

                                pos_cont += 1

            else:
                for i in pos_sim:
                    if self.flag_init == 3:
                        pos_min = 1e5
                        k = 0

                        while np.isnan(P_ds_PI[i - k]) or P_ds_PI[i - k] == 0:
                            if i - k == 0:
                                break
                            k += 1
                        P_ds_est[i] = P_ds_PI[i - k]
                        pos_min = min(pos_min, i - k)

                        k = 0
                        while np.isnan(P_us_PI[i - k]) or P_us_PI[i - k] == 0 or P_us_PI[i - k] > 200:
                            if i - k == 0:
                                break
                            k += 1
                        P_us_est[i] = P_us_PI[i - k]
                        pos_min = min(pos_min, i - k)

                        if P_us_est[i] < P_ds_est[i]:
                            P_us_est[i] = P_ds_est[i]

                        k = 0
                        while np.isnan(T_us_PI[i - k]) or T_us_PI[i - k] == 273.15:
                            if i - k == 0:
                                break
                            k += 1
                        T_us_est[i] = T_us_PI[i - k]
                        pos_min = min(pos_min, i - k)

                        k = 0
                        while np.isnan(u_PI[i - k]) or u_PI[i - k] == 0:
                            if i - k == 0 or i > n_pi - 3:
                                break
                            if u_RWT[i - k] == 0 and (P_us_PI[i + 2 // (24 * ts)] < P_us_PI[i] or P_us_PI[i + 3 // (24 * ts)] < P_us_PI[i]):
                                break
                            k += 1
                        opening_est[i] = u_PI[i - k]
                        pos_min = min(pos_min, i - k)

                        k = 0
                        while np.isnan(Qgi_PI[i - k]) or Qgi_PI[i - k] > 1000:
                            if i - k == 0:
                                break
                            k += 1
                        Qgi_est[i] = Qgi_PI[i - k]
                        pos_min = min(pos_min, i - k)

                    if P_us_est[i] != 0:
                        Fc_est[i] = P_us_RWT[i] / P_us_est[i]
                    else:
                        Fc_est[i] = np.nan

                    try:
                        if i < len(self.btp_data[well]):
                            results = VFM(
                                T_us_est.iloc[i], T_us_RWT.iloc[i], P_us_est.iloc[i], P_us_RWT.iloc[i],
                                P_ds_est.iloc[i], P_ds_RWT.iloc[i], Qgi_est.iloc[i], Qgi_RWT.iloc[i],
                                opening_est.iloc[i], opening_RWT.iloc[i], Fc_est.iloc[i], self.pi_data[well]['rhoo_SC'].iloc[i],
                                SGg[i], self.SGw, GOR[i], BSW[i], Ql_SC[i], PureProperties,
                                y[i], T_sep[i], P_sep[i], self.flag_code
                            )
                            (self.Cv_est[i], self.Cv_gpm_est[i], self.Qw_SC_est[i], self.Qo_SC_est[i],
                             self.Qg_SC_est[i], self.API_est[i], self.GOR_est[i], self.SGg_est[i],
                             self.z_est[i], self.x_est[i], self.y_est[i], self.MW_vector[i], self.FO_del[i],
                             self.pseudo_est[i]) = results
                            pos_cont += 1
                            pos_cons[i] = 1  # Update to 1 instead of index
                        else:
                            pos_error[i] = 1
                    except Exception as e:
                        pos_error[i] = 1
                        print(f"Error processing position {i}: {e}")

                pos_cons = np.where(pos_cons > 0)[0].astype(int)  # Filter out zeros and convert to integer indices

            if not os.path.exists(self.results_directory):
                os.makedirs(self.results_directory)

            (Qot_PI_est, Qgt_PI_est, Qot_BDO_est, Qgt_BDO_est, Qwt_BDO_est,
             PRE_Qo_PI, PRE_Qg_PI, PRE_Qo_BDO, PRE_Qg_BDO, PRE_Qw_BDO, MAPE_Q) = plotting_vfm_v2(
                self.pi_data[well], self.bdo_data, Time_BDO, self.Qw_SC_est, self.Qo_SC_est, self.Qg_SC_est, pos_sim, self.flag_init, self.results_directory
            )

            rhow_SC = 1000  # [kg/m^3]
            API = 141.5 / (self.btp_data[well]['Rhoo_SC'].mean() / rhow_SC) - 131.5

            if pos_cons.size > 0:
                MAPE_x, MAPE_y = plotting_delumping(API, self.API_est, GOR, self.GOR_est, SGg, self.SGg_est, y, self.z_est, self.y_est, self.pseudo_est, self.x_est, pos_cons, pos_cont, self.flag_code, self.results_directory)
            else:
                print(f"Warning: pos_cons is empty for well {well}")

            np.savez(os.path.join(self.results_directory, "Results"), Cv_est=self.Cv_est, Cv_gpm_est=self.Cv_gpm_est, Qw_SC_est=self.Qw_SC_est, Qo_SC_est=self.Qo_SC_est, Qg_SC_est=self.Qg_SC_est,
                     API_est=self.API_est, GOR_est=self.GOR_est, SGg_est=self.SGg_est, z_est=self.z_est, x_est=self.x_est, y_est=self.y_est, MW_vector=self.MW_vector,
                     FO_del=self.FO_del, Qot_PI_est=Qot_PI_est, Qgt_PI_est=Qgt_PI_est, Qot_BDO_est=Qot_BDO_est, Qgt_BDO_est=Qgt_BDO_est,
                     Qwt_BDO_est=Qwt_BDO_est, PRE_Qo_PI=PRE_Qo_PI, PRE_Qg_PI=PRE_Qg_PI, PRE_Qo_BDO=PRE_Qo_BDO, PRE_Qg_BDO=PRE_Qg_BDO,
                     PRE_Qw_BDO=PRE_Qw_BDO, MAPE_Q=MAPE_Q, MAPE_x=MAPE_x, MAPE_y=MAPE_y, pos_sim=pos_sim, flag_init=self.flag_init, flag_code=self.flag_code)

# Usage example
# data_dir = "/content/vfm_v2/Python/Data/"
# results_dir = "/content/vfm_v2/Python/Results/VFM_case"
# flag_init = 2  # This should be set by the user
# flag_code = 3  # This should be set by the user

# vfm_processor = VFMProcessor(data_dir, results_dir, flag_init, flag_code)
