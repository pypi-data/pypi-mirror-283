import os
import numpy as np
import pandas as pd

class DataImporter:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.wells = ['RJS-680', 'LL-60', 'LL-69', 'LL-90', 'LL-97', 'LL-100', 'LL-102']
        self.data_btp = {well: {} for well in self.wells}
        self.data_pi = {'Time': [], 'P_sep': [], 'Qo_SC': [], 'Qg_SC': []}
        self.data_well_specific = {
            well: {
                'DeltaPManifold_PI': [], 'DeltaPManifold_RWT': [], 'P_ds_SDV_PI': [], 'P_us_PI': [], 'T_us_PI': [],
                'u_PI': [], 'Qgi_PI': [], 'TimeBTP': [], 'P_us_RWT': [], 'T_us_RWT': [], 'u_RWT': [], 'Qgi_RWT': [],
                'P_ds_SDV_RWT': [], 'rhoo_SC': []
            } for well in self.wells
        }
        self.data_bdo = {'Time': [], 'Ql_SC': [], 'Qo_SC': [], 'Qg_SC': [], 'Qw_SC': []}

    def read_btp_data(self):
        btp_path = os.path.join(self.data_directory, 'BTP_Data.csv')
        aux = pd.read_csv(btp_path, delimiter=',', encoding='utf-8-sig')
        print("BTP_Data.csv columns:", aux.columns)

        aux['Time'] = pd.to_datetime(aux['Time'], dayfirst=True)
        aux.columns = [col.replace('Bo_inv', 'Bo').replace('PusChoke', 'P_us').replace('TusChoke', 'T_us').replace('Unnamed: 32', 'MolarMass') for col in aux.columns]
        aux = aux.drop(columns=['Unnamed: 33'])

        for _, row in aux.iterrows():
            well = row['Well']
            if well in self.wells:
                for col in aux.columns:
                    if col not in self.data_btp[well]:
                        self.data_btp[well][col] = []
                    self.data_btp[well][col].append(row[col])
        print(f"BTP data processed for wells: {self.wells}")

    def read_pi_data(self):
        pi_path = os.path.join(self.data_directory, 'Config_TAGS_PI-Daniel_PIDATALINK.xlsx')
        aux = pd.read_excel(pi_path, sheet_name='DataPI')
        print("Config_TAGS_PI-Daniel_PIDATALINK.xlsx columns:", aux.columns)

        aux['Time'] = pd.to_datetime(aux['Time'], dayfirst=True, errors='coerce')

        for i, row in aux.iterrows():
            time = row['Time']
            p_sep = self.safe_float_conversion(row['P66_301092_1223_PIT_012_EAN'])
            qo_sc = self.safe_float_conversion(row['P66_301092_1212_FQI_002a_vzb']) + self.safe_float_conversion(row['P66_301092_1212_FQI_002b_vzb'])
            qg_sc = self.safe_float_conversion(row['P66_301092_1223_FQI_015_vzb_cor']) + self.safe_float_conversion(row['P66_301092_1223_FQI_020_vzb_cor']) + self.safe_float_conversion(row['P66_301092_1223_FQI_030_vzb_cor'])
            delta_p_manifold = self.safe_float_conversion(row['P66_301092_1223_PDIT_021_EAN'])
            p_ds_sdv = (self.safe_float_conversion(row['P66_301092_1223_PIT_024_EAN']) + self.safe_float_conversion(row['P66_301092_1223_PIT_026_EAN'])) / 2

            self.data_pi['Time'].append(time)
            self.data_pi['P_sep'].append(p_sep)
            self.data_pi['Qo_SC'].append(qo_sc)
            self.data_pi['Qg_SC'].append(qg_sc)

            well_columns = {
                'RJS-680': 'W', 'LL-60': 'R', 'LL-69': 'V', 'LL-90': 'U', 'LL-97': 'G', 'LL-100': 'K', 'LL-102': 'J'
            }

            for well, suffix in well_columns.items():
                self.data_well_specific[well]['DeltaPManifold_PI'].append(delta_p_manifold)
                self.data_well_specific[well]['P_ds_SDV_PI'].append(p_ds_sdv)
                self.data_well_specific[well]['P_us_PI'].append(self.safe_float_conversion(row.get(f'P66_301092_1210_PIT_001{suffix}_EAN', np.nan)))
                self.data_well_specific[well]['T_us_PI'].append(self.safe_float_conversion(row.get(f'P66_301092_1210_TIT_008{suffix}_EAN', np.nan)))
                self.data_well_specific[well]['u_PI'].append(self.safe_float_conversion(row.get(f'P66_301092_1210_ZIT_004{suffix}_EAN', np.nan)))
                self.data_well_specific[well]['Qgi_PI'].append(self.safe_float_conversion(row.get(f'P66_301092_1244_FIT_001{suffix}_EAN', np.nan)))

        for key in self.data_pi:
            print(f"{key} length: {len(self.data_pi[key])}")

    def read_bdo_data(self):
        bdo_path = os.path.join(self.data_directory, 'BDO_Data.csv')
        aux = pd.read_csv(bdo_path, delimiter=';', decimal=',', encoding='utf-8-sig')
        print("BDO_Data.csv columns:", aux.columns)

        aux['Time'] = pd.to_datetime(aux['Time'], dayfirst=True, errors='coerce')

        for _, row in aux.iterrows():
            self.data_bdo['Time'].append(pd.to_datetime(row['Time'], dayfirst=True))
            self.data_bdo['Ql_SC'].append(self.safe_float_conversion(row['Ql_SC']))
            self.data_bdo['Qo_SC'].append(self.safe_float_conversion(row['Qo_SC']))
            self.data_bdo['Qg_SC'].append(self.safe_float_conversion(row['Qg_SC']))
            self.data_bdo['Qw_SC'].append(self.safe_float_conversion(row['Ql_SC']) - self.safe_float_conversion(row['Qo_SC']))
        print("BDO data processing completed.")

    def ensure_consistent_lengths(self):
        max_length = max(len(self.data_pi[key]) for key in self.data_pi)
        for key in self.data_pi:
            if len(self.data_pi[key]) < max_length:
                self.data_pi[key].extend([np.nan] * (max_length - len(self.data_pi[key])))

        for well in self.wells:
            lengths = {key: len(self.data_well_specific[well][key]) for key in self.data_well_specific[well]}
            print(f"Lengths for well {well}: {lengths}")
            max_length = max(lengths.values())
            for key in self.data_well_specific[well]:
                if len(self.data_well_specific[well][key]) < max_length:
                    self.data_well_specific[well][key].extend([np.nan] * (max_length - len(self.data_well_specific[well][key])))

    def safe_float_conversion(self, value):
        if isinstance(value, str):
            value = value.replace(',', '.')
        try:
            return float(value)
        except ValueError:
            return float('nan')

    def save_data(self):
        # Save data_btp to a single Excel file
        with pd.ExcelWriter(os.path.join(self.data_directory, 'Data_BTP.xlsx'), engine='openpyxl') as writer:
            for well in self.wells:
                well_df = pd.DataFrame(self.data_btp[well])
                well_df['N_data'] = len(well_df)
                well_df.columns = [col.replace('Bo_inv', 'Bo').replace('PusChoke', 'P_us').replace('TusChoke', 'T_us').replace('Unnamed: 32', 'MolarMass') for col in well_df.columns]
                well_df = well_df.drop(columns=['Unnamed: 33'], errors='ignore')
                well_df.to_excel(writer, sheet_name=well, index=False)
        print("BTP data saved to Excel.")

        # Combine data_pi and well-specific data into an Excel file with multiple sheets
        with pd.ExcelWriter(os.path.join(self.data_directory, 'Data_PI.xlsx'), engine='openpyxl') as writer:
            for well in self.wells:
                total_rows = len(self.data_pi['Time'])
                n_data = len(self.data_btp[well]['Time'])
                interval = total_rows // n_data

                time_btp = []
                delta_p_manifold_rwt = []
                p_us_rwt = []
                t_us_rwt = []
                u_rwt = []
                qgi_rwt = []
                p_ds_sdv_rwt = []
                rhoo_sc = []

                for i in range(n_data):
                    start_idx = i * interval
                    end_idx = start_idx + interval if i < n_data - 1 else total_rows
                    time_btp.extend([self.data_btp[well]['Time'][i]] * (end_idx - start_idx))
                    delta_p_manifold_rwt.extend([self.data_btp[well]['DeltaPManifold'][i]] * (end_idx - start_idx))
                    p_us_rwt.extend([self.data_btp[well]['P_us'][i]] * (end_idx - start_idx))
                    t_us_rwt.extend([self.data_btp[well]['T_us'][i]] * (end_idx - start_idx))
                    u_rwt.extend([self.data_btp[well]['u'][i]] * (end_idx - start_idx))
                    qgi_rwt.extend([self.data_btp[well]['Qgi'][i]] * (end_idx - start_idx))
                    p_ds_sdv_rwt.extend([self.data_btp[well]['PdsSDV'][i]] * (end_idx - start_idx))
                    rhoo_sc.extend([self.data_btp[well]['Rhoo_SC'][i]] * (end_idx - start_idx))

                well_df = pd.DataFrame({
                    'Time': self.data_pi['Time'],
                    'Wells': [well] * len(self.data_pi['Time']),
                    'DeltaPManifold_PI': self.data_well_specific[well]['DeltaPManifold_PI'],
                    'DeltaPManifold_RWT': delta_p_manifold_rwt,
                    'P_ds_SDV_PI': self.data_well_specific[well]['P_ds_SDV_PI'],
                    'P_sep': self.data_pi['P_sep'],
                    'Qo_SC': self.data_pi['Qo_SC'],
                    'Qg_SC': self.data_pi['Qg_SC'],
                    'P_us_PI': self.data_well_specific[well]['P_us_PI'],
                    'T_us_PI': self.data_well_specific[well]['T_us_PI'],
                    'u_PI': self.data_well_specific[well]['u_PI'],
                    'Qgi_PI': self.data_well_specific[well]['Qgi_PI'],
                    'TimeBTP': time_btp,
                    'P_us_RWT': p_us_rwt,
                    'T_us_RWT': t_us_rwt,
                    'u_RWT': u_rwt,
                    'Qgi_RWT': qgi_rwt,
                    'P_ds_SDV_RWT': p_ds_sdv_rwt,
                    'rhoo_SC': rhoo_sc,
                })
                well_df.to_excel(writer, sheet_name=well, index=False)
        print("PI data saved to Excel.")

        # Save data_bdo to CSV
        bdo_df = pd.DataFrame(self.data_bdo)
        bdo_df.to_csv(os.path.join(self.data_directory, 'Data_BDO.csv'), index=False, sep=';')
        print("BDO data saved to CSV.")

    def read_and_process_data(self):
        self.read_btp_data()
        self.read_pi_data()
        self.read_bdo_data()
        self.ensure_consistent_lengths()
        self.save_data()

# Example usage:
# data_importer = DataImporter(data_directory="/content/vfm_v2/Python/Data/")
# data_importer.read_and_process_data()
